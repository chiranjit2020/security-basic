# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A **documentation site** ("Security Basics") built with **MkDocs + Material**, teaching web
application security as an *engineering mental model* for a backend developer rather than as
exam definitions. Published to GitHub Pages at
`https://chiranjit2020.github.io/security-basic/`.

Content is authored by the repo owner. Each chapter is delivered as: **a question, then the
owner's solution content**. Claude's job is to place that content into the site, not to
rewrite it — preserve the author's wording, diagrams, and voice.

## Commands

```bash
pip install -r requirements.txt        # one-time setup (needs mkdocs-material 9.7.x)
python -m mkdocs serve                  # live preview at http://127.0.0.1:8000
python -m mkdocs build --strict         # full build to ./site (must pass before pushing)
```

`mkdocs` / `mkdocs.exe` is not on PATH in this environment — always invoke via `python -m mkdocs`.
Push to `main` triggers `.github/workflows/deploy.yml`, which builds with `--strict` and
deploys to GitHub Pages. GitHub repo Settings → Pages → Source must be set to "GitHub Actions".

## Layout

- `docs/` — the published site (this is `docs_dir`).
  - `docs/index.md` — landing page; explains the two anchor models and the Q&A format.
  - `docs/foundations/` — states-of-data material that precedes the security sequence
    (`states-of-data.md`, `backup-data.md`). Same question-first format as chapters.
  - `docs/chapters/index.md` — chapter list; has a table + `nav` reminder in an HTML comment.
  - `docs/chapters/NN-slug.md` — one file per chapter.
  - `docs/assets/` — images (e.g. `3-states-of-data.png`).
  - `docs/stylesheets/extra.css` — dark-theme tweaks and the `.question` admonition styling.
- `mkdocs.yml` — site config. Theme: Material, `scheme: slate` (forced dark), fonts
  Ubuntu / Ubuntu Mono. Build is `--strict` with `validation:` set to warn on omitted/broken links.
- `CHAPTER_TEMPLATE.md` (repo root, kept out of `docs/` so `--strict` stays clean) — start
  every new chapter from this.
- `drafts/` — the owner's raw source notes; **not** part of the built site. The `chapter-NN`
  filenames do not match the published chapter numbers. Mapping of what's been published:
  - `chapter-01.md` → `foundations/states-of-data.md`
  - `chapter-02.md` → `foundations/backup-data.md`
  - `chapter-03.md` → *empty*
  - `chapter-04.md` → `roadmap.md`
  - `chapter-05.md` → `chapters/01-cia-triad.md`
  - `chapter-06.md` → `chapters/02-authentication-vs-authorization.md`
  - `chapter-07.md` → `chapters/03-encryption-hashing-encoding.md`
  New drafts may land as `drafts/chapter-08.md`, etc. `3-states-of-data.png` lives here and
  is copied to `docs/assets/`.
- `.github/workflows/deploy.yml` — CI build + Pages deploy.

## Adding a chapter (the core workflow)

1. Copy `CHAPTER_TEMPLATE.md` to `docs/chapters/NN-slug.md`.
2. Fill the `!!! question "The question"` admonition with the chapter's opening question.
3. Paste the owner's solution content verbatim below the marker comment.
4. Add a row to the table in `docs/chapters/index.md`.
5. Add the file to the `nav:` → `Chapters:` list in `mkdocs.yml` (order = chapter order).
6. Run `python -m mkdocs build --strict` — it must pass with no warnings.
7. Commit and push to `main`.

## House style (when formatting delivered content)

- Second person, addressed to the developer-reader; conversational, direct.
- Lead with the question a concept answers, then the mechanism.
- ASCII diagrams stay in ```text fences; keep the `↓ │ ┌ └ ┼` vocabulary as the author wrote it.
- Markdown tables to cross concepts (e.g. data-state × CIA property).
- Keep the author's sparse heading emoji (🔐 🧱 ⚡ 🧠); don't add more.
- Preserve precise vulnerability names (IDOR/BOLA, DDoS) and hedged claims ("TLS helps prevent…").
- Recurring worked example across chapters: a cloud-kitchen / e-commerce app with
  Owner / Manager / Staff roles. Keep it consistent; don't invent new domains.
