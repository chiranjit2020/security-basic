---
description: How servers store credentials safely — why hashing beats encryption, what salt does, bcrypt and Argon2, and secure registration, login and reset flows.
---

# Chapter 6 — Password Security & Credential Storage

This is where security becomes **very practical for a backend developer**.

You already know authentication. Now the question is:

> **Where and how does the server store the thing that proves a user's identity?**

---

## 1. The Worst Possible Design

Suppose a user registers:

```text
Email: user@example.com
Password: MySecret123
```

A bad database stores:

| id | email                                       | password    |
| -: | ------------------------------------------- | ----------- |
|  1 | [user@example.com](mailto:user@example.com) | MySecret123 |

If your database is leaked:

```text
Attacker
   ↓
Database breach
   ↓
Passwords exposed
   ↓
User accounts compromised
```

And the damage can extend beyond your application because people often reuse passwords.

**Never store plaintext passwords.**

---

# 2. "Why not encrypt the password?"

This is an important distinction.

Encryption is reversible:

```text
password
   ↓
encrypt + key
   ↓
ciphertext
   ↓
decrypt + key
   ↓
password
```

But your application doesn't actually need to know the user's original password.

During login, it only needs to answer:

> **"Does the password they just entered match the password they originally registered?"**

Therefore, we use **password hashing**.

```text
Registration:

password
   ↓
password-hashing algorithm
   ↓
password hash
   ↓
database
```

Later:

```text
Login password
      ↓
password verification
      ↓
matches stored hash?
      ↓
YES → authenticated
NO  → rejected
```

The server doesn't need to recover the original password.

---

# 3. But Isn't Hashing One-Way?

Yes.

Conceptually:

```text
password ──→ hash
```

You don't do:

```text
hash ──→ password
```

That's precisely the point.

But there's a problem.

Suppose someone uses:

```text
password = password123
```

An attacker can calculate hashes of common passwords.

```text
password123 → hash A
qwerty       → hash B
123456       → hash C
admin123     → hash D
...
```

Then compare them against stolen hashes.

This is why **ordinary fast hashing is not enough for passwords.**

---

# 4. SHA-256 Is Not a Password Hashing Strategy

You may already know:

```text
SHA-256("hello")
```

produces a hash.

So why not:

```text
SHA-256(password)
```

?

Because SHA-256 is designed to be **fast**.

That's excellent for things like:

* checksums
* fingerprints
* integrity operations
* cryptographic constructions

But password attackers also want speed.

Imagine an attacker has a stolen database and can test billions of guesses quickly.

A password-hashing algorithm deliberately makes each guess expensive.

That's the fundamental idea.

> **For passwords, you want attackers to pay computational/memory cost for every guess.**

---

# 5. Salt — The Simple but Important Idea

Consider two users:

```text
Alice → password123
Bob   → password123
```

Without salts, the same password produces the same hash.

```text
Alice → HASH(password123)
Bob   → HASH(password123)
```

That's undesirable.

Instead, a unique random **salt** is generated for each password.

```text
Alice:
password123 + random salt A
          ↓
       password hash A

Bob:
password123 + random salt B
          ↓
       password hash B
```

So even though they chose the same password, their stored hashes differ.

### Salt is not a secret.

It can be stored alongside the password hash.

Its purpose is to prevent attackers from efficiently reusing precomputed results across users and passwords.

---

# 6. Modern Password Hashing

Common password-hashing algorithms include:

* **Argon2id**
* bcrypt
* scrypt
* PBKDF2

For new systems, **Argon2id is generally an excellent choice** when your platform supports it.

Notice the difference:

```text
SHA-256
    ↓
Fast general-purpose hash
```

versus:

```text
Argon2id
    ↓
Password hashing function
    ↓
Designed to make guessing expensive
```

---

# 7. What Actually Goes Into Your Database?

You might see something resembling:

```text
$argon2id$v=19$m=65536,t=3,p=4$...
```

You don't need to manually create this structure.

A proper password-hashing library/framework handles:

* algorithm
* salt
* cost parameters
* hash generation
* verification

Your database stores the resulting password hash.

Conceptually:

```text
users
--------------------------------
id
email
password_hash
created_at
```

Not:

```text
password
```

---

# 8. Registration Flow

Imagine your cloud-kitchen application.

A restaurant owner registers:

```text
POST /register

email = owner@example.com
password = MyStrongPassword
```

Backend:

```text
             Registration
                  │
                  ▼
          Validate input
                  │
                  ▼
       Hash password (Argon2id)
                  │
                  ▼
        Store password_hash
                  │
                  ▼
             Database
```

The plaintext password should **not** be stored.

Ideally, after hashing, your application doesn't retain it unnecessarily.

---

# 9. Login Flow

User enters:

```text
email = owner@example.com
password = MyStrongPassword
```

Backend:

```text
POST /login
       │
       ▼
Find user by email
       │
       ▼
Retrieve password_hash
       │
       ▼
Verify supplied password
against stored hash
       │
   ┌───┴───┐
   │       │
 MATCH   NO MATCH
   │       │
   ▼       ▼
Login    Reject
```

The backend does **not** decrypt the stored hash.

It asks the password-hashing library:

> "Does this supplied password correspond to this stored hash?"

---

# 10. Password Reset Is a Different Problem

Suppose the user clicks:

> **Forgot password?**

You should **not** email them:

> "Your password is `MySecret123`."

That would imply you can retrieve their original password—which is exactly what we don't want.

Instead:

```text
Forgot password
       ↓
Generate random reset token
       ↓
Send reset link
       ↓
User creates new password
       ↓
Hash new password
       ↓
Replace old password hash
```

The reset token itself should also be designed carefully: short-lived, single-use, and stored/handled in a way that limits damage if it leaks.

---

# 11. Passwords vs API Keys vs Secrets

This distinction becomes important as a backend engineer.

### User password

Usually:

```text
Password
   ↓
Password hashing
   ↓
Hash stored
```

### Application secret

For example:

```text
JWT signing secret
Database credential
Third-party API secret
```

These usually need to be **retrievable by the application**, so hashing them isn't generally the same solution.

They belong in:

```text
Environment variables
Secret manager
Secure configuration
```

rather than:

```text
GitHub repository
```

So:

> **Passwords → usually hash them.**
> **Secrets the application must recover → protect/encrypt/manage them securely.**

---

# 12. A Huge Mistake: Committing Secrets to Git

Never do this:

```text
const DB_PASSWORD = "super-secret-password";
```

and push it to GitHub.

Even if you later delete the line, it may remain in Git history.

Instead:

```text
.env
```

```text
DB_PASSWORD=...
JWT_SECRET=...
API_KEY=...
```

and keep `.env` out of version control.

For production, preferably use the hosting platform's secret/environment-variable system or a dedicated secrets manager.

---

# 13. How This Connects to CIA

Password security primarily protects:

### Confidentiality

An attacker shouldn't obtain users' usable credentials from a database leak.

### Integrity

An attacker who obtains credentials may be able to modify data or accounts.

### Availability

Account compromise can potentially lead to destructive actions, though availability isn't the primary password-security goal.

So one security mechanism can indirectly affect multiple CIA properties.

---

# 14. The Backend Security Mental Model

For every authentication system, think:

```text
                USER
                 │
                 ▼
          ┌─────────────┐
          │ Credentials │
          └──────┬──────┘
                 │
                 ▼
        ┌──────────────────┐
        │ Password hashing │
        └────────┬─────────┘
                 │
                 ▼
             DATABASE
                 │
                 │
       ┌─────────▼─────────┐
       │ Password verification│
       └─────────┬─────────┘
                 │
            Match / Reject
```

And after successful authentication:

```text
Authentication
      ↓
Authorization
      ↓
Validation
      ↓
Business Logic
      ↓
Database
```

That chain is worth memorizing—not as syntax, but as a **security boundary model**.

---

# The most important takeaway

Don't think:

> "How do I hide the password?"

Think:

> **"How can my system verify the password without ever needing to know the original password again?"**

That's the reason password hashing exists.

And this leads naturally to the next problem:

**If the password is correct, how does the server remember that the user is logged in?**

That's **Chapter 7 — Sessions, Cookies, Tokens & JWTs**.

