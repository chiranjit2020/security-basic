# Chapter 5 — TLS, HTTPS & Digital Certificates

!!! question "The question"
    When I type `https://example.com` into my browser, exactly how does my browser know
    it is really talking to `example.com` and not an attacker pretending to be the server?

This is where the previous chapters finally come together.

You already know:

* **CIA** → what security is trying to protect
* **Authentication vs Authorization** → who you are and what you're allowed to do
* **Encryption vs Hashing vs Encoding** → different cryptographic purposes
* **Symmetric vs Asymmetric cryptography** → different ways cryptography handles keys

Now let's answer:

> **What actually happens when your browser connects to `https://example.com`?**

---

## 1. First: HTTP vs HTTPS

HTTP by itself is an application-layer protocol for transferring web messages.

Conceptually:

```text
Browser
   │
   │ HTTP
   ↓
Server
```

If the connection isn't otherwise protected, an attacker positioned on the network may be able to observe or manipulate traffic.

HTTPS is essentially:

```text
HTTP
  +
TLS
```

So:

```text
Browser
   │
   │ HTTPS
   ↓
   TLS
   ↓
  HTTP
   ↓
Server
```

**TLS provides the security layer. HTTP provides the web communication.**

---

## 2. What does TLS need to accomplish?

When your browser connects to a server, TLS needs to establish several things.

#### ① Confidentiality

> Can someone listening to the network read my data?

**No.**

#### ② Integrity

> Can someone modify the data without detection?

**No.**

#### ③ Authentication

> Am I really communicating with the intended server?

**The server proves its identity using a certificate and cryptographic mechanisms.**

So TLS connects directly to our CIA model:

```text
                 TLS
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
 Confidentiality Integrity Authentication
        │         │         │
     Encryption  Detect   Certificate
                 changes  + signatures
```

---

## 3. The problem: Anyone can claim to be Google

Imagine you visit:

```text
https://example.com
```

But an attacker says:

```text
"Hey! I'm example.com."
```

Your browser needs a way to determine:

> **Are you actually example.com?**

This is where **digital certificates** enter the picture.

---

## 4. Digital certificates

A TLS certificate essentially binds an identity such as a domain name to a **public key**, along with information about who issued and validated that certificate.

Conceptually:

```text
example.com
     │
     ↓
Certificate
     │
     ├── Domain identity
     ├── Public key
     ├── Issuer
     ├── Validity information
     └── Digital signature
```

The certificate is digitally signed by a **Certificate Authority (CA)**.

---

## 5. Certificate Authority

Think of a CA as part of a trust system.

Instead of your browser blindly believing:

```text
Server says:
"I'm example.com."
```

it can reason more like:

```text
Server
  ↓
Certificate
  ↓
Signed by trusted CA?
  ↓
Certificate valid?
  ↓
Domain matches?
  ↓
Cryptographic checks pass?
  ↓
Trust the server identity
```

Your operating system/browser comes with a collection of trusted root certificates.

That's the foundation of the **Web PKI (Public Key Infrastructure)**.

---

## 6. The certificate doesn't contain the website's password

This is another common misconception.

A certificate does **not** give the browser some secret server password.

Instead, it contains information including the server's **public key** and a CA's signature over the certificate data.

The corresponding **private key** stays with the server.

```text
SERVER
 ├── Public key  → certificate → can be shared
 └── Private key → 🔐 secret
```

Never expose the private key.

---

## 7. Now let's actually connect

You type:

```text
https://example.com
```

There are several layers involved.

A simplified version:

```text
Browser
   ↓
DNS
   ↓
IP address
   ↓
TCP connection
   ↓
TLS handshake
   ↓
HTTP request
   ↓
Server
```

Notice how your previous networking knowledge fits here.

---

## 8. Step 1 — DNS

Your browser needs to find the server's IP address.

Conceptually:

```text
example.com
     ↓
    DNS
     ↓
93.184.x.x
```

DNS answers:

> "Which IP address should I connect to?"

DNS itself isn't what encrypts your HTTP traffic.

That's a different layer.

---

## 9. Step 2 — TCP

Depending on the HTTP version and transport being used, the connection may use TCP or QUIC.

For the classic HTTP/1.1 or HTTP/2 case:

```text
Browser
   ↓
TCP connection
   ↓
Server
```

TCP gives you a reliable transport.

But TCP doesn't mean:

> "The connection is encrypted."

That's why we need TLS.

```text
TCP ≠ Encryption
```

---

## 10. Step 3 — TLS handshake

Now things get interesting.

The browser and server negotiate cryptographic parameters and establish shared secrets.

A simplified view:

```text
Browser                         Server
   │                               │
   │──── ClientHello ─────────────→│
   │                               │
   │←── ServerHello ───────────────│
   │                               │
   │←── Certificate ───────────────│
   │                               │
   │──── Key exchange ─────────────│
   │                               │
   │   Shared secret established   │
   │                               │
   │════════ encrypted HTTP ═══════│
```

This is intentionally simplified.

Modern TLS 1.3 has a very specific handshake structure, and the cryptography involved is more sophisticated than the old "server sends its public key and browser encrypts the AES key" explanation.

---

## 11. Where asymmetric cryptography fits

Remember Chapter 4?

You learned:

```text
Public key
Private key
```

TLS uses asymmetric cryptography-related mechanisms for things such as:

* authenticating the server
* digital signatures
* establishing cryptographic secrets

But it doesn't use public-key cryptography to encrypt every HTTP packet.

Why?

Because symmetric encryption is much more efficient.

So after the handshake:

```text
                 TLS
                  │
        ┌─────────┴─────────┐
        ↓                   ↓
   Authentication      Key establishment
        │                   │
 Certificate/signature      ↓
                    Shared symmetric keys
                            │
                            ↓
                    Encrypt application data
```

---

## 12. The beautiful part: Hybrid cryptography

This is the architecture you should remember.

```text
        ASYMMETRIC / KEY EXCHANGE
                  │
                  ↓
       Establish shared secret
                  │
                  ↓
          SYMMETRIC CRYPTO
                  │
                  ↓
      Encrypt actual application data
```

So your browser doesn't choose:

> "Should I use RSA or AES?"

The TLS protocol combines different cryptographic mechanisms for different jobs.

---

## 13. What does the attacker see?

Suppose you send:

```http
POST /login
username=chiranjit
password=MyPassword
```

Without TLS, someone capable of observing the traffic could potentially see the request contents.

With HTTPS, the application data is protected inside the TLS connection.

Conceptually:

```text
Browser
   │
   │ plaintext
   ↓
TLS encryption
   │
   ↓
ciphertext
   │
   │ 👀 attacker sees traffic
   │
   ↓
Server
   │
TLS decryption
   ↓
plaintext
```

The attacker may still see some metadata depending on the protocol, network setup, and deployment—but not simply the plaintext HTTP contents protected by TLS.

---

## 14. What if the attacker modifies the request?

Suppose you send:

```text
amount = ₹500
```

and an attacker tries to change it to:

```text
amount = ₹50,000
```

TLS provides integrity protection for the protected connection.

The modified ciphertext should fail authentication checks.

Conceptually:

```text
Browser
   ↓
TLS-protected message
   ↓
👤 Attacker modifies it
   ↓
Server
   ↓
❌ Authentication/integrity check fails
```

So TLS isn't merely:

> "Encryption."

It's providing **authenticated, integrity-protected communication**.

---

## 15. The certificate's real job

This is perhaps the most important thing to understand.

Encryption alone isn't enough.

Imagine an attacker creates:

```text
evil-example.com
```

and gives you a perfectly valid public key.

You could establish an encrypted connection with them.

The connection would be:

```text
Encrypted ✓
```

but:

```text
You're talking to the wrong server ❌
```

Therefore TLS needs **authentication** as well as encryption.

That's why certificates matter.

```text
          CERTIFICATE
               │
               ↓
       "This public key
        belongs to
        example.com"
               │
               ↓
       Trusted CA signature
               │
               ↓
       Browser verifies
```

---

## 16. Certificate ≠ encryption

Another important distinction:

**Certificate**

→ helps establish/authenticate identity and provides a public key.

**TLS**

→ protocol that establishes a secure connection.

**Encryption algorithm**

→ cryptographic mechanism that protects data.

They're related, but they're not the same thing.

```text
Certificate
     ↓
Identity + public key

TLS
     ↓
Secure communication protocol

AES/ChaCha20
     ↓
Symmetric encryption
```

---

## 17. Where does hashing fit?

Now bring Chapter 3 back.

TLS also uses cryptographic hashes and related constructions.

For example, TLS uses cryptographic hashing in mechanisms involved in:

* transcript integrity
* key derivation
* authentication
* digital signatures and certificates

So you can see how the concepts we've learned aren't isolated.

```text
              TLS
               │
     ┌─────────┼─────────┐
     ↓         ↓         ↓
Certificates  Hashing  Encryption
     │                    │
Public/private       Symmetric crypto
key mechanisms            │
     │                    │
     └─────────┬──────────┘
               ↓
        Secure connection
```

---

## 18. Now map this to your backend

Suppose you deploy your Go/Node/PHP API:

```text
Frontend
   │
   │ HTTPS
   ↓
Reverse Proxy / Load Balancer
   │
   ↓
Backend
   │
   ↓
Database
```

A common deployment might terminate TLS at a reverse proxy/load balancer:

```text
Browser
   │
   │ 🔐 HTTPS
   ↓
Nginx / Load Balancer
   │
   │ internal connection
   ↓
Backend
```

That means:

> **HTTPS encryption on the browser-to-proxy connection does not automatically mean every internal hop is encrypted.**

This is a very important production-security concept.

For sensitive systems, you may also protect internal traffic:

```text
Browser
   │ HTTPS
   ↓
Load Balancer
   │ HTTPS / mTLS
   ↓
API
   │ TLS
   ↓
Database
```

This is part of thinking about **data in transit across the entire architecture**, not just "turning on HTTPS."

---

## 19. Connect everything we've learned

You started with:

#### Chapter 1

```text
CIA
├── Confidentiality
├── Integrity
└── Availability
```

Then:

#### Chapter 2

```text
Authentication
Authorization
```

Then:

#### Chapter 3

```text
Encryption
Hashing
Encoding
```

Then:

#### Chapter 4

```text
Symmetric
Asymmetric
```

Now:

#### Chapter 5

```text
TLS
│
├── Certificates
├── Authentication
├── Key establishment
├── Symmetric encryption
└── Integrity protection
```

And suddenly:

```text
                 HTTPS
                   │
                  TLS
                   │
       ┌───────────┼───────────┐
       ↓           ↓           ↓
 Authentication Confidentiality Integrity
       │           │           │
 Certificates   Encryption   Authentication
       │           │           │
       └───────────┼───────────┘
                   ↓
             Secure HTTP
```

---

## 🧠 The one thing I want you to remember

Don't think:

> **HTTPS = encryption**

Think:

> **HTTPS = HTTP carried through TLS, where TLS establishes an authenticated and cryptographically protected communication channel.**

That one mental model will save you from a *lot* of confusion later.

---

## Your next chapter

The natural next step is:

**Chapter 6 — Password Security & Credential Storage**

We'll take this:

```text
User
 ↓
Password
 ↓
Login
 ↓
Database
```

and answer:

* Why passwords should **not** be encrypted like ordinary data
* What **salt** actually does
* Why SHA-256 is not a password-storage algorithm
* bcrypt vs Argon2
* What happens when a database is leaked
* Password verification
* Password reset tokens
* API keys and secrets
* How authentication connects to your PHP/Node/Go applications

That chapter will turn the cryptography concepts into **actual backend security engineering**.
