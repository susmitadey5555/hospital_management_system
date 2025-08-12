import streamlit as st
import pandas as pd
from db import fetch_all, execute, get_conn, fetch_one
st.set_page_config(layout='wide', page_title='HMS — Streamlit')
# dark-ish CSS
st.markdown("""
<style>
    .stApp { background-color: #0e1117; color: #d7dbe0; }
    .block-container{padding:1rem 2rem}
    .stButton>button { background-color:#1f6feb; color:white; border-radius:6px; }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title('Hospital Management System — Login')
    user = st.text_input('Username')
    pwd = st.text_input('Password', type='password')
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button('Login'):
            rows = fetch_all('SELECT * FROM users WHERE username=%s AND password=%s', (user, pwd))
            if rows:
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error('Invalid credentials')
    with col2:
        st.write('Demo credentials: **admin / admin123**')
else:
    st.sidebar.title('Navigation')
    page = st.sidebar.radio('Go to', ['Dashboard','Patients','Doctors','Appointments','Logout'])

    if page == 'Logout':
        st.session_state.logged_in = False
        st.experimental_rerun()

    if page == 'Dashboard':
        st.header('Dashboard')
        patients = fetch_one('SELECT COUNT(*) AS c FROM patients')['c'] or 0
        doctors = fetch_one('SELECT COUNT(*) AS c FROM doctors')['c'] or 0
        appts = fetch_one('SELECT COUNT(*) AS c FROM appointments')['c'] or 0
        c1, c2, c3 = st.columns(3)
        c1.metric('Patients', patients)
        c2.metric('Doctors', doctors)
        c3.metric('Appointments', appts)

    if page == 'Patients':
        st.header('Patients')
        df = pd.DataFrame(fetch_all('SELECT * FROM patients'))
        st.dataframe(df)
        with st.expander('Add patient'):
            name = st.text_input('Name', key='pname')
            age = st.number_input('Age', min_value=0, max_value=120, key='page')
            gender = st.selectbox('Gender', ['', 'Male', 'Female', 'Other'], key='pg')
            contact = st.text_input('Contact', key='pc')
            if st.button('Add patient'):
                execute('INSERT INTO patients (name, age, gender, contact) VALUES (%s,%s,%s,%s)', (name, age, gender, contact))
                st.success('Added'); st.experimental_rerun()

    if page == 'Doctors':
        st.header('Doctors')
        df = pd.DataFrame(fetch_all('SELECT * FROM doctors'))
        st.dataframe(df)
        with st.expander('Add doctor'):
            name = st.text_input('Name', key='dname')
            spec = st.text_input('Specialization', key='dspec')
            contact = st.text_input('Contact', key='dc')
            if st.button('Add doctor'):
                execute('INSERT INTO doctors (name, specialization, contact) VALUES (%s,%s,%s)', (name, spec, contact))
                st.success('Added'); st.experimental_rerun()

    if page == 'Appointments':
        st.header('Appointments')
        df = pd.DataFrame(fetch_all('SELECT * FROM appointments'))
        st.dataframe(df)
        with st.expander('Create appointment'):
            patients = fetch_all('SELECT patient_id, name FROM patients')
            doctors = fetch_all('SELECT doctor_id, name FROM doctors')
            p_map = {f"{r['patient_id']}: {r['name']}": r['patient_id'] for r in patients}
            d_map = {f"{r['doctor_id']}: {r['name']}": r['doctor_id'] for r in doctors}
            psel = st.selectbox('Patient', list(p_map.keys()) if p_map else ['No patients'], key='apsel')
            dsel = st.selectbox('Doctor', list(d_map.keys()) if d_map else ['No doctors'], key='adsel')
            date = st.date_input('Date')
            time = st.text_input('Time (HH:MM:SS)', value='09:00:00')
            if st.button('Add appointment'):
                if p_map and d_map:
                    pid = p_map[psel]; did = d_map[dsel]
                    execute('INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (%s,%s,%s,%s)', (pid, did, date.isoformat(), time))
                    st.success('Appointment created'); st.experimental_rerun()
                else:
                    st.error('Add patients and doctors first')
