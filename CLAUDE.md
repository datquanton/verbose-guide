# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a content-only repository. There is no build system, no dependencies, no tests, and no source code — only Markdown files tracked in git.

The sole content file is `spotify-playlist-artists.md`, a flat bulleted list of artist names.

## Conventions

- Artist lists are maintained as a single-level Markdown bullet list (`- Name`), one artist per line, preserving the order they appear in the source playlist rather than sorting alphabetically.
- Preserve diacritics and non-ASCII characters exactly as spelled by the artist (e.g. `Victoria Monét`, `Hoàng Dũng`, `Mỹ Anh`).
- Keep each file focused on a single list; use the top-level `#` heading to name it.

## Workflow

- Branch naming follows `claude/<short-description>-<suffix>` (see existing `claude/add-spotify-playlist-artists-y4Vk4`, `claude/add-claude-documentation-mfyss`).
- Commits are short imperative summaries (e.g. `Add Spotify playlist artists list`).
- There is nothing to lint, build, or test — verification is visual review of the rendered Markdown.
