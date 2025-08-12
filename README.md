# Hospital Management System — Streamlit (Python + MySQL)

## What is included
- `app.py` — Streamlit app (Login, Patients, Doctors, Appointments)
- `db.py` — database helpers (reads Streamlit secrets)
- `schema/hms.sql` — SQL to create DB and tables
- `requirements.txt` — Python deps
- `.streamlit/secrets.toml.example` — example for Streamlit secrets

## Quick local run
1. Create a python venv: `python -m venv venv` and activate it.
2. `pip install -r requirements.txt`
3. (Optional) If you want to test without MySQL the app will use a local sqlite DB automatically.
4. Run: `streamlit run app.py`

## Deploy on Streamlit Cloud (recommended)
1. Push this repo to GitHub (public repo recommended for free Streamlit plan).
2. Provision a free MySQL (Railway is recommended) and run `schema/hms.sql` there.
3. In Streamlit Cloud app settings, add secrets under `mysql` matching `.streamlit/secrets.toml.example`.
4. Create new app in Streamlit Cloud and point to this repo and `app.py`.
5. Deploy and open the live URL.

## Notes
- Demo credentials: `admin` / `admin123`
- For production, do not store plaintext passwords. Use hashing.
- If you want, I can also provide a GitHub Actions workflow to auto-deploy on push.
