# Multi-Agent OS — Design

Status: draft v1
Branch: `claude/multi-agent-workflow-design-gNZgl`
Scope: company-scale, self-hosted, many agents, many processes
Author: design pass via Claude

---

## 0. TL;DR

Treat the platform as a real operating system for agents, not as a workflow tool with bots bolted on. The kernel is a durable workflow engine. Agents are deterministic orchestrations that wrap non-deterministic model calls as activities, so every run is replayable. Prompts, tools, and models are versioned artifacts gated by an eval harness. All model traffic flows through a self-hosted gateway that enforces per-tenant token and dollar budgets. Security is capability-based: every run gets a scoped, short-lived token, not ambient credentials. Everything runs on Kubernetes with GitOps.

One sentence: **Temporal as kernel, Claude Agent SDK as process runtime, Postgres+pgvector+Qdrant as memory hierarchy, NATS+MCP as IPC, LiteLLM as model gateway, OPA as policy, Langfuse as eval/trace, all on K8s.**

---

## 1. Scale targets

| Dimension | v1 (6 mo) | v2 (18 mo) |
|---|---|---|
| Concurrent runs | 1k | 50k |
| Distinct agents | 50 | 500 |
| Distinct processes | 20 | 200 |
| Tenants (internal teams) | 5 | 50 |
| Daily LLM spend ceiling | $2k | $50k |
| p50 run latency | 30s | 30s |
| p99 run latency | 10m | 10m |
| Eval suite size | 500 cases | 50k cases |
| RTO / RPO | 1h / 15m | 15m / 1m |

These numbers drive every "build vs. buy vs. defer" call below.

---

## 2. Non-goals

- Public multi-tenant SaaS. Internal platform only.
- Real-time (<1s) conversational UX. Latency target is interactive-but-async.
- Replacing existing systems of record (CRM, ticketing, data warehouse). The OS *orchestrates*; data lives where it lives.
- Training or fine-tuning models. Inference only, via gateway.
- Code-free authoring. Processes are code, reviewed in Git.

---

## 3. The OS metaphor (mapping)

| OS concept | In this system | Implementation |
|---|---|---|
| Kernel | Durable workflow engine | Temporal (self-hosted) |
| Process | Agent run (a workflow execution) | Temporal workflow |
| Thread | Activity inside a run | Temporal activity |
| Scheduler | Task queues + priorities + fairness | Temporal task queues + custom dispatcher |
| Syscall | Tool invocation | MCP call through capability-checked proxy |
| IPC | Inter-agent messaging | NATS JetStream + A2A protocol |
| Filesystem | Artifact + knowledge storage | MinIO (blobs) + Postgres (structured) + Qdrant (vectors) |
| Memory hierarchy | Context tiers (L1-L4) | Redis / Postgres / Qdrant / MinIO |
| Capabilities | Scoped permission tokens | Biscuit or SPIFFE-issued JWTs, verified by OPA |
| Package manager | Versioned agents/prompts/tools | OCI artifacts in Harbor, manifests in Git |
| Init system | Bootstrap + service discovery | ArgoCD + Kubernetes |
| Debugger | Trace + replay + step | Langfuse + Temporal replay + OpenTelemetry |
| /proc | Live introspection | Temporal Web UI + Grafana dashboards |

The metaphor is not decoration. It forces the right layer boundaries: no agent talks to a database directly, every action is a syscall, every syscall is audited, and every process is restartable from any checkpoint.

---

## 4. Architecture at a glance

```
                  +----------------------------------------+
                  |  Humans (operators, reviewers, admins) |
                  +-----------------+----------------------+
                                    |
                  +-----------------v----------------------+
                  |  Work plane UI (Next.js / Plane.so)    |
                  |  Approvals, dashboards, run inspector  |
                  +-----------------+----------------------+
                                    |
+-----------------+   +-------------v------------+   +------------------+
|  Eval harness   |   |   Control plane API      |   |  Observability   |
|  (Langfuse +    |<->|   (REST + gRPC, OPA)     |<->|  OTel, Grafana,  |
|   Promptfoo)    |   +-------------+------------+   |  Loki, Tempo,    |
+-----------------+                 |                |  Langfuse        |
                                    |                +------------------+
                  +-----------------v----------------------+
                  |  Kernel: Temporal cluster              |
                  |  (frontend / history / matching /      |
                  |  worker services, Postgres backend)    |
                  +-----------------+----------------------+
                                    |
            +-----------+-----------+-----------+-----------+
            |           |           |           |           |
       +----v----+ +----v----+ +----v----+ +----v----+ +---v----+
       | Agent   | | Agent   | | Agent   | | Agent   | |  ...   |
       | worker  | | worker  | | worker  | | worker  | |        |
       | pool A  | | pool B  | | pool C  | | pool D  | |        |
       +----+----+ +----+----+ +----+----+ +----+----+ +--------+
            |           |           |           |
            +-----------+-----+-----+-----------+
                              |
              +---------------v----------------+
              |  Model gateway (LiteLLM)        |
              |  budgets, caching, rate limit,  |
              |  failover, audit                 |
              +---------------+----------------+
                              |
              +---------------v----------------+
              |  Anthropic / OpenAI / local     |
              |  (vLLM on GPU nodes)            |
              +---------------------------------+

  Side planes:
    - MCP tool servers (one per capability domain): Slack, Jira, Gmail,
      internal APIs, SQL warehouse, code-exec sandbox, file ops.
    - NATS JetStream: events, A2A messages, signals.
    - Memory: Redis (L1), Postgres+pgvector (L2), Qdrant (L3), MinIO (L4).
    - Secrets: Vault. Identity: Keycloak (humans) + SPIRE (workloads).
    - Policy: OPA bundles distributed via OCI.
```

---

## 5. Kernel — durable workflow engine

**Pick: Temporal (self-hosted, OSS).**

Why: durable execution with deterministic replay, mature operators for K8s, first-class signals and queries (needed for HITL), strong language SDKs (Python + TS to match agent runtimes), Postgres or Cassandra persistence, battle-tested at companies running >10k workflows/sec.

Rejected:
- **Restate** — simpler model, but younger, smaller ecosystem; revisit at v2 for specific subsystems.
- **Conductor (Netflix)** — JSON workflows hurt code review and refactoring.
- **Airflow / Prefect / Dagster** — DAG-shaped, not durable-execution; wrong primitive for long-running agentic workflows with signals and HITL.
- **AWS Step Functions / Google Workflows** — managed, not self-hosted; vendor lock.
- **DBOS** — interesting, too young for company scale.
- **Build our own on Postgres** — we will lose two engineer-years rebuilding what Temporal already ships.

**Key invariant:** workflow code is deterministic. All non-determinism (LLM calls, HTTP calls, time, randomness) goes through activities. This is what makes runs replayable — the single biggest debugging superpower we get.

---

## 6. Process model

```
Tenant ──< Process (definition) ──< Run (instance) ──< Task ──< Event
                                       │                │
                                       └──< Artifact    └──< ToolCall
                                       └──< Message
                                       └──< Approval
```

- **Process**: a workflow definition (code in Git, versioned). E.g. "Customer escalation triage", "RFP response draft".
- **Run**: one execution of a process. Has an immutable input, a state machine, a budget, an owner, a tenant.
- **Task**: one activity inside a run — either an agent step, a tool call, a wait-for-signal, or a sub-workflow.
- **Agent**: a long-lived logical identity (role + system prompt + allowed tools + policy). An agent does not own a process; processes invoke agents.
- **Artifact**: any output worth persisting (draft doc, SQL query, plot, code patch).
- **Message**: durable inter-agent or agent-to-human communication, on NATS, mirrored to Postgres.
- **Approval**: a typed signal awaited by a workflow, satisfied by a human in the UI.

Why split Agent from Process: the same agent ("Researcher") is reused across many processes; the same process can swap agents under A/B. This is the analogue of programs vs. processes in Unix.

---

## 7. Scheduler — priorities, fairness, backpressure

Temporal alone gives task queues. Company scale needs more:

- **Per-tenant task queues** with weighted fair share. Tenant A's burst cannot starve Tenant B.
- **Priority lanes** per queue: `interactive`, `batch`, `background`. Interactive runs preempt batch in worker assignment, never mid-activity.
- **Concurrency caps** per (tenant, model, tool). LiteLLM enforces model-side; a sidecar token-bucket enforces tool-side.
- **Backpressure**: when queue depth or model gateway 429s exceed thresholds, the control plane rejects new runs with `Retry-After` instead of letting Temporal accumulate millions of pending activities.
- **Deadlines**: every run carries a wall-clock deadline. Activities check the deadline before each LLM call. Past deadline → fail-soft to a "best partial result" path.

---

## 8. Memory hierarchy

| Tier | Purpose | Store | TTL | Typical size |
|---|---|---|---|---|
| L1 conversation buffer | Working context for the current run | Redis | Run lifetime + 1h | ~100KB / run |
| L2 episodic | Past runs, decisions, outcomes per agent/tenant | Postgres + pgvector | 90d hot, archive cold | ~10GB / tenant |
| L3 semantic | Org knowledge: docs, wikis, code, tickets | Qdrant (chunks) + Postgres (sources) | Indefinite, re-indexed weekly | ~100GB total |
| L4 cold artifacts | Raw outputs, attachments, large blobs | MinIO (S3-compatible) | Per retention policy | Unlimited |

Rules:
- **No agent reads L3 or L4 directly.** Memory access is a syscall (`memory.search`, `memory.fetch`) that returns typed, attributed, capability-checked results.
- **Every retrieval is logged** with query, results, scores. Required for eval reproducibility.
- **Writes to L2/L3 are mediated** by a "librarian" subsystem that handles chunking, dedup, embedding, and PII redaction.

Embedding model is pinned and versioned alongside the index. Re-embedding is a planned migration, not an ambient drift.

---

## 9. IPC

Three channels, each with a clear job:

1. **Workflow signals (Temporal)** — typed, in-process. Used for HITL approvals, parent-child handoffs, cancellation.
2. **NATS JetStream** — durable pub/sub for cross-process and cross-cluster events. Used for "new ticket arrived", "model degraded", "budget threshold crossed", agent-to-agent broadcasts.
3. **A2A (agent-to-agent) protocol over MCP** — for synchronous request/response between agents that are not parent/child in a workflow. Wrapped in capability checks at the gateway.

Anti-pattern banned by lint: agents writing to each other's memory directly. Always go through a typed message or a syscall.

---

## 10. Syscalls — tool registry and contracts

Every external action is a tool call. Tools are MCP servers, one per capability domain. Each tool publishes a manifest:

```yaml
name: jira.create_issue
version: 1.4.0
owner: platform-eng
schema:
  input:  { project: string, summary: string, body: markdown, labels: [string] }
  output: { key: string, url: string }
side_effects: write
idempotency_key: required
capabilities_required: [jira:write:project=<param.project>]
cost_class: cheap
rate_limit: 60/min/tenant
audit: full
```

The registry enforces:
- **Typed I/O** — invalid args rejected before the model is charged.
- **Idempotency** — every write tool requires a key; replays are safe.
- **Capability binding** — the tool proxy verifies the run's capability token covers the requested action against OPA before forwarding.
- **Cost class** — cheap / standard / expensive / dangerous; expensive and dangerous classes require explicit budget and (optionally) human approval.
- **Audit** — full request/response logged with run id, agent id, tenant id.

This is the syscall ABI of the OS. Adding a tool is a PR with manifest + tests + eval.

---

## 11. Security

Capability-based, not role-based at the data path.

- **Run identity**: each run gets a SPIFFE workload identity and a short-lived capability token (Biscuit) listing exactly the tools, scopes, and resources it may touch. Token lifetime = run deadline.
- **Policy as code**: OPA bundles distributed via OCI. Policies cover: who can launch which process, against which tenant data, with which tools, up to which budget, requiring which approvals.
- **Secrets**: Vault. Agents never see raw secrets — tools receive them via short-lived leases.
- **Human identity**: Keycloak (OIDC), groups synced from HRIS.
- **Data isolation**: per-tenant Postgres schemas; row-level security as defense in depth; per-tenant Qdrant collections; per-tenant MinIO buckets with bucket policies.
- **PII**: a redaction sidecar runs on all messages crossing the model gateway when policy demands it; redaction events are themselves audited.
- **Egress**: agent pods have no internet egress except via the model gateway and the tool proxy. Enforced at the CNI layer.
- **Supply chain**: all images signed (cosign), SBOMs generated, admission controller rejects unsigned or vulnerable images.

---

## 12. Model gateway and cost governance

**Pick: LiteLLM (self-hosted).** One ingress to Anthropic, OpenAI, and a local vLLM cluster for open models on GPU nodes.

Functions:
- **Routing** by model name + tenant policy (e.g. EU tenants must use EU-region Anthropic).
- **Caching** at prompt-prefix level for prompt caching savings (Anthropic), plus a Redis layer for full-prompt exact match.
- **Rate limiting and failover** with circuit breakers per provider.
- **Token + dollar budgets** per (tenant, process, run). Hard ceilings. Soft warnings at 50/80/95%.
- **Audit log** of every call: prompt hash, model, tokens, cost, latency, cache hit, tenant, run id.
- **Key rotation** without redeploys.

Cost reporting: Prometheus metrics exported per tenant/process; Grafana dashboard for chargeback; weekly cost report auto-posted to a NATS topic that the Finance agent picks up.

---

## 13. Package manager — prompts, agents, tools as artifacts

Three artifact kinds, one registry (Harbor as OCI):

| Kind | Versioned how | Promotion gate |
|---|---|---|
| Prompt | Markdown + frontmatter in Git, hashed, packaged as OCI artifact | Eval suite green on canary tenant |
| Agent | Manifest + prompt refs + tool refs + policy, packaged as OCI | All referenced eval suites green; staged rollout |
| Tool | MCP server image + manifest | Integration tests + capability review |

Process workflows reference artifacts by digest, not tag, for reproducibility. Tag-to-digest resolution happens at deploy.

A run records the exact digest of every artifact it used. Replaying a run pins to those digests — model included.

---

## 14. Evals as release gate

No prompt, agent, or model change reaches production without a green eval run.

- **Suites**: per-agent and per-process, written as code, stored in Git, executed by Langfuse (with Promptfoo for the prompt-only cases).
- **Cases**: golden input/output, plus rubric-graded LLM-as-judge for open-ended outputs, plus production traffic replay (sampled, scrubbed).
- **Gates**: a PR that changes a prompt triggers the affected suites in CI; the merge is blocked on green + cost-delta below threshold.
- **Shadow traffic**: candidate prompts run alongside production at low percentage; outputs are graded offline; promotion is a config flip.
- **Regression catalog**: every production incident produces at least one new eval case. The eval suite grows monotonically.

---

## 15. Human-in-the-loop

HITL is a first-class workflow primitive, not a hack.

- Workflows declare typed `Approval[T]` waits with SLAs.
- The work-plane UI surfaces queues per role, with context (run trace, artifacts, suggested decision, similar past cases).
- Timeouts are explicit: every approval has an `on_timeout` branch (escalate, auto-deny, auto-approve with notification, etc.).
- Bulk approvals supported for high-volume low-risk decisions, with sampling-based audit.
- Every approval records the human identity, the rendered context, and the decision — auditable forever.

---

## 16. Observability

OpenTelemetry everywhere. Three views:

- **System view** — Grafana on Prometheus (metrics), Loki (logs), Tempo (traces). SRE-grade dashboards: queue depth, worker saturation, gateway 4xx/5xx, budget burn.
- **Run view** — Temporal Web UI for workflow structure; Langfuse for LLM-specific traces (prompts, completions, scores, costs).
- **Agent view** — per-agent health: success rate, p95 latency, eval pass rate trend, cost per run, top failure modes.

Alerting via Alertmanager → PagerDuty (or self-hosted Grafana OnCall). On-call rotates within the platform team.

---

## 17. Data model (core tables)

Postgres, schema per tenant. Abbreviated:

```sql
-- Definitions (deploy-time)
process_def (id, name, version, digest, owner_team, default_budget_usd, deadline_s, created_at)
agent_def   (id, name, version, digest, system_prompt_ref, tools[], policy_ref, model_ref)
tool_def    (id, name, version, digest, manifest_jsonb)
prompt_def  (id, name, version, digest, body_ref, model_hint)

-- Runtime
run         (id, tenant_id, process_def_id, status, started_at, ended_at,
             deadline_at, budget_usd, spent_usd, owner_user_id, parent_run_id,
             input_jsonb, output_jsonb, error_jsonb)
task        (id, run_id, agent_def_id, kind, status, started_at, ended_at,
             input_jsonb, output_jsonb, retries, span_id)
tool_call   (id, task_id, tool_def_id, input_jsonb, output_jsonb,
             idempotency_key, cost_usd, latency_ms, status, span_id)
model_call  (id, task_id, model, prompt_hash, in_tokens, out_tokens,
             cost_usd, cache_hit, latency_ms, span_id)
message     (id, run_id, from_agent_id, to_agent_id_or_topic, body_jsonb,
             created_at)
artifact    (id, run_id, kind, uri, sha256, size_bytes, mime, created_at)
approval    (id, run_id, task_id, type, requested_at, decided_at,
             decided_by, decision, context_ref)
event       (id, run_id, kind, payload_jsonb, created_at)

-- Cross-cutting
audit_log   (id, actor, action, target, before_jsonb, after_jsonb, at)
budget      (id, scope, period, limit_usd, spent_usd)
capability_token (id, run_id, jti, scopes, issued_at, expires_at, revoked_at)
```

All timestamps UTC, all `_jsonb` columns schema-validated against the artifact's manifest at write time.

---

## 18. Example workflow (pseudocode)

```python
# process: customer_escalation_triage v3.2.1
@workflow.defn
class EscalationTriage:
    @workflow.run
    async def run(self, ticket: Ticket) -> TriageOutcome:
        ctx = RunContext.current()
        ctx.set_deadline(minutes=20)
        ctx.set_budget(usd=2.50)

        classified = await workflow.execute_activity(
            agents.Classifier.classify, ticket,
            start_to_close_timeout=timedelta(minutes=2),
            retry_policy=RetryPolicy(maximum_attempts=3),
        )

        if classified.severity == "P1":
            approval = await workflow.wait_for_signal(
                "human_approval", timeout=timedelta(minutes=10),
                on_timeout=Escalate(to="oncall-lead"),
            )
            if not approval.granted:
                return TriageOutcome.declined(reason=approval.reason)

        draft = await workflow.execute_activity(
            agents.Responder.draft_reply, classified,
            start_to_close_timeout=timedelta(minutes=5),
        )

        await workflow.execute_activity(
            tools.zendesk.post_reply,
            ZendeskReply(ticket_id=ticket.id, body=draft.body,
                         idempotency_key=ctx.idem("zendesk_reply")),
        )
        return TriageOutcome.handled(draft_id=draft.id)
```

Note what is and is not in workflow code: no LLM calls, no network, no time-of-day, no randomness. All non-determinism is fenced into activities.

---

## 19. Self-hosted reference stack

| Layer | Pick | Why | Rejected alternatives |
|---|---|---|---|
| Workflow engine | Temporal | Durable, replay, signals, scale | Restate, Conductor, Airflow, Cadence |
| Agent runtime | Claude Agent SDK (Python + TS) | First-class agent loop, MCP native | LangGraph, CrewAI, AutoGen, custom |
| Model gateway | LiteLLM | OSS, budgets, multi-provider | Portkey (managed), homegrown |
| Local inference | vLLM on GPU nodes | Throughput, OpenAI-compatible | TGI, Ollama (single-node) |
| Tool protocol | MCP | Open, growing ecosystem | OpenAPI-only, custom RPC |
| Event bus | NATS JetStream | Lightweight, durable, multi-tenant | Kafka/Redpanda (overkill v1), RabbitMQ |
| OLTP | Postgres (CloudNativePG operator) | Boring, proven, pgvector | MySQL, CockroachDB |
| Vector store | Qdrant | Filtering, hybrid search, OSS | Weaviate, Milvus, pgvector-only |
| Object store | MinIO | S3-compatible, simple ops | SeaweedFS, Ceph (heavier) |
| Cache | Redis | Ubiquitous | KeyDB, Dragonfly (revisit) |
| Secrets | Vault | Standard, dynamic creds | Infisical (younger), SOPS-only |
| Workload ID | SPIRE (SPIFFE) | Industry standard mTLS identity | Plain mTLS |
| Human ID | Keycloak | Mature OIDC, federation | Ory, Authentik |
| Policy | OPA + Rego | Mature, declarative, bundles | Cedar, Casbin |
| Capability tokens | Biscuit | Offline-verifiable, attenuable | Macaroons, plain JWT |
| Eval / LLM trace | Langfuse (self-hosted) | OSS, traces + evals + datasets | Phoenix, Helicone, custom |
| Prompt regression | Promptfoo | Lightweight, CI-friendly | Inside Langfuse only |
| Metrics | Prometheus + Thanos | Standard, long retention | VictoriaMetrics (close call) |
| Logs | Loki | Cheap, label-based | Elastic (heavier) |
| Traces | Tempo | Pairs with Loki/Grafana | Jaeger |
| Dashboards | Grafana | Standard | Plain |
| Container orch | Kubernetes (Talos nodes) | Industry default, operators everywhere | Nomad (lighter but smaller ecosystem) |
| GitOps | ArgoCD | Mature, multi-cluster | Flux |
| Registry | Harbor | OCI artifacts, signing, scanning | plain registry |
| Image signing | cosign | Standard | notary v1 |
| CI | GitLab CE or Gitea Actions | Self-hosted | Drone (slimmer roadmap) |
| Work plane UI | Custom Next.js + Plane.so for tickets | Tailored UX | Retool/Appsmith (limit on agent UX) |
| Code-exec sandbox | Firecracker microVMs or gVisor pods | Strong isolation for agent-generated code | Plain containers (insufficient) |

---

## 20. Deployment topology

- **Three K8s clusters**: `platform-prod`, `platform-stage`, `platform-dev`. Each cluster owns its Temporal, Postgres (CNPG), NATS, Qdrant, MinIO, LiteLLM, observability stack.
- **GPU node pool** in `platform-prod` for vLLM; tainted, autoscaled by KEDA on queue depth.
- **Multi-AZ** within a region for v1. Active-passive cross-region for v2 (Postgres logical replication, MinIO async replication, Temporal global namespaces).
- **Backups**: Postgres PITR (15-min RPO), MinIO versioning + cross-bucket replication, Qdrant snapshots nightly, Vault snapshots daily, all to a separate object-store account.
- **DR drill**: quarterly restore-from-snapshot exercise on a scratch cluster, tracked as a process in the OS itself.

---

## 21. Multi-tenancy and RBAC

- **Tenant = internal team or product area.** Each tenant has: schema, vector collection, object bucket, NATS account, Temporal namespace, Vault path, budget envelope.
- **RBAC roles**: `viewer`, `operator`, `approver`, `developer`, `tenant-admin`, `platform-admin`. Mapped from Keycloak groups.
- **OPA decisions** carry the tenant id; cross-tenant data access is denied by default and requires an explicit policy entry plus audit.

---

## 22. Failure modes per layer

| Layer | Likely failure | Mitigation |
|---|---|---|
| Model provider | Outage, 5xx, rate limit | Gateway failover to alt provider or local vLLM; circuit breaker; queue with bounded wait |
| Tool (MCP) | Slow, flaky, breaking change | Per-tool timeouts; semver-pinned manifests; canary on tool upgrades |
| Workflow worker | OOM, crash | Temporal resumes on another worker; activities idempotent |
| Postgres | Primary loss | CNPG failover; PITR; runbook tested quarterly |
| NATS | Stream loss | Replicated streams; runs fall back to Temporal signals for critical paths |
| Vector store | Index corruption | Re-index from source-of-truth artifacts; embeddings versioned |
| Gateway budget exceeded | Tenant runaway | Hard cap → run fails fast with budget error; alert; auto-throttle |
| Eval false-green | Bad prompt ships | Shadow traffic + production sampling re-evals; fast rollback by digest pin |
| Capability token leak | Lateral movement | Short TTL; revocation list checked at tool proxy; SPIFFE attestation |
| Human approver overload | Backlog | Per-approver SLA dashboards; auto-route by load; escalation policy |

---

## 23. Phased rollout

**Phase 0 — Foundation (weeks 1-6).** Exit when: a Hello-Process runs end-to-end in `platform-dev` with traces, budgets, and one tool call.
- K8s clusters + GitOps + observability stack.
- Temporal, Postgres, NATS, MinIO, Qdrant, Redis, LiteLLM, Langfuse, Keycloak, Vault, OPA, SPIRE.
- One reference agent + one reference tool + one reference process.

**Phase 1 — First production process (weeks 7-14).** Exit when: one real business process runs for one tenant with SLAs met, eval gate enforced, HITL working, cost dashboard live.
- Eval harness wired to CI; promotion-by-digest live.
- Capability tokens enforced at tool proxy.
- Tenant onboarding runbook.

**Phase 2 — Multi-tenant scale (months 4-9).** Exit when: 5 tenants, 20 processes, 50 agents, cost chargeback monthly, DR drill green.
- Per-tenant queues + fairness scheduler.
- Local vLLM cluster online.
- A2A protocol in production for at least one multi-agent workflow.
- Backups + PITR validated.

**Phase 3 — Hardening (months 10-18).** Exit when: targets in §1 met; on-call quiet weeks.
- Active-passive cross-region.
- Shadow traffic eval pipeline.
- Code-exec sandbox (Firecracker) generally available.
- Internal agent/prompt/tool marketplace.

---

## 24. Open questions

1. **Workflow language ergonomics.** Pure Temporal Python is verbose for branchy agent flows. Consider a thin DSL or codegen, but only after we have ≥10 real processes — avoid premature abstraction.
2. **Episodic memory write policy.** Who decides what graduates from L1 to L2? Naive "everything" floods the store; agent-decided is unreliable. Likely answer: a small "summarizer" process per agent run, gated by a quality eval.
3. **Cross-tenant knowledge sharing.** Some org knowledge (HR policy, engineering wiki) is global; how do we model that without weakening isolation? Likely a shared `org` tenant with read-only fan-out and explicit redaction policies.
4. **Local model strategy.** Which open models cover which cost classes acceptably? Needs a quarterly bake-off.
5. **MCP version skew.** As the MCP spec evolves, how do we pin and migrate? Treat MCP versions like protocol versions: support N and N-1, deprecate on a schedule.
6. **Marketplace governance.** Once teams publish their own agents/tools, who reviews? Probably a lightweight platform-team review for `cost_class >= expensive` or `side_effects = write` outside the publisher's tenant.

---

## 25. Appendix — what we explicitly are not building

- A no-code workflow editor.
- A general-purpose RAG system. Memory is a system service, not a product.
- A bespoke vector DB or workflow engine.
- A model router smarter than LiteLLM until we have data showing it pays back.
- A custom protocol where MCP suffices.

When in doubt, do less. The OS metaphor only works if each layer stays small enough to reason about.
