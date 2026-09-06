# Security Basics

A backend developer's **mental model** for web application security — built as one
connected map instead of a pile of isolated facts.

Two anchor models run through every chapter:

- **Three states of data** — *at rest*, *in use*, *in transit*. Where is the data right now?
- **CIA triad** — *confidentiality*, *integrity*, *availability*. What property are you protecting?

Every mechanism (TLS, hashing, RBAC, sessions, JWT, …) is introduced as an answer to a
*"why"* posed in terms of those two models.

---

## How each chapter is structured

Each chapter opens with a **question**, followed by the worked-through answer.

!!! question "Example"
    Is backup data a fourth state of data?

Then the solution content follows.

---

## Where to start

- [Foundations](foundations/index.md) — the states-of-data model every later chapter leans on.
- [Chapters](chapters/index.md) — the security sequence, starting with the CIA Triad.

More are added as they are written.
