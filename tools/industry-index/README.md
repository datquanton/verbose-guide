# Industry section index

Organises `/nganh/` by industry without moving any page (old links keep working).

```
python3 tools/industry-index/build.py      # from the repository root; also run by tools/mirae-coverage/build.py
```

`sections.json` is the registry: the industries (id, name and one-line description in both languages) and every report with its path, date, kind (Mirae / quarterly data / outlook / earnings review), whether an English version exists, and the industries it belongs to. A report covering several industries is listed under each. Titles and summaries of vault-built reports are copied from their cards; Mirae pages take theirs live from `tools/mirae-coverage/meta.json`.

The script writes:
- `nganh/index.html` (rewritten inside its existing header and footer) and `nganh/en/index.html` (new; header and footer taken from `/en/`), grouped by industry with a jump row;
- an industry jump row under the Ngành / Sectors heading on `/` and `/en/` (the English heading now links to `/nganh/en/`);
- a "same industry" box at the end of every report listed in the registry, vault-built ones included.

Inserted blocks sit between `<!-- industry-index -->` markers and are replaced on each run; a second run changes nothing.

**When a new report is published:** add a row to `sections.json`, then run the script. **After a vault `publish.sh` copy-in:** run `python3 tools/mirae-coverage/build.py` (rebuilds the Mirae pages, then this index). Until the vault generator itself knows about this structure, its copy-in will overwrite `nganh/index.html` and remove the inserted blocks; the command above restores them.
