---
description: The order to learn web security in — CIA triad, auth, cryptography, TLS, passwords, access control — and why that sequence beats memorising algorithms.
---

# Roadmap

!!! question "The question"
    I've got the three states of data down. What should I learn next in security, and in
    what order — so I'm not just memorizing AES, RSA, JWT, and TLS without understanding
    why each one exists?

Continuing from the three states of data into security, the next concept to learn is probably:

## 🔐 CIA Triad

It gives you the **security goals**; the three data states tell you **where the data is**.

```text
                 INFORMATION SECURITY
                         │
              ┌──────────┼──────────┐
              ↓          ↓          ↓
        CONFIDENTIALITY INTEGRITY AVAILABILITY
              │          │          │
           Who can     Has data    Can I
           see it?     changed?    access it?
```

Then connect it to the three data states:

| Data state     | Main security mechanisms                          |
| -------------- | ------------------------------------------------- |
| **At Rest**    | Encryption, access control, backups, integrity    |
| **In Use**     | Process isolation, permissions, memory protection |
| **In Transit** | TLS, certificates, encryption, authentication     |

### Then I'd take you through this sequence

**1. CIA Triad** ← **next**

↓

**2. Authentication vs Authorization**
Who are you? → What are you allowed to do?

↓

**3. Encryption vs Hashing vs Encoding**
This is a *very important* distinction.

↓

**4. Symmetric vs Asymmetric Encryption**
AES, RSA, ECC, public/private keys.

↓

**5. TLS / HTTPS**
What actually happens when your browser talks to a server?

↓

**6. Password Security**
Hashing, salt, bcrypt/Argon2, password storage.

↓

**7. Secrets & Key Management**
API keys, environment variables, secret managers, key rotation.

↓

**8. Data Integrity**
Hashes, checksums, HMAC, digital signatures.

↓

**9. Access Control Models**
ACL → RBAC → ABAC → least privilege.

↓

**10. Backup Security**
Encryption, retention, versioning, immutable backups, 3-2-1 strategy, ransomware considerations.

---

### And there's one particularly important realization for you

You've already encountered **ACL, TLS, IPv6, routing, firewalls, authentication, databases, backups, etc.**

But you have often learned them as **individual technologies**.

Security becomes much clearer when you organize them like this:

```text
                    DATA
                      │
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
     AT REST        IN USE       IN TRANSIT
        │             │             │
        └─────────────┼─────────────┘
                      ↓
                 SECURITY
                      │
             ┌────────┼────────┐
             ↓        ↓        ↓
            CIA      ACCESS   CRYPTO
             │        │        │
       Confidential  AuthN    Encrypt
       Integrity     AuthZ    Hash
       Availability  ACL      Sign
                              Keys
```

**That is the mental map I'd recommend you build next.**

And I would **not jump straight into cryptography**. Learn **CIA Triad → Authentication/Authorization → Encryption/Hashing/Encoding** first. Otherwise you'll end up memorizing AES, RSA, SHA-256, JWT, TLS, etc. without understanding *why each exists*.
