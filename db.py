import streamlit as st
import mysql.connector
from mysql.connector import Error

def get_conn():
    # read credentials from Streamlit secrets if present
    if 'mysql' in st.secrets:
        cfg = st.secrets['mysql']
        return mysql.connector.connect(
            host=cfg['host'],
            port=int(cfg.get('port', 3306)),
            user=cfg['user'],
            password=cfg['password'],
            database=cfg['database']
        )
    # fallback: use SQLite for local demo
    import sqlite3, os
    db_path = os.path.join(os.getcwd(), 'local_hms.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def dict_row(row, cur):
    # convert sqlite or mysql row to dict
    if row is None:
        return None
    try:
        return {k: row[k] for k in row.keys()}
    except Exception:
        # mysql returns tuples when not using dictionary cursor - handle in callers
        return row

def fetch_all(query, params=()):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True) if hasattr(conn, 'cursor') and 'mysql' in str(type(conn)).lower() else conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        # normalize sqlite rows
        if rows and isinstance(rows[0], tuple):
            cols = [d[0] for d in cur.description]
            result = [dict(zip(cols, r)) for r in rows]
        else:
            result = [dict(r) for r in rows] if rows and hasattr(rows[0], 'keys') else rows
        cur.close()
        conn.close()
        return result
    except Exception as e:
        try:
            cur.close(); conn.close()
        except: pass
        raise

def fetch_one(query, params=()):
    rows = fetch_all(query, params)
    return rows[0] if rows else None

def execute(query, params=()):
    conn = get_conn()
    try:
        cur = conn.cursor() if not hasattr(conn, 'cursor') or 'mysql' not in str(type(conn)).lower() else conn.cursor()
        cur.execute(query, params)
        conn.commit()
        cur.close(); conn.close()
    except Exception as e:
        try:
            cur.close(); conn.close()
        except: pass
        raise
