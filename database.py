import sqlite3
import threading
import time
from typing import Dict, Iterable, List

DB_PATH = "temperature.db"

_thread_local = threading.local()
_db_init_lock = threading.Lock()
_initialized = False


def _get_conn() -> sqlite3.Connection:
    if not hasattr(_thread_local, "conn"):
        _thread_local.conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False,
            timeout=30
        )
        _thread_local.conn.row_factory = sqlite3.Row
        _initialize_db(_thread_local.conn)
    return _thread_local.conn


def _initialize_db(conn: sqlite3.Connection):
    global _initialized
    if _initialized:
        return

    with _db_init_lock:
        if _initialized:
            return

        conn.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL,
                ts INTEGER NOT NULL,
                inserted_at INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_sensor_ts
            ON readings(sensor_id, ts DESC)
        """)

        conn.commit()
        _initialized = True


# ---------- INSERT ----------
def insert_data(item: Dict):
    insert_many([item])


def insert_many(items: Iterable[Dict]):
    if not items:
        return

    conn = _get_conn()
    now = int(time.time())

    params = []
    for it in items:
        params.append((
            it["sensor_id"],
            it["temperature"],
            it.get("humidity"),
            it["ts"],
            now
        ))

    with conn:
        conn.executemany("""
            INSERT INTO readings
            (sensor_id, temperature, humidity, ts, inserted_at)
            VALUES (?, ?, ?, ?, ?)
        """, params)


# ---------- READ ----------
def query_latest(sensor_id: str, limit: int = 10) -> List[sqlite3.Row]:
    conn = _get_conn()
    cur = conn.execute("""
        SELECT sensor_id, temperature, humidity, ts, inserted_at
        FROM readings
        WHERE sensor_id = ?
        ORDER BY ts DESC
        LIMIT ?
    """, (sensor_id, limit))
    return cur.fetchall()