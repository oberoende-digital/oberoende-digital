#!/usr/bin/env python3
import sqlite3, secrets, html, datetime
from pathlib import Path
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

class ODServer(ThreadingHTTPServer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sessions = {}

BASE = Path(__file__).resolve().parent
DB = BASE / "od_lab.sqlite3"
PORT = 8787

def db():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT UNIQUE NOT NULL, name TEXT, created_at TEXT NOT NULL)")
    con.execute("CREATE TABLE IF NOT EXISTS proposals (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, title TEXT NOT NULL, body TEXT NOT NULL, language TEXT, created_at TEXT NOT NULL, FOREIGN KEY(user_id) REFERENCES users(id))")
    return con

def now():
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def esc(x):
    return html.escape(x or "", quote=True)

class H(BaseHTTPRequestHandler):
    server_version = "ODProposalPrototype/0.1"

    def get_user(self):
        cookie = self.headers.get("Cookie", "")
        sid = None
        for part in cookie.split(";"):
            part = part.strip()
            if part.startswith("od_session="):
                sid = part.split("=", 1)[1]
        return self.server.sessions.get(sid) if sid else None

    def send_html(self, body, status=200, headers=None):
        raw = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        if headers:
            for k, v in headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(raw)

    def page(self, content):
        return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OD Proposal Portal</title><style>
body{{font-family:Inter,system-ui,-apple-system,sans-serif;background:#F7F4ED;color:#132845;margin:0;line-height:1.6}}.wrap{{max-width:840px;margin:0 auto;padding:42px 22px}}.card{{background:#fff;border:1px solid #D9D7D1;border-radius:10px;padding:24px;margin:18px 0}}input,textarea,select{{width:100%;box-sizing:border-box;padding:12px;border:1px solid #D9D7D1;border-radius:6px;font:inherit;margin:6px 0 14px}}button,.btn{{background:#132845;color:#F7F4ED;border:0;border-radius:6px;padding:11px 16px;font-weight:800;text-decoration:none;display:inline-block;cursor:pointer}}.muted{{color:#5b6775}}.top{{display:flex;justify-content:space-between;gap:12px;align-items:center}}h1{{font-family:Georgia,serif;font-size:42px;line-height:1.05}}li{{margin:8px 0}}</style></head><body><div class="wrap"><div class="top"><strong>Oberoende Digital · Proposal Portal</strong><a href="https://oberoendedigital.se">Back to site</a></div>{content}</div></body></html>'''

    def redirect(self, loc):
        self.send_response(303)
        self.send_header("Location", loc)
        self.end_headers()

    def do_GET(self):
        user = self.get_user()
        if self.path.startswith("/logout"):
            self.send_html(self.page('<div class="card"><h1>Logged out</h1><p><a class="btn" href="/">Log in again</a></p></div>'), headers={"Set-Cookie": "od_session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"})
            return
        if self.path.startswith("/proposals"):
            if not user:
                self.redirect("/")
                return
            con = db()
            rows = con.execute("SELECT p.title,p.body,p.language,p.created_at,u.email FROM proposals p JOIN users u ON u.id=p.user_id ORDER BY p.id DESC LIMIT 100").fetchall()
            con.close()
            items = ''.join(f'<li><strong>{esc(t)}</strong> <span class="muted">{esc(lang)} · {esc(ts)} · {esc(email)}</span><br>{esc(b)}</li>' for t, b, lang, ts, email in rows) or '<li>No proposals yet.</li>'
            self.send_html(self.page(f'<div class="card"><h1>Submitted proposals</h1><ol>{items}</ol><p><a class="btn" href="/">Submit another</a></p></div>'))
            return
        if not user:
            self.send_html(self.page('''<div class="card"><h1>Human login prototype</h1><p class="muted">First local prototype. No BankID yet. Use your name and email to start the human input loop.</p><form method="post" action="/login"><label>Name</label><input name="name" placeholder="Your name"><label>Email</label><input type="email" name="email" placeholder="you@example.com" required><button>Log in</button></form></div>'''))
            return
        self.send_html(self.page(f'''<div class="card"><h1>Submit a proposal or topic</h1><p class="muted">Logged in as {esc(user['email'])}. This stores your submission locally in SQLite on this machine.</p><form method="post" action="/submit"><label>Language</label><select name="language"><option>English</option><option>Svenska</option></select><label>Title</label><input name="title" required maxlength="180" placeholder="What should OD explore?"><label>Proposal / topic</label><textarea name="body" required rows="9" placeholder="Describe the proposal, concern, question, or policy area. Sources and uncertainty are welcome."></textarea><button>Submit proposal</button> <a class="btn" href="/proposals">View submissions</a> <a href="/logout">Log out</a></form></div>'''))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        data = parse_qs(self.rfile.read(length).decode("utf-8"))
        if self.path == "/login":
            email = (data.get("email", [""])[0] or "").strip().lower()
            name = (data.get("name", [""])[0] or "").strip()
            if not email or "@" not in email:
                self.send_html(self.page('<div class="card"><h1>Invalid email</h1><p><a href="/">Try again</a></p></div>'), 400)
                return
            con = db()
            con.execute("INSERT OR IGNORE INTO users(email,name,created_at) VALUES(?,?,?)", (email, name, now()))
            con.execute("UPDATE users SET name=? WHERE email=?", (name, email))
            uid = con.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()[0]
            con.commit(); con.close()
            sid = secrets.token_urlsafe(32)
            self.server.sessions[sid] = {"id": uid, "email": email, "name": name}
            self.send_response(303)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", f"od_session={sid}; Path=/; HttpOnly; SameSite=Lax")
            self.end_headers()
            return
        if self.path == "/submit":
            user = self.get_user()
            if not user:
                self.redirect("/")
                return
            title = (data.get("title", [""])[0] or "").strip()
            body = (data.get("body", [""])[0] or "").strip()
            lang = (data.get("language", [""])[0] or "").strip()
            if not title or not body:
                self.send_html(self.page('<div class="card"><h1>Missing content</h1><p><a href="/">Try again</a></p></div>'), 400)
                return
            con = db()
            con.execute("INSERT INTO proposals(user_id,title,body,language,created_at) VALUES(?,?,?,?,?)", (user["id"], title, body, lang, now()))
            con.commit(); con.close()
            self.send_html(self.page(f'<div class="card"><h1>Proposal received</h1><p><strong>{esc(title)}</strong></p><p class="muted">Stored locally. Next step is AI-assisted clustering, evidence lookup and deliberation workflow.</p><p><a class="btn" href="/">Submit another</a> <a class="btn" href="/proposals">View submissions</a></p></div>'))
            return
        self.send_error(404)

if __name__ == "__main__":
    db().close()
    httpd = ODServer(("127.0.0.1", PORT), H)
    print(f"OD proposal prototype serving at http://127.0.0.1:{PORT}", flush=True)
    httpd.serve_forever()
