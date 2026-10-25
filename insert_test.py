"""Insert one row to fire the webhook trigger.

    export DB_USER=app_user DB_PASSWORD=... DB_DSN=localhost:1521/XEPDB1
    python insert_test.py
"""
import os

import oracledb

conn = oracledb.connect(
    user=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    dsn=os.environ["DB_DSN"],
)
with conn.cursor() as cur:
    cur.execute(
        "INSERT INTO documents (title, content) VALUES (:t, :c) RETURNING doc_id INTO :id",
        t="Test from Python",
        c="Hello webhook",
        id=cur.var(oracledb.NUMBER),
    )
    doc_id = cur.getvalue(0)[0]
conn.commit()
conn.close()
print(f"Inserted doc_id={doc_id} — check the receiver terminal.")
