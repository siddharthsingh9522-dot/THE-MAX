# OM Suite - unified web app

Teen alag projects (Paid/ToPay, OM Suite, DBP Report) ko ek app me jodne ka project.
Ek login, ek design (light, white-blue), mobile par installable (PWA), admin approval + per-user tool access.

## Build status

| Phase | Kya hai | Status |
|---|---|---|
| **1** | Shell, login/signup + admin approval, Users & Access, Settings, Paid/ToPay Suite (saare 7 modes + CN Query + OmInsights fetch), Docker/Render, PWA | **Ready (is zip me)** |
| **2a** | DBP Report Builder, Validation & Audit, Month-wise Summary (ADR / NET / Full Region), AI Chatbot, Directory & Masters | **Ready** |
| 2b | Mail Center (branch mails, region auto-mail, full-report mail, SMTP + Thunderbird) | Next |
| 3 | TBB Mail, Bill Mail, Branch Finder, Customer Search, OM Automation (CN/GST/Party/Master) | Planned |
| - | GR Auto Modification: alag app, sirf tile/link (apna login) | Tile ready, `GR_AUTO_URL` set karna hai |

## Local chalana

```bash
pip install -r requirements.txt
cp .env.example .env        # optional
python app.py               # http://localhost:5000
python -m pytest tests      # 123 tests (85 are the original DBP engine tests, unchanged logic)
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

Lambe OmInsights exports ke liye gunicorn timeout 900 s hai (`Dockerfile`). Ek saath max 3 exports chalte hain, baaki ko "busy" milta hai.

Docker image me Chromium bhi hai (GST Query ke liye, Phase 3). Free plan ki RAM kam hai - GST Query chalane ke time `plan: starter` karna padega. Abhi ke liye Chrome nahi chahiye: `--build-arg INSTALL_CHROME=0`.

## DBP tools (Phase 2a)

* Pandas engine `dbp/` Streamlit app se aaya hai - **calculation logic same hai** (original 85 tests ab bhi pass hote hain, `tests/engine/`). Sirf screens naye shell me dobara bani hain.
* Har user ka apna workspace hota hai (`data/workspaces/<user>/`): upload hui files, generated report, chat history. 7 din purane workspace apne aap delete ho jate hain.
* **Directory & Masters** (sirf admin): directory aur branch master yahin se update hote hain; galat file upload hui to purani file safe rehti hai. Personal employee-directory workbooks `dbp/masters_seed/` me local rakhein; `.xlsx` seed files Git se excluded hain. First start par available seed files `data/masters/` me copy hote hain. Seed files ke bina bhi app start hota hai; admin Directory & Masters page se authorized workbooks upload kar sakta hai.
* Render ki disk free plan par har redeploy par reset hoti hai. Persistent data ke liye Render persistent disk lagayein; seed workbooks ko Git me commit na karein.
* `GEMINI_ADMIN_API_KEY` optional hai (chatbot ki wording ke liye). Bina key ke chatbot data se seedha jawab deta hai.
* Badi Excel files pandas me RAM leti hain; Render free (512 MB) par bahut badi files par memory kam pad sakti hai.
* Streamlit se jo cheezein nahi layi gayi: "server folder se auto-pick" (web server par meaningless), login page ka video background, month-wise "AI double-check" button.

## Jaan lena zaroori

* **OmInsights fetch (Paid/ToPay):** ab local `ominsights_proxy.py` ki zarurat nahi. Har user **Settings -> OmInsights login** me apna username/password ek baar save karta hai (login verify hota hai, password encrypted store hota hai). Server uske naam se OmInsights se data laata hai. Sirf card 546 aur 967 allowed hain (`OMINSIGHTS_ALLOWED_CARDS`) - ye open proxy nahi hai. **Zaroori:** OmInsights ko Render ka server khud reach kar pana chahiye. Agar wo sirf office network/VPN par khulta hai to ye buttons Render par kaam nahi karenge (Settings me "verify nahi hua" warning aayegi).
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
