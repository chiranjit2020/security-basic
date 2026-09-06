---
description: Encryption vs hashing vs encoding — three different jobs. Why Base64 isn't encryption, why SHA-256 isn't password storage, and where each belongs.
---

# Chapter 3 — Encryption vs Hashing vs Encoding

!!! question "The question"
    HTTPS, passwords, JWT, API keys, Base64, AES, RSA, SHA-256, bcrypt, Argon2 — a beginner
    lumps them together as "ways of making data unreadable." Why is that wrong, and what
    problem does each one actually solve?

This is a **critical chapter for web development**, because these three terms are constantly mixed up.

You will encounter:

* HTTPS
* Passwords
* JWT
* API keys
* Base64
* AES
* RSA
* SHA-256
* bcrypt
* Argon2

A beginner often thinks:

> “They're all ways of converting data into something unreadable.”

**That's wrong.**

They solve fundamentally different problems.

---

## 1. The big picture

Think of three different goals:

```text
                    DATA
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
      ENCRYPTION   HASHING   ENCODING
          │          │          │
       Hide data   Verify /   Represent
       from others  identify    data
          │          │          │
       Reversible  One-way    Reversible
```

The simplest rule:

> **Encryption protects secrecy.**
> **Hashing protects/verifies integrity or stores passwords safely.**
> **Encoding changes representation.**

---

## 2. Encryption 🔒

#### Goal:

> **Keep data secret from people who don't have the key.**

Encryption transforms:

```text
Plaintext
    ↓
  🔐 Key
    ↓
Ciphertext
```

And with the appropriate key:

```text
Ciphertext
    ↓
  🔑 Key
    ↓
Plaintext
```

#### Important:

**Encryption is reversible.**

That's the defining characteristic.

---

### Web-development example

Suppose your application has:

```text
Customer
    ↓
Credit-card-related information
```

You don't want someone who obtains the stored data to simply read it.

Conceptually:

```text
"Sensitive data"
      ↓
    AES key
      ↓
"8fA2...x91"
```

When your authorized application needs the original data:

```text
"8fA2...x91"
      ↓
    AES key
      ↓
"Sensitive data"
```

That's encryption.

---

## 3. Encryption has a key

This is crucial.

```text
Encryption = Algorithm + Key
```

For example:

```text
AES + secret key
```

Without the key, the ciphertext should be computationally impractical to decrypt.

You'll later learn:

#### Symmetric encryption

Same key:

```text
        🔑
        │
Plain → Encrypt → Cipher
                    │
                    ↓
                   🔑
                    │
                 Decrypt
                    ↓
                  Plain
```

Examples:

**AES, ChaCha20**

---

#### Asymmetric encryption

Two related keys:

```text
Public Key  🔓
Private Key 🔐
```

The public key can be shared.

The private key must remain secret.

You'll encounter:

**RSA, ECC**

Don't worry about the mathematics yet.

---

## 4. Hashing #️⃣

Now we have something completely different.

#### Goal:

> **Produce a fixed-size fingerprint of data.**

```text
Input
  ↓
Hash function
  ↓
Hash
```

For example:

```text
"hello"
   ↓
SHA-256
   ↓
2cf24dba5fb0a30e...
```

The crucial property:

> **You don't normally decrypt a hash.**

There is no:

```text
SHA-256 key
```

and no:

```text
decrypt(hash)
```

That's not how cryptographic hashing works.

---

## 5. Why do we need hashing?

One major web-development use case:

### Password storage

Suppose a user chooses:

```text
MyPassword123
```

You should **not** store:

```text
password = "MyPassword123"
```

And generally, you should not store passwords using ordinary reversible encryption either.

Instead:

```text
Password
    ↓
Password hashing algorithm
    ↓
Password hash
    ↓
Database
```

Then during login:

```text
User enters password
        ↓
Password verification
        ↓
Compare against stored password hash
        ↓
Match?
        ↓
Login
```

For passwords, use dedicated password-hashing algorithms such as:

**Argon2id, bcrypt, scrypt, PBKDF2**

—not plain SHA-256.

---

## 6. Why not SHA-256 for passwords?

This is an important security lesson.

SHA-256 is designed to be **fast**.

That's great for many integrity-related tasks.

But password attackers also benefit from speed.

Imagine an attacker has obtained:

```text
database.sql
```

containing password hashes.

They can attempt:

```text
password1 → SHA-256
password2 → SHA-256
password3 → SHA-256
...
```

Very quickly.

Password hashing algorithms deliberately make guessing **expensive** through techniques such as configurable work factors and memory requirements.

That's why:

```text
SHA-256
    ≠
Password hashing
```

---

## 7. Encoding 📦

Now the third concept.

Encoding is **not primarily a security mechanism**.

Its purpose is:

> **Represent data in a format suitable for a particular system or protocol.**

A classic example:

### Base64

Suppose you have binary data.

You encode it:

```text
Binary data
    ↓
 Base64
    ↓
ASCII representation
```

You can then decode it:

```text
Base64
  ↓
Decode
  ↓
Original binary data
```

No secret key.

No security.

No password.

---

## 8. Base64 is NOT encryption

This is one of the most common beginner mistakes.

Someone sees:

```text
SGVsbG8gV29ybGQ=
```

and thinks:

> "Encrypted!"

No.

That's Base64 encoding.

Anyone can decode it.

```text
SGVsbG8gV29ybGQ=
          ↓
       Base64
          ↓
Hello World
```

So:

> **Obfuscation ≠ encryption.**

---

## 9. Compare all three

|                           | Encryption | Hashing                    | Encoding       |
| ------------------------- | ---------- | -------------------------- | -------------- |
| Purpose                   | Secrecy    | Fingerprint / verification | Representation |
| Reversible?               | ✅ With key | ❌ Normally one-way         | ✅              |
| Uses secret key?          | Usually    | No                         | No             |
| Protects confidentiality? | ✅          | Not by itself              | ❌              |
| Example                   | AES        | SHA-256                    | Base64         |
| Password storage?         | ❌          | ✅ Argon2/bcrypt/etc.       | ❌              |
| HTTPS?                    | ✅          | Sometimes internally       | Sometimes      |

---

## 10. Let's map this to your web stack

Suppose you build:

```text
React
   ↓
HTTPS
   ↓
Go / Node / PHP API
   ↓
MySQL
```

Different mechanisms appear at different places.

#### HTTPS

```text
Browser
   │
   │ 🔐 TLS
   ↓
Backend
```

**Encryption** protects data in transit.

---

#### Password

```text
User password
      ↓
Argon2id / bcrypt
      ↓
Database
```

**Hashing** protects password storage.

---

#### JSON / API data

```text
JavaScript object
      ↓
JSON.stringify()
      ↓
JSON
      ↓
HTTP
```

That's **serialization/representation**, not encryption.

---

#### Base64

You may encounter:

```text
Authorization: Basic ...
```

The credentials in HTTP Basic Authentication are Base64-encoded.

That does **not** make them secret.

Security comes from using **TLS/HTTPS** around the communication.

---

## 11. JWT will test your understanding

Soon you'll encounter something like:

```text
eyJhbGciOiJIUzI1NiIs...
```

Beginners often say:

> "JWT is encrypted."

Usually, **no**.

A standard signed JWT is generally:

```text
HEADER.PAYLOAD.SIGNATURE
```

The header and payload are Base64URL-encoded.

The signature provides authenticity/integrity.

Conceptually:

```text
JWT
 │
 ├── Header       → encoded
 ├── Payload      → encoded
 └── Signature    → cryptographic protection
```

So don't put sensitive secrets into a normal JWT payload merely because it "looks encrypted."

We'll cover JWT properly later.

---

## 12. A better mental model

Instead of remembering definitions, ask:

#### "What problem am I solving?"

```text
I need to hide the data.
        ↓
   ENCRYPTION


I need to verify/securely store something
        ↓
     HASHING


I need to represent data in another format.
        ↓
     ENCODING
```

That's the mental model.

---

## 13. Connect it to CIA

Now our previous chapters start connecting beautifully.

```text
                    DATA
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
     AT REST       IN USE      IN TRANSIT
        │            │            │
        └────────────┼────────────┘
                     ↓
                    CIA
               ┌─────┼─────┐
               ↓     ↓     ↓
              CONF  INT   AVAIL
               │     │
               ↓     ↓
          Encryption  Hashing
             TLS      Signatures
```

But be careful:

**Encryption ≠ integrity automatically.**

Modern authenticated encryption modes such as **AES-GCM** provide confidentiality *and* integrity protection.

This distinction becomes important when we study TLS.

---

## 🧠 Your security map so far

You now have:

```text
CHAPTER 1
CIA TRIAD
│
├── Confidentiality
├── Integrity
└── Availability
        │
        ↓
CHAPTER 2
AUTHENTICATION + AUTHORIZATION
        │
        ↓
CHAPTER 3
CRYPTOGRAPHIC BASICS
│
├── Encryption
│    ├── Symmetric
│    └── Asymmetric
│
├── Hashing
│    ├── Cryptographic hashes
│    └── Password hashing
│
└── Encoding
     └── Base64 / Base64URL
```

### The next chapter should be:

**Chapter 4 — Symmetric vs Asymmetric Cryptography**

We'll answer the question that naturally comes next:

> **If encryption requires a key, how does a browser securely communicate with a server when they've never shared a secret key before?**

That question leads directly into **public/private keys → key exchange → certificates → TLS → HTTPS**.

And **that's where your networking knowledge and security knowledge finally collide.**
