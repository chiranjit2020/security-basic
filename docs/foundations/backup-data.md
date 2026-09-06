---
description: Where backups fit in the three states of data, why "backup data" is not a fourth state, and the security concerns backups need of their own.
---

# Foundation — Backup Data

!!! question "The question"
    Backups are stored somewhere too — disk, tape, cloud. So is "backup data" a fourth
    state of data?

**Backup data is a form of data at rest** because a backup is stored somewhere—disk, SSD, tape, cloud storage, etc.

But there is a useful distinction:

```text
DATA
│
├── Data in Use
│   └── RAM / CPU / application processing
│
├── Data in Transit
│   └── Network / API / TCP / HTTPS
│
└── Data at Rest
    ├── Primary data
    │   └── Database / filesystem
    │
    └── Backup data
        ├── Local backup
        ├── Remote backup
        ├── Cloud backup
        ├── Snapshot
        └── Archive
```

## But "backup data" is not a fourth state

It's a **category/purpose of stored data**, not another state alongside the three.

For example:

> MySQL database → **Data at Rest**
> MySQL backup → **Data at Rest**

If you're **uploading the backup to cloud storage**, however, it temporarily becomes **Data in Transit** during the transfer:

```text
Database
   │
   │ backup/export
   ↓
Backup file
   │
   │ HTTPS / SFTP
   ↓
Cloud storage
   │
   └── Data at Rest
```

This distinction becomes important in backend engineering because **backups need their own security considerations**: encryption, access control, retention, integrity, versioning, and secure deletion.

So your instinct is right: **backup data deserves its own classification from an operational/security perspective, but not as a fourth "state of data."**
