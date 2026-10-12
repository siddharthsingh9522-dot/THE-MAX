# OM Suite - unified web app

Teen alag projects (Paid/ToPay, OM Suite, DBP Report) ko ek app me jodne ka project.
Ek login, ek design (light, white-blue), mobile par installable (PWA), admin approval + per-user tool access.

## Build status

| Phase | Kya hai | Status |
|---|---|---|
| **1** | Shell, login/signup + admin approval, Users & Access, Settings, Paid/ToPay Suite (saare 7 modes + CN Query), Docker/Render, PWA | **Ready (is zip me)** |
| 2 | DBP Report Builder, Month-wise Summary, AI Chatbot, Validation, Directory, Mail Center + Thunderbird | Planned |
| 3 | TBB Mail, Bill Mail, Branch Finder, Customer Search, OM Automation (CN/GST/Party/Master) | Planned |
| - | GR Auto Modification: alag app, sirf tile/link (apna login) | Tile ready, `GR_AUTO_URL` set karna hai |

## Local chalana

```bash
pip install -r requirements.txt
cp .env.example .env        # optional
python app.py               # http://localhost:5000
python -m pytest tests      # 14 tests
```
`ADMIN_EMAILS` wala email signup karte hi admin ban jata hai. Agar `ADMIN_EMAILS` khali ho to pehla signup admin banta hai.
Bina Firebase ke app local SQLite (`data/omsuite.db`) use karta hai - sirf development ke liye.

## Firebase (persistent users) - ek baar ka setup

1. Firebase console -> project **ptp-report** -> *Build -> Firestore Database* (agar nahi bana to Create database).
2. *Project settings -> Service accounts -> Generate new private key* -> JSON file download hogi.
3. Us JSON ka poora content Render me env var **`FIREBASE_SERVICE_ACCOUNT_JSON`** me paste karo (ya local me `FIREBASE_SERVICE_ACCOUNT_FILE=path`). **Is JSON ko GitHub par kabhi mat daalna.**
4. Firestore *Rules* me sab client access band kar do (server Admin SDK rules bypass karta hai):
   ```
   rules_version = '2';
   service cloud.firestore { match /databases/{database}/documents { match /{document=**} { allow read, write: if false; } } }
   ```
   Dhyan: purana Paid/ToPay (Netlify) abhi Firestore me seedha API key se `ptp_auth/store` padhta hai - ye rule lagate hi wo purana login band ho jayega. Naye app par shift hone ke baad hi lagao.

Users collection `omsuite_users`, audit `omsuite_audit` me jate hain (naya data; purane `ptp_auth/store` ko ye app nahi chhoota).

## Render par deploy (Docker)

1. Is folder ko GitHub repo me push karo.
2. Render -> New -> **Blueprint** -> repo choose karo (`render.yaml` apne aap padh leta hai).
3. Env vars: `FIREBASE_SERVICE_ACCOUNT_JSON` (upar wala), `ADMIN_EMAILS` (check karo), `GR_AUTO_URL` (GR Auto ka URL, optional). `SECRET_KEY` Render khud banata hai.
4. Deploy ke baad `https://<app>.onrender.com/healthz` me `"store": "firestore"` dikhna chahiye. Agar `"local"` dikhe to Firebase JSON set nahi hua - users redeploy par ud jayenge.

Docker image me Chromium bhi hai (GST Query ke liye, Phase 3). Free plan ki RAM kam hai - GST Query chalane ke time `plan: starter` karna padega. Abhi ke liye Chrome nahi chahiye: `--build-arg INSTALL_CHROME=0`.

## Jaan lena zaroori

* **Paid/ToPay "Fetch from OM Insights" buttons** `http://127.0.0.1:5051` par ek local proxy (`ominsights_proxy.py`) maangte hain. Wo file zip me nahi thi, aur Render par ye address kaam nahi karega. Baaki sab (upload se report banana, region split, auto mail draft, CN Query) bina proxy ke chalta hai.
* Paid/ToPay ka calculation code bilkul wahi hai jo pehle tha (browser me chalta hai) - sirf design aur navigation naya hai, login hata kar shell ka login lagaya hai.
* Purane Paid/ToPay users naye app me automatic nahi aate (password hash format alag hai). Sab ko ek baar signup karna hoga, admin approve karega.
* Auto Mail abhi `mailto:`/.eml draft banata hai; "Send via Thunderbird" bridge Phase 2 me Mail Center ke saath aayega.

## Structure

```
app.py, wsgi.py            app factory / gunicorn entry
core/                      config, store (Firestore|SQLite), auth, security, module registry
blueprints/                main (dashboard/settings), admin, paid_topay
templates/, static/        shell + design tokens; static/modules/paid_topay = the tool
tests/                     pytest
Dockerfile, render.yaml
```
Naya tool jodne ke liye: `core/modules.py` me entry, ek blueprint, ek template - baaki (sidebar, dashboard card, admin access) apne aap ho jata hai.
