---
description: Creating, storing, using, rotating and destroying secrets and keys — why .env is not a security system, secret managers, least privilege, and leak response.
---

# Chapter 10 — Secrets, Keys & Key Management

This chapter is where cryptography meets **real production engineering**.

You already learned encryption:

> **Encryption is only as secure as the key.**

A perfect encryption algorithm with a leaked key is basically useless.

So the real question becomes:

> **How do we create, store, use, rotate, and destroy secrets and cryptographic keys safely?**

---

# 1. What Is a Secret?

A secret is sensitive information that should not be publicly exposed.

Examples:

```text
DATABASE_PASSWORD
API_KEY
JWT_SIGNING_SECRET
ENCRYPTION_KEY
OAuth client secret
TLS private key
Cloud credentials
```

Think of it as:

```text
              SECRET
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   Database    API       Crypto
   password    key        key
```

But there's an important distinction.

A **password** is usually something a human uses to authenticate.

A **secret/key** may be used by software to authenticate, authorize, sign, or encrypt.

---

# 2. The Classic Developer Mistake

Imagine writing:

```text id="2f7x9k"
const DB_PASSWORD = "MySuperSecretPassword";
```

Then:

```text id="m8c3qp"
git add .
git commit
git push
```

Now the secret is in your Git repository.

Even if the repository is private, this is still bad practice.

And if the repository becomes public:

💀

The credential may already be compromised.

---

# 3. Why `.env` Exists

Instead of putting configuration directly into your source code:

```text id="7h1m4z"
DATABASE_HOST=...
DATABASE_USER=...
DATABASE_PASSWORD=...
JWT_SECRET=...
```

Your application reads environment variables.

Conceptually:

```text id="p5r8nx"
Operating Environment
        │
        │ environment variables
        ▼
     Application
```

Your source code can say:

```text id="d3k6wv"
read DATABASE_PASSWORD
```

without containing the actual password.

---

# 4. But `.env` Is NOT a Security System

This is important.

Developers sometimes think:

> "I use `.env`, therefore my secrets are secure."

No.

`.env` is primarily a **configuration mechanism**.

If you do:

```text id="x8q2mj"
.env
```

and then accidentally:

```text id="n4v7cs"
git add .env
```

your secret is still leaked.

So you generally put:

```text id="y5k9bd"
.env
```

in:

```text id="s2h6px"
.gitignore
```

For production, use your hosting provider's secret/environment-variable system or a dedicated secret manager where appropriate.

---

# 5. Development vs Production

### Development

You might have:

```text id="q7w2kc"
.env
```

```text
DB_HOST=localhost
DB_PASSWORD=...
API_KEY=...
```

### Production

Your deployment environment might inject:

```text id="f8n3mv"
DATABASE_URL
JWT_SECRET
API_KEY
```

without putting them into your Git repository.

Conceptually:

```text id="v9c1zs"
                 Git
                  │
                  │ application code
                  ▼
             Deployment
                  ▲
                  │
            Secret Store
                  │
                  ▼
             Environment
```

---

# 6. Keys Are Not All the Same

This is a common source of confusion.

### Authentication secret

Used to prove something knows a secret.

Example:

```text id="a3y8qf"
API_SECRET
```

### Signing key

Used to create/verifiy digital signatures.

Example:

```text id="r4m7tx"
JWT signing key
```

### Encryption key

Used to encrypt/decrypt data.

Example:

```text id="c9k2wd"
AES key
```

### TLS private key

Used as part of the server's cryptographic identity.

Example:

```text id="h6p1zs"
server_private_key
```

They shouldn't automatically be treated as interchangeable.

---

# 7. Never Confuse Public and Private Keys

With asymmetric cryptography:

```text id="j8v4qp"
        KEY PAIR

Public Key              Private Key
    │                        │
    │ can be shared           │ MUST remain secret
    ▼                        ▼
Everyone                  Owner/server
```

For example, a TLS certificate contains public information.

The corresponding private key is sensitive.

If an attacker obtains the private key, the security assumptions around that cryptographic identity can be broken.

---

# 8. Key Management Is More Than Storage

Suppose you have an encryption key:

```text id="n2x6kc"
KEY = ABC123...
```

Where do you store it?

That's only question #1.

Real key management asks:

```text id="u7p3mv"
How is the key generated?
        ↓
Where is it stored?
        ↓
Who can access it?
        ↓
How is it used?
        ↓
How is access audited?
        ↓
How is it rotated?
        ↓
What happens if it leaks?
        ↓
How is it destroyed?
```

That's **Key Management**.

---

# 9. Key Rotation

Suppose your application uses:

```text id="f5k9yr"
KEY_V1
```

Months later, you want to replace it:

```text id="s8m2dx"
KEY_V1 → KEY_V2
```

That's key rotation.

Why?

Because you want to limit the lifetime of a cryptographic key and respond to possible compromise or operational requirements.

But rotation creates another problem:

> **What about data encrypted using the old key?**

You may need a strategy such as:

```text id="q6z3pv"
Decrypt with V1
      ↓
Re-encrypt with V2
```

or support multiple active key versions during migration.

This is why key management becomes an engineering problem.

---

# 10. Encryption Key ≠ Password Hash

This distinction is extremely important.

Suppose:

```text id="t1h8vx"
User password
      ↓
Argon2id
      ↓
Password hash
```

You don't need an encryption key to reverse it.

But:

```text id="b7n4qm"
Sensitive database field
      ↓
AES-GCM + encryption key
      ↓
Ciphertext
```

The application needs access to the key to decrypt it.

So:

```text id="y3p6ck"
Passwords → password hashing

Recoverable sensitive data → encryption
```

Don't invent your own hybrid scheme.

---

# 11. Where Should Production Secrets Live?

Small deployments might use:

```text id="x4m8pz"
Hosting platform
    ↓
Environment variables
```

Larger systems may use dedicated secret-management systems.

Conceptually:

```text id="v5k2dn"
Application
    │
    │ authenticated request
    ▼
Secret Manager
    │
    ▼
Required secret
```

Examples of the category include:

* cloud secret managers
* Vault-style systems
* managed key-management services

The point isn't the brand.

The point is:

> **Don't make your Git repository your secret vault.**

---

# 12. Least Privilege

Suppose your application only needs to read a database.

Why give it:

```text id="q9w5rz"
DELETE
DROP DATABASE
CREATE USER
SUPERUSER
```

permissions?

Don't.

Give the application the minimum privileges required.

```text id="m2c7hx"
Application
    ↓
Limited DB account
    ↓
Only required operations
```

This is **Least Privilege**.

If the application's credentials are compromised, the blast radius is smaller.

---

# 13. Your Cloud-Kitchen Application

Imagine your production architecture:

```text id="j7p3bx"
                    Internet
                       │
                       ▼
                Reverse Proxy
                       │
                       ▼
                  Backend API
                    /     \
                   /       \
                  ▼         ▼
              Database     Redis
                  │
                  ▼
             Secret Store
```

The backend might need:

```text id="a8v4qm"
DATABASE_URL
REDIS_URL
JWT_SIGNING_KEY
PAYMENT_API_KEY
```

But:

```text id="r6k2cz"
Browser
```

should **never receive your server-side secrets**.

This sounds obvious, but exposing environment variables through frontend builds is a common mistake.

---

# 14. Frontend Environment Variables Are Not Automatically Secret

Suppose you write:

```text id="c5m9vx"
VITE_API_KEY=secret123
```

and your frontend bundler includes it in JavaScript.

Anyone can inspect the downloaded JavaScript.

Therefore:

> **Anything shipped to the browser should be considered public.**

Even if the variable is called:

```text id="s7h3nd"
SECRET_KEY
```

the name doesn't make it secret.

The browser belongs to the user.

---

# 15. API Keys Need Scope Too

Suppose a third-party service gives you an API key.

Don't assume:

```text id="p8r4mz"
API key = unlimited access
```

Good systems often support restrictions such as:

```text id="y2n6vc"
Allowed API
Allowed operations
Allowed origins/IPs
Expiration
Rate limits
```

Again:

> **Reduce the blast radius.**

---

# 16. What If a Secret Leaks?

This is where real security engineering differs from:

> "Just keep the password safe."

Assume eventually something will leak.

Your response should be:

```text id="w3k7px"
Detect
  ↓
Revoke
  ↓
Rotate
  ↓
Investigate
  ↓
Assess impact
  ↓
Restore secure configuration
```

For example:

```text id="q5m8nd"
GitHub secret leak
      ↓
Revoke credential
      ↓
Generate replacement
      ↓
Deploy new credential
      ↓
Audit usage
```

**Deleting the secret from the latest commit isn't enough.**

Treat the exposed credential as compromised.

---

# 17. Security Principle: Assume Breach

This is a powerful mindset.

Don't design:

> "Nobody will ever get inside."

Design:

> **"If this credential leaks, how much damage can it cause?"**

That leads naturally to:

* least privilege
* short-lived credentials
* rotation
* segmentation
* monitoring
* auditing
* limited permissions

This is much stronger engineering.

---

# 18. Connect It to CIA

### Confidentiality

Secrets and keys must remain confidential.

### Integrity

Signing keys protect the integrity/authenticity of signed data.

### Availability

Proper key-management and recovery procedures prevent a lost key from making critical encrypted data permanently inaccessible.

That last point is easy to overlook.

**Losing an encryption key can be almost as catastrophic as leaking one.**

Leaked key → attacker can decrypt.

Lost key → **you may not be able to decrypt your own data.**

---

# 19. The Mental Model

Don't think:

```text id="g4r9tz"
"Where do I put my API key?"
```

Think:

```text id="b2x7mc"
            SECRET
               │
       ┌───────┴────────┐
       ▼                ▼
   Who needs it?    How long?
       │                │
       ▼                ▼
 Least privilege    Rotation
       │                │
       └───────┬────────┘
               ▼
         Secure storage
               │
               ▼
            Monitoring
               │
               ▼
         Incident response
```

That's **secret management**, not simply `.env`.

---

# The bigger security architecture so far

You've now covered:

```text id="s9p3kw"
                    SECURITY
                       │
 ┌─────────────────────┼──────────────────────┐
 │                     │                      │
Identity             Browser                Data
 │                     │                      │
 ├─ Passwords          ├─ SOP                 ├─ Encryption
 ├─ Authentication     ├─ CORS               ├─ Hashing
 ├─ Sessions           ├─ CSRF               ├─ Integrity
 └─ Authorization      └─ XSS                └─ Secrets/Keys
```

And we're approaching a much more complete backend-security model.

---

## Next — Chapter 11: Access Control & Privilege Escalation

This is where we'll go deeper than simply:

```text
Owner
Manager
Staff
```

We'll examine:

* **RBAC**
* **ABAC**
* horizontal privilege escalation
* vertical privilege escalation
* BOLA/IDOR
* object-level authorization
* multi-tenant security
* why `/users/123` is a security boundary
* how to design authorization so one business/customer cannot access another's data

This chapter is particularly relevant to your **generic multi-business cloud-kitchen application**, because multi-tenancy introduces a very dangerous question:

> **"What stops Business A from accessing Business B's data?"**

