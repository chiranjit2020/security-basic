---
description: How a stateless server recognises a logged-in user — sessions, cookies and their security attributes, JWTs, access vs refresh tokens, and session theft.
---

# Chapter 7 — Sessions, Cookies, Tokens & JWTs

This chapter answers a very practical question:

> **After the user successfully logs in, how does the server know that the next request is coming from the same authenticated user?**

Because HTTP has an important property:

> **HTTP is stateless.**

---

## 1. The Problem

Imagine:

```text
POST /login
email = alice@example.com
password = ********
```

Server verifies the password:

```text
Password correct
      ↓
Alice is authenticated
```

Then Alice requests:

```text
GET /profile
```

How does the server know:

> "This is Alice"?

The second request doesn't automatically carry the memory of the first request.

That's the **session problem**.

---

# 2. The Traditional Solution — Sessions

The server creates a session.

Conceptually:

```text
Alice logs in
     ↓
Server creates:
session_id = X7K92...
     ↓
Server stores:
X7K92... → user_id = 42
     ↓
Browser receives session ID
```

The browser then sends that session ID on subsequent requests.

```text
Browser
   │
   │ session_id
   ▼
Server
   │
   │ lookup session
   ▼
user_id = 42
```

Now the server knows:

> This request belongs to user 42.

---

# 3. Where Does the Session ID Live?

Usually in a **cookie**.

Example conceptually:

```text
Set-Cookie:
session_id=X7K92...
```

The browser stores it.

Later:

```text
GET /dashboard
Cookie: session_id=X7K92...
```

The browser automatically sends the cookie to the appropriate domain/path according to cookie rules.

---

# 4. Cookie ≠ Session

This distinction is important.

A **cookie** is a mechanism for storing/sending data in the browser.

A **session** is an authentication/state mechanism maintained by the application.

Think:

```text
Cookie
  ↓
carries session identifier
  ↓
Server
  ↓
session storage
  ↓
user identity
```

They're related, but they're not the same thing.

---

# 5. Where Does the Server Store Sessions?

For a simple application:

```text
Server memory
```

But production systems commonly use something like:

```text
Redis
Database
Distributed session store
```

Example:

```text
Redis

session:X7K92
      ↓
{
   user_id: 42,
   role: "owner"
}
```

This becomes especially important when you have multiple backend servers.

```text
             Load Balancer
             /           \
            /             \
      Server A           Server B
           \               /
            \             /
               Redis
```

Both servers can access the same session store.

---

# 6. Why Cookies Need Security Attributes

A session cookie is extremely sensitive.

If an attacker steals it, they may be able to impersonate the user.

Therefore, cookies have important security attributes.

### `Secure`

Send the cookie only over HTTPS.

```text
Secure
```

This helps prevent accidental transmission over plaintext HTTP.

---

### `HttpOnly`

JavaScript cannot directly read the cookie.

```text
HttpOnly
```

So:

```text
document.cookie
```

cannot access that cookie.

This is particularly useful for reducing the impact of some XSS attacks against session cookies.

**But HttpOnly does not magically prevent XSS.** An XSS payload can still potentially perform actions as the user through the browser.

---

### `SameSite`

Controls when cookies are sent in cross-site contexts.

Common values:

```text
Strict
Lax
None
```

This is an important defense against certain CSRF scenarios.

---

# 7. Session Authentication Flow

Put everything together:

```text
             LOGIN
               │
               ▼
        Verify password
               │
               ▼
       Authentication ✓
               │
               ▼
       Create session
               │
               ▼
      Set-Cookie: SID
               │
               ▼
            Browser
               │
       subsequent request
               │
               ▼
        Cookie: SID
               │
               ▼
            Server
               │
        lookup session
               │
               ▼
           User = 42
               │
               ▼
        Authorization
               │
               ▼
          Response
```

This is one of the most important authentication flows to understand as a web developer.

---

# 8. What About JWT?

Now we reach the thing that causes enormous confusion:

**JWT — JSON Web Token**

A JWT can carry claims such as:

```text
{
  "sub": "42",
  "role": "owner",
  "exp": 1799000000
}
```

It is then cryptographically signed.

Conceptually:

```text
Header
+
Payload
+
Signature
```

The important point:

> **A normal signed JWT is not encrypted.**

Its payload is generally readable by whoever possesses the token.

So don't put secrets/passwords inside it.

---

# 9. Session vs JWT

### Traditional session

```text
Browser
   │
   │ session ID
   ▼
Server
   │
   ▼
Session Store
   │
   ▼
User
```

The important state lives on the server.

### JWT

```text
Browser
   │
   │ JWT
   ▼
Server
   │
   ▼
Verify signature
   │
   ▼
Read claims
```

The token itself carries information.

This can reduce the need for centralized session state, but introduces other tradeoffs.

---

# 10. The Big JWT Misconception

You'll often hear:

> "JWT is more secure than sessions."

That's nonsense as a blanket statement.

JWT and sessions solve the problem differently.

Security depends on:

* how tokens are stored
* signing-key protection
* expiration
* token rotation/revocation strategy
* authorization checks
* XSS/CSRF defenses
* transport security
* application architecture

A badly implemented JWT system can be worse than a well-designed session system.

---

# 11. JWT Revocation Problem

Suppose you issue:

```text
JWT
expires in 7 days
```

Then the user clicks:

> **Log out**

With a traditional server-side session, you can simply delete:

```text
session:X7K92
```

Done.

But a self-contained JWT may remain cryptographically valid until its expiration unless you have an additional revocation/rotation mechanism.

This is one reason **short-lived access tokens + refresh-token mechanisms** are commonly used in token-based architectures.

---

# 12. Access Token vs Refresh Token

A common architecture:

```text
Login
  │
  ├── Access Token
  │      short lifetime
  │
  └── Refresh Token
         longer lifetime
```

When the access token expires:

```text
Refresh Token
      ↓
Authorization server
      ↓
New Access Token
```

This limits the lifetime of the access credential used for ordinary API calls.

But refresh tokens themselves become highly sensitive credentials and require careful storage, rotation/revocation, and theft detection strategies.

---

# 13. Where Should You Use Which?

For a normal web application:

### Server-rendered web application

Traditional sessions + secure cookies are often an excellent choice.

### SPA + backend

You can use either:

```text
Session + cookie
```

or an appropriately designed token architecture.

Don't choose JWT simply because:

> "Modern developers use JWT."

Choose it because the architecture actually benefits from it.

### Microservices / distributed systems

Tokens can be useful because services can verify signed claims without necessarily consulting one central session database for every request.

But that doesn't automatically make JWT the best solution.

---

# 14. Your Cloud-Kitchen Application

Imagine:

```text
Owner logs in
      ↓
Authentication
      ↓
Session established
      ↓
GET /orders
      ↓
Who is the user?
      ↓
Owner #17
      ↓
Authorization
      ↓
Can Owner #17 access these orders?
      ↓
YES
      ↓
Return orders
```

Now imagine:

```text
Staff #8
      ↓
GET /admin/users
      ↓
Authenticated? YES
      ↓
Authorized? NO
      ↓
403 Forbidden
```

This connects directly to Chapter 2.

**Authentication tells you who they are.**

**Authorization tells you what they can do.**

The session/token provides the mechanism for carrying that authenticated identity across requests.

---

# 15. One More Important Attack — Session Theft

Imagine:

```text
Alice
  ↓
logs in
  ↓
session cookie
  ↓
attacker steals cookie
  ↓
attacker sends cookie
  ↓
server sees valid session
  ↓
Alice's account
```

The attacker doesn't necessarily need Alice's password.

They have effectively stolen the **authentication credential**.

This is called **session hijacking**.

That's why:

```text
HTTPS
Secure cookies
HttpOnly
SameSite
Session expiration
Session rotation
XSS prevention
```

matter.

---

# 16. The Bigger Mental Model

You can now visualize the whole authentication system:

```text
                    USER
                      │
                      ▼
                 PASSWORD
                      │
                      ▼
             Password Hashing
                      │
                      ▼
                 DATABASE
                      │
                      │
                  LOGIN
                      │
                      ▼
              Authentication
                      │
                      ▼
            Session / Token
                      │
                      ▼
            Subsequent Request
                      │
                      ▼
              Authentication
                      │
                      ▼
               Authorization
                      │
                      ▼
              Business Logic
                      │
                      ▼
                  DATABASE
```

This is much more important than memorizing "JWT syntax."

---

## The key distinction

| Concept          | Question                                        |
| ---------------- | ----------------------------------------------- |
| Password hashing | How do we safely store passwords?               |
| Authentication   | Who are you?                                    |
| Session          | How do we remember your login?                  |
| Cookie           | How does the browser store/send information?    |
| JWT              | One format/mechanism for carrying signed claims |
| Authorization    | What are you allowed to do?                     |

And now you have a complete chain:

**Password → Authentication → Session/Token → Authorization**

---

### Next: Chapter 8 — CSRF, XSS & CORS

This is where browser security gets interesting.

We'll answer three questions:

1. **How can another website trick a logged-in browser into making a request?**
2. **How can malicious JavaScript steal or abuse data in your application?**
3. **Why does the browser sometimes block one frontend from talking to another backend?**

Those lead directly into **CSRF, XSS, CORS, Same-Origin Policy, and browser security boundaries**.

