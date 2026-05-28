# OD Proposal Server Prototype

Local first prototype for human login and proposal/topic submission.

Run:

```bash
python3 server/proposal_server.py
```

Open:

http://127.0.0.1:8787

Data is stored locally in `server/od_lab.sqlite3` and is not suitable for production without HTTPS, real identity, consent flows, access control hardening, backups and deployment on a dedicated server.
