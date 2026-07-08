# Oracle insert → webhook (Option C)

When a row is inserted into `documents`, an `AFTER INSERT` trigger calls your server with `UTL_HTTP`.

## Files

| File | Purpose |
|------|---------|
| `sql/01_table.sql` | `documents` table + webhook URL config |
| `sql/02_acl.sql` | Network ACL (run as SYS) |
| `sql/03_trigger.sql` | Trigger that POSTs JSON on insert |
| `server/receiver.py` | Simple Python server to catch the webhook |
| `insert_test.py` | Insert a test row from Python |

## Try it

### 1. Start the receiver

```bash
python server/receiver.py
```

Runs on port `8000`. Note your machine's IP (e.g. `192.168.1.10`) — Oracle must reach this address. `localhost` only works if Oracle is on the same host.

### 2. Run the SQL scripts

```bash
# as APP_USER
sqlplus app_user/pass@XEPDB1 @sql/01_table.sql

# as SYS — edit host IP and APP_USER in the file first
sqlplus sys/pass@XEPDB1 as sysdba @sql/02_acl.sql

# as APP_USER — edit webhook URL in 01_table.sql if needed
sqlplus app_user/pass@XEPDB1 @sql/03_trigger.sql
```

Or test with SQL only:

```sql
INSERT INTO documents (title, content) VALUES ('Hello', 'world');
COMMIT;
```

### 3. (Optional) Insert from Python

```bash
pip install -r requirements.txt
export DB_USER=app_user DB_PASSWORD=pass DB_DSN=localhost:1521/XEPDB1
python insert_test.py
```

You should see the JSON payload printed in the receiver terminal.

## Payload example

```json
{"doc_id":1,"title":"Hello","event_type":"document.created","created_at":"2026-07-08T12:00:00"}
```

## Notes

- The trigger uses an **autonomous transaction** so a slow/down webhook does not roll back the insert.
- Failed webhooks are swallowed (insert still succeeds). There is no retry — use an outbox pattern if you need that.
- For **HTTPS**, you also need an Oracle wallet with the server's CA certificate.
