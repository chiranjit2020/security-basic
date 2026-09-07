---
description: The browser as a security boundary — origins, the same-origin policy, CORS, and how CSRF and XSS attacks work and how a backend developer prevents them.
---

# Chapter 8 — CSRF, XSS, CORS & the Same-Origin Policy

This chapter is important because now we're moving from **backend security** into the **browser's security model**.

A useful question to keep in mind:

> **The browser is not just a UI. It is a security boundary.**

---

# 1. First: What Is an "Origin"?

An origin is essentially:

```text id="8c2m1p"
scheme + host + port
```

For example:

```text id="yqj7m8"
https://example.com:443
```

Change one of these and you potentially have a different origin.

```text id="j6w0ap"
https://example.com
https://api.example.com
http://example.com
https://example.com:8443
```

These are not all the same origin.

This leads to the **Same-Origin Policy**.

---

# 2. Same-Origin Policy

The browser generally prevents a page from freely reading data from another origin.

Imagine:

```text id="h8f3z2"
evil.com
   │
   │ "Give me data from"
   ▼
bank.com
```

If any random website could freely read another website's private responses, the web would be fundamentally broken.

So the browser says:

> **Different origins don't automatically get unrestricted access to each other's resources.**

That's the basic idea behind the **Same-Origin Policy (SOP)**.

---

# 3. But Then How Does a Frontend Call an API?

Suppose your application is:

```text id="4q1s0k"
Frontend:
https://app.example.com

API:
https://api.example.com
```

Different origins.

Your React application does:

```text id="9p0wqa"
fetch("https://api.example.com/orders")
```

The browser checks the cross-origin rules.

This is where **CORS** comes in.

---

# 4. CORS

CORS = **Cross-Origin Resource Sharing**

It allows a server to tell the browser:

> "I permit this particular origin to access my resources."

For example, the API might respond with:

```text id="9skxpm"
Access-Control-Allow-Origin:
https://app.example.com
```

The browser then permits the frontend to access the response, subject to the CORS policy.

### Important:

**CORS is primarily a browser enforcement mechanism.**

It does not protect your API from:

```text id="3k8v1r"
curl
Postman
Python
Go
another server
```

Those clients aren't subject to the browser's CORS enforcement.

Therefore:

> **CORS is not authentication.**

And:

> **CORS is not an API firewall.**

Your backend must still authenticate and authorize requests.

---

# 5. Now the Interesting Part — CSRF

Suppose Alice logs into:

```text id="w9x5k2"
bank.com
```

Her browser has:

```text id="u5g2q8"
session=ABC123
```

Now Alice visits:

```text id="n4d6za"
evil.com
```

The malicious website attempts to make a request to:

```text id="9g5s4w"
bank.com/transfer
```

If the browser automatically attaches Alice's authentication cookie under the applicable cookie rules, the request could potentially be authenticated as Alice.

That's the basic idea behind:

**Cross-Site Request Forgery (CSRF).**

The attacker isn't necessarily stealing Alice's cookie.

They're trying to **make Alice's browser perform an action using Alice's existing authentication context.**

---

# 6. CSRF in Your Cloud-Kitchen App

Imagine:

```text id="xj7jpx"
POST /api/products/123/delete
```

Owner is logged in.

Their browser automatically sends the session cookie.

A malicious page attempts to cause that request.

If your application has inadequate CSRF defenses, the server may see:

```text id="w8e1vc"
Valid session
      ↓
Authenticated owner
      ↓
Delete product
```

The owner never intentionally clicked "Delete."

That's the fundamental problem.

---

# 7. CSRF Token

One traditional defense is a CSRF token.

The server generates a random value:

```text id="a7c5qr"
csrf_token = random-secret-value
```

The legitimate application includes it in a state-changing request:

```text id="x9r1dv"
POST /products/delete

product_id=123
csrf_token=...
```

Server verifies:

```text id="q2k8zx"
Session ✓
CSRF token ✓
       ↓
Allow action
```

A malicious third-party website shouldn't be able to obtain the legitimate token under the browser's same-origin protections.

---

# 8. SameSite Cookies

Modern cookie controls provide another important CSRF defense.

For example:

```text id="y3d9sv"
SameSite=Lax
```

or:

```text id="h5p2nx"
SameSite=Strict
```

These tell the browser to restrict when cookies are sent in cross-site contexts.

But don't reduce CSRF protection to:

> "Just add SameSite and forget security."

Cookie behavior depends on the exact request/context, and applications should use an appropriate CSRF strategy for their architecture.

---

# 9. Now XSS

CSRF abuses the **user's authenticated browser**.

XSS attacks the **application's ability to safely handle untrusted content/code**.

XSS = **Cross-Site Scripting**.

Imagine your application displays:

```text id="2z8h6d"
Hello, <username>
```

If user-controlled content is inserted into HTML incorrectly, an attacker might inject JavaScript.

Conceptually:

```text id="4t0q7y"
Attacker input
      ↓
Application
      ↓
Browser interprets it as code
      ↓
Malicious JavaScript executes
```

That's XSS.

---

# 10. Why XSS Is Dangerous

JavaScript executing in your application's origin can potentially:

* read page data
* perform actions as the user
* access non-HttpOnly browser storage
* modify the UI
* send sensitive information to an attacker-controlled destination

If your application has:

```text id="w0j5ca"
XSS
 +
authenticated user
```

the consequences can be severe.

Remember our previous chapter?

`HttpOnly` can prevent JavaScript from directly reading an HttpOnly session cookie.

But:

> **HttpOnly does not make XSS harmless.**

The malicious script may still be able to make authenticated requests from the victim's browser.

---

# 11. The Classic XSS Mistake

Suppose you do something conceptually equivalent to:

```text id="v6p8bx"
element.innerHTML = userInput;
```

and `userInput` contains HTML/JavaScript that you didn't intend to trust.

You're giving the browser instructions to interpret that content as markup.

That's dangerous when the input isn't properly controlled/sanitized.

Prefer safe DOM APIs and frameworks' escaping behavior where appropriate.

---

# 12. Stored vs Reflected XSS

### Stored XSS

Attacker submits malicious content:

```text id="9c3q7h"
Comment
   ↓
Database
   ↓
Victim opens page
   ↓
Malicious script executes
```

The payload is stored by the application.

### Reflected XSS

Malicious content comes through a request and gets reflected into the response without proper handling.

Conceptually:

```text id="0t7yqa"
Malicious URL/request
        ↓
Server
        ↓
Response containing unsafe input
        ↓
Browser executes it
```

---

# 13. XSS Prevention

The core principle:

> **Treat untrusted input as data, not executable code.**

Important defenses include:

### Output encoding / escaping

Convert special characters so they remain text rather than becoming HTML/JavaScript.

### Safe DOM APIs

Prefer operations that treat content as text rather than arbitrary HTML when HTML isn't needed.

### Framework escaping

React, for example, escapes ordinary interpolated text by default.

But developers can bypass those protections with mechanisms such as raw HTML rendering.

### Content Security Policy

A **CSP** can restrict what scripts/resources the browser is allowed to execute or load.

It's a powerful additional layer, not a replacement for fixing XSS.

---

# 14. CSRF vs XSS

This distinction is worth burning into your brain.

| Attack | Main idea                                                          |
| ------ | ------------------------------------------------------------------ |
| CSRF   | Trick the victim's browser into performing an authenticated action |
| XSS    | Get malicious JavaScript to execute in the application's origin    |

Think:

```text id="q3z8hx"
CSRF
Attacker → victim's browser → legitimate application
```

versus:

```text id="w6r1cp"
XSS
Attacker → malicious code → application's browser context
```

---

# 15. CORS Is Different From Both

CORS answers:

> **"Can this browser-origin access this cross-origin response?"**

CSRF asks:

> **"Can an attacker cause a victim's browser to perform an authenticated action?"**

XSS asks:

> **"Can attacker-controlled JavaScript execute in my application's origin?"**

Same browser, completely different problems.

---

# 16. A Very Important CORS Mistake

Developers sometimes do:

```text id="b7n4ka"
Access-Control-Allow-Origin: *
```

and think:

> "Now my API is insecure."

Not necessarily.

CORS doesn't determine whether your API requires authentication.

Your API should still do:

```text id="j2p9wc"
Request
   ↓
Authentication
   ↓
Authorization
   ↓
Validation
   ↓
Business logic
```

CORS is an additional browser-level policy.

---

# 17. The Security Picture So Far

You've now built a surprisingly useful mental model:

```text id="7m5c4z"
                    WEB APP
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     PASSWORD       SESSION          BROWSER
        │              │              │
        ▼              ▼              ▼
   Hashing         Cookies       Same-Origin
                                  Policy
                                     │
                     ┌───────────────┼──────────────┐
                     │               │              │
                    XSS            CSRF            CORS
```

And these connect to the earlier chapters:

```text id="1q9b3v"
Password
   ↓
Authentication
   ↓
Session / Token
   ↓
Authorization
   ↓
Application action
```

While the browser adds:

```text id="5k8m1d"
Same-Origin Policy
       ↓
CORS / Cookie rules / browser protections
       ↓
Limits cross-site behavior
```

---

# 18. The Engineering Mental Model

When building a web application, ask:

### Authentication

> **Who is making this request?**

### Authorization

> **Are they allowed to do this?**

### CSRF

> **Could another site trick their browser into doing this?**

### XSS

> **Could attacker-controlled content become executable code?**

### CORS

> **Which browser origins are allowed to read this cross-origin response?**

### Same-Origin Policy

> **What cross-origin access does the browser prevent by default?**

These are **different security questions**.

That's the key lesson of this chapter.

---

## Next — Chapter 9: Input Validation, Injection & SQL Injection

This one is especially important for you as a backend developer.

We'll go from:

```text
User input
    ↓
Backend
    ↓
Database
```

and discover how something as innocent as:

```text
"admin"
```

can become dangerous when an application treats **data as instructions**.

We'll cover **SQL Injection, command injection, NoSQL injection, parameterized queries, validation vs sanitization, and why "escaping everything" isn't a proper security strategy.**

