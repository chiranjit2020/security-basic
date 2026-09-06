---
description: The site's design system — a Red Hat Design System–derived palette, type scale, spacing, and components on an Ubuntu-typeface dark theme.
---

# Design System

The visual language of this site is adapted from the
**[Red Hat Design System](https://ux.redhat.com/)** — its neutral gray scale,
Red Hat red, type scale, 4px-based spacing, 3px radius, and visible focus ring.
The typeface is **Ubuntu / Ubuntu Mono** rather than the Red Hat font family
(with **OCR A Std** on the wordmark, headings, and inline code), and the theme
is dark-first.

All values live as CSS custom properties in `docs/stylesheets/extra.css`
(`--rh-*` for raw tokens, `--sb-*` for the semantic light/dark bindings).

---

## Color

### Neutrals — `--rh-color-gray-*`

<div class="sb-swatches" markdown="0">
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#f2f2f2"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-10</span><br><span class="sb-swatch__hex">#f2f2f2</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#e0e0e0"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-20</span><br><span class="sb-swatch__hex">#e0e0e0</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#c7c7c7"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-30</span><br><span class="sb-swatch__hex">#c7c7c7</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#a3a3a3"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-40</span><br><span class="sb-swatch__hex">#a3a3a3</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#707070"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-50</span><br><span class="sb-swatch__hex">#707070</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#4d4d4d"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-60</span><br><span class="sb-swatch__hex">#4d4d4d</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#383838"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-70</span><br><span class="sb-swatch__hex">#383838</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#292929"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-80</span><br><span class="sb-swatch__hex">#292929</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#1f1f1f"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-90</span><br><span class="sb-swatch__hex">#1f1f1f</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#151515"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">gray-95</span><br><span class="sb-swatch__hex">#151515</span></span></div>
</div>

### Brand & status

<div class="sb-swatches" markdown="0">
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#ee0000"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">red-50 · brand</span><br><span class="sb-swatch__hex">#ee0000</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#a60000"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">red-60 · brand hover</span><br><span class="sb-swatch__hex">#a60000</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#0066cc"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">blue-50 · link (light)</span><br><span class="sb-swatch__hex">#0066cc</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#92c5f9"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">blue-30 · link (dark)</span><br><span class="sb-swatch__hex">#92c5f9</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#63993d"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">green-50 · tip</span><br><span class="sb-swatch__hex">#63993d</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#f5921b"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">orange-40 · warning</span><br><span class="sb-swatch__hex">#f5921b</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#f0561d"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">red-orange-50 · danger</span><br><span class="sb-swatch__hex">#f0561d</span></span></div>
  <div class="sb-swatch"><span class="sb-swatch__chip" style="background:#876fd4"></span><span class="sb-swatch__meta"><span class="sb-swatch__name">purple-40 · question</span><br><span class="sb-swatch__hex">#876fd4</span></span></div>
</div>

### Semantic bindings

| Token | Light | Dark |
|---|---|---|
| `--sb-surface` | `#ffffff` | `gray-95` `#151515` |
| `--sb-surface-raised` | `gray-10` `#f2f2f2` | `gray-90` `#1f1f1f` |
| `--sb-text` | `gray-95` `#151515` | `gray-10` `#f2f2f2` |
| `--sb-text-muted` | `gray-60` `#4d4d4d` | `gray-30` `#c7c7c7` |
| `--sb-border` | `gray-30` `#c7c7c7` | `gray-70` `#383838` |
| `--sb-link` | `blue-50` `#0066cc` | `blue-30` `#92c5f9` |
| `--sb-brand` | `red-50` `#ee0000` | `red-50` `#ee0000` |

---

## Typography

Families: **Ubuntu** (body text), **OCR A Std** (the wordmark, every heading,
and inline code), **Ubuntu Mono** (code blocks and ASCII/tree diagrams — OCR A
has no box-drawing or arrow glyphs, so diagram blocks stay on Ubuntu Mono to
keep the monospace grid). Body line-height `1.5`, heading line-height `1.3`.
Headings render at a compressed 22 → 16 px scale.

<div markdown="0">
  <div class="sb-type-row"><span class="sb-type-row__label">h1<br>1.375rem · 700 · OCR A</span><span style="font-family:'OCR A Std',monospace;font-size:1.375rem;font-weight:700">Web Security</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">h2<br>1.25rem · 700 · OCR A</span><span style="font-family:'OCR A Std',monospace;font-size:1.25rem;font-weight:700">Confidentiality</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">h3<br>1.125rem · 500 · OCR A</span><span style="font-family:'OCR A Std',monospace;font-size:1.125rem;font-weight:500">Broken confidentiality</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">h4–h6<br>1rem · OCR A</span><span style="font-family:'OCR A Std',monospace;font-size:1rem;font-weight:700">Session-based authentication</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">body-lg<br>1.125rem · 400</span><span style="font-size:1.125rem">Where is my data right now, and what protects it?</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">body-md<br>1rem · 400</span><span style="font-size:1rem">Encryption protects secrecy. Hashing verifies integrity.</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">body-sm<br>0.875rem · 400</span><span style="font-size:0.875rem">Caption and helper text</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">inline code<br>OCR A Std</span><span style="font-family:'OCR A Std',monospace">GET /api/users/42</span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">code block<br>Ubuntu Mono</span><span style="font-family:'Ubuntu Mono',monospace">GET /api/users/42</span></div>
</div>

---

## Spacing

A 4px-based scale (`--rh-space-*`) drives content rhythm — paragraph and heading
margins, admonition padding, grid gaps.

<div markdown="0">
  <div class="sb-type-row"><span class="sb-type-row__label">xs · 4px</span><span class="sb-space-bar" style="width:4px"></span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">md · 8px</span><span class="sb-space-bar" style="width:8px"></span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">lg · 16px</span><span class="sb-space-bar" style="width:16px"></span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">xl · 24px</span><span class="sb-space-bar" style="width:24px"></span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">2xl · 32px</span><span class="sb-space-bar" style="width:32px"></span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">3xl · 48px</span><span class="sb-space-bar" style="width:48px"></span></div>
  <div class="sb-type-row"><span class="sb-type-row__label">4xl · 64px</span><span class="sb-space-bar" style="width:64px"></span></div>
</div>

---

## Shape & focus

- **Border radius:** `3px` everywhere (`--rh-border-radius`); pills at `64px`.
- **Border widths:** `1px` hairline, `2px` emphasis, `3px` keyline.
- **Focus ring:** `2px` solid blue, `2px` offset — never removed.

---

## Components

### Admonitions

Each is a card with a `3px` left keyline in its status color and a faint tinted
title bar.

!!! question "question — opens every chapter"
    State the question this chapter answers.

!!! note "note"
    Supporting context.

!!! tip "tip"
    A recommended practice.

!!! warning "warning"
    Something to be careful about.

!!! danger "danger"
    A real hazard — e.g. storing passwords with plain SHA-256.

### Table

| State | Confidentiality | Integrity |
|---|---|---|
| At rest | Encryption, access control | Hashes, DB controls |
| In transit | TLS | TLS, MACs / signatures |

### Buttons

[Primary action](#){ .md-button .md-button--primary }
[Secondary action](#){ .md-button }

### Code

```text
Browser
   │  HTTPS  (data in transit)
   ↓
Web server
```

---

## Attribution

Palette, scale, and interaction patterns are derived from the
[Red Hat Design System](https://ux.redhat.com/) and
[Red Hat design tokens](https://github.com/RedHat-UX/red-hat-design-tokens)
(Red Hat, Inc.). This is an independent learning project and is not affiliated
with or endorsed by Red Hat.
