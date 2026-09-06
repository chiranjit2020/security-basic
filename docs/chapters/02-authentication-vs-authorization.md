---
description: Authentication vs authorization for backend developers — identity vs permission, 401 vs 403, BOLA/IDOR, RBAC and ABAC, and never trusting the frontend.
---

# Chapter 2 — Authentication vs Authorization

!!! question "The question"
    A user is logged in. Does that mean they're allowed to do what they just asked for?
    How does a web application actually decide *who can access what*?

Now that you understand **CIA**, the next step is learning **how a web application decides who can access what**.

This is one of the most important security concepts for a backend developer.

---

## 1. The fundamental distinction

There are two different questions:

```text
AUTHENTICATION
      ↓
"WHO ARE YOU?"

AUTHORIZATION
      ↓
"WHAT ARE YOU ALLOWED TO DO?"
```

Or simply:

> **Authentication = Identity**
> **Authorization = Permission**

Don't mix them.

---

## 2. Authentication — "Who are you?"

Suppose you visit:

```text
https://example.com/dashboard
```

The server needs to determine:

> Is this request coming from Chiranjit, or from an unauthenticated user?

A common flow is:

```text
Browser
   │
   │ username + password
   ↓
POST /login
   │
   ↓
Backend
   │
   ├── Find user
   ├── Verify password
   └── Create authenticated session
             │
             ↓
        Browser receives
        session cookie
```

From that point onward, the browser sends the session information with subsequent requests.

```text
GET /dashboard
Cookie: session=abc123
```

The server can now associate:

```text
abc123 → User #42
```

That's **authentication**.

---

## 3. But authentication isn't permission

Imagine User #42 successfully logs in.

They are authenticated.

But then they request:

```http
DELETE /api/users/7
```

Should they be allowed to delete User #7?

**Not necessarily.**

The server must perform another check:

```text
Is User #42 authenticated?
        ↓ YES
Is User #42 authorized to delete User #7?
        ↓ NO
       403
```

That's **authorization**.

---

## 4. Your cloud-kitchen application

Let's use the type of application you've been building.

Suppose there are three users:

```text
Owner
Manager
Staff
```

They all log in through the same system.

#### Authentication

```text
Owner
   ↓
login
   ↓
"Yes, you're Owner #1"
```

```text
Manager
   ↓
login
   ↓
"Yes, you're Manager #7"
```

```text
Staff
   ↓
login
   ↓
"Yes, you're Staff #19"
```

All three are **authenticated**.

But their permissions differ.

#### Authorization

```text
                 OWNER   MANAGER   STAFF
View orders        ✓        ✓        ✓
Create order      ✓        ✓        ✓
Change price      ✓        ✓        ✗
Delete product    ✓        ✓        ✗
View reports      ✓        ✓        ✗
Manage users      ✓        ✗        ✗
```

That's authorization.

---

## 5. The dangerous mistake beginners make

They protect a route like this:

```php
if (!$user_logged_in) {
    die("Unauthorized");
}
```

They think:

> "Great. The endpoint is secure."

No.

You've only established:

**Authentication.**

You haven't established:

**Authorization.**

The real logic should conceptually be:

```text
Request
   ↓
Is user authenticated?
   ↓
YES
   ↓
Who is the user?
   ↓
What permissions does this user have?
   ↓
Is this operation allowed?
   ↓
YES → perform operation
NO  → reject
```

---

## 6. HTTP status codes make this clearer

You'll commonly encounter:

#### `401 Unauthorized`

Despite its confusing name, it essentially means:

> **You haven't successfully authenticated.**

Example:

```text
GET /api/profile

No valid session/token
        ↓
       401
```

#### `403 Forbidden`

Means:

> **I know who you are, but you're not allowed to do this.**

```text
User = Staff
Request = DELETE /products/10

Authenticated ✓
Authorized   ✗
             ↓
            403
```

This distinction is extremely useful when designing APIs.

---

## 7. Now connect this to CIA

Remember our previous chapter?

Authentication and authorization are **mechanisms that help enforce security properties**.

Consider:

```text
Staff → GET /customers/42
```

If Staff shouldn't see that customer's private information:

```text
Authorization
      ↓
Request denied
      ↓
Confidentiality protected
```

Now:

```text
Staff → PUT /products/42
       change price
```

If Staff shouldn't modify prices:

```text
Authorization
      ↓
Request denied
      ↓
Integrity protected
```

So:

```text
                AUTHORIZATION
                      │
             ┌────────┴────────┐
             ↓                 ↓
       Confidentiality      Integrity
       "Can't see it"      "Can't change it"
```

That's a much better mental model than treating authorization as just another login feature.

---

## 8. The really important part: Never trust the frontend

Suppose your React frontend does this:

```javascript
if (user.role === "admin") {
    showDeleteButton();
}
```

That's good for **UI**.

But it provides **zero security by itself**.

An attacker can simply call your API directly:

```http
DELETE /api/products/42
```

They don't need your button.

Therefore:

> **The frontend can hide functionality. The backend must enforce permission.**

This is one of the most important rules you'll learn as a backend developer.

```text
              FRONTEND
                 │
        UI convenience only
                 │
                 ↓
            BACKEND
                 │
        REAL security boundary
                 │
                 ↓
             DATABASE
```

---

## 9. Authentication mechanisms

Authentication can be implemented in different ways.

#### Session-based authentication

```text
Login
 ↓
Server creates session
 ↓
Session ID → browser cookie
 ↓
Browser sends cookie
 ↓
Server identifies user
```

Very common for traditional web applications.

---

#### Token-based authentication

```text
Login
 ↓
Server issues token
 ↓
Client stores token
 ↓
Client sends token with requests
 ↓
Server validates token
```

You'll encounter things like:

* JWT
* OAuth 2.0
* OpenID Connect
* API keys

**Don't learn these yet.**

First understand the underlying concepts.

---

## 10. Authorization models

Once you understand authentication vs authorization, you'll encounter several ways to implement permissions.

#### ACL — Access Control List

```text
User 42 → can read
User 51 → can read + write
User 73 → can read + delete
```

#### RBAC — Role-Based Access Control

```text
User
 ↓
Role
 ↓
Permissions
```

For example:

```text
Staff
 ↓
orders.read
orders.create

Manager
 ↓
orders.read
orders.create
inventory.write

Owner
 ↓
*
```

#### ABAC — Attribute-Based Access Control

Instead of only asking:

> "What role does this person have?"

you can consider attributes:

```text
User role
+
Department
+
Resource owner
+
Location
+
Time
+
Action
```

For example:

> A manager can modify orders **belonging to their branch** during working hours.

That's a considerably more sophisticated authorization system.

---

## 11. A real API mental model

Suppose you build:

```http
PATCH /api/products/123
```

Your backend shouldn't think:

> "The frontend sent a request, so update the database."

It should think:

```text
                    REQUEST
                       │
                       ↓
                 Authentication
                       │
                 "Who are you?"
                       │
                       ↓
                  Authorization
                       │
              "Can you do this?"
                       │
                       ↓
                    Validation
                       │
               "Is this data valid?"
                       │
                       ↓
                 Business Logic
                       │
                       ↓
                    Database
```

This is becoming the **security mindset** I want you to develop.

---

## 12. One subtle but critical concept

Suppose the URL is:

```http
GET /api/orders/123
```

And User #42 is logged in.

You check:

```text
User #42 is authenticated ✓
```

But you forget:

```text
Does Order #123 belong to User #42?
```

If Order #123 belongs to User #99, you've created a vulnerability.

This is commonly called **Broken Object Level Authorization (BOLA)**, historically also associated with **IDOR** patterns.

And this connects directly to something you will eventually study in the **OWASP Top 10**.

---

## 🧠 Your mental model after Chapter 2

You should now be able to look at a web request like this:

```text
                    HTTP REQUEST
                         │
                         ↓
                ┌────────────────┐
                │ AUTHENTICATION  │
                │    WHO ARE YOU? │
                └───────┬────────┘
                        ↓
                ┌────────────────┐
                │ AUTHORIZATION   │
                │ WHAT CAN YOU DO?│
                └───────┬────────┘
                        ↓
                   VALIDATION
                        ↓
                  BUSINESS LOGIC
                        ↓
                    DATABASE
```

And underneath it:

```text
        SECURITY OBJECTIVES
               │
       ┌───────┼───────┐
       ↓       ↓       ↓
     CONF.   INTEGRITY  AVAIL.
       │       │       │
       └───────┼───────┘
               ↑
        AuthN + AuthZ
```

### The next chapter

**Chapter 3 — Encryption vs Hashing vs Encoding**

This is where things get particularly important for you because you'll encounter:

**AES, RSA, ECC, SHA-256, bcrypt, Argon2, Base64, HTTPS, passwords, tokens, JWTs...**

And I'll show you **why these are completely different things**, despite beginners often putting them all under the word *"encryption."*
