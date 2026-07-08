-- Run as APP_USER after 01_table.sql and 02_acl.sql.

CREATE OR REPLACE TRIGGER documents_ai_webhook
    AFTER INSERT ON documents
    FOR EACH ROW
DECLARE
    PRAGMA AUTONOMOUS_TRANSACTION;

    v_url  VARCHAR2(500);
    v_body VARCHAR2(4000);
    v_req  UTL_HTTP.req;
    v_resp UTL_HTTP.resp;
    v_line VARCHAR2(4000);
BEGIN
    SELECT value INTO v_url FROM webhook_config WHERE name = 'url';

    v_body := JSON_OBJECT(
        'doc_id'     VALUE :NEW.doc_id,
        'title'      VALUE :NEW.title,
        'event_type' VALUE 'document.created',
        'created_at' VALUE TO_CHAR(:NEW.created_at, 'YYYY-MM-DD"T"HH24:MI:SS')
    );

    v_req := UTL_HTTP.begin_request(v_url, 'POST', 'HTTP/1.1');
    UTL_HTTP.set_header(v_req, 'Content-Type', 'application/json');
    UTL_HTTP.set_header(v_req, 'Content-Length', LENGTHB(v_body));
    UTL_HTTP.write_text(v_req, v_body);

    v_resp := UTL_HTTP.get_response(v_req);
    BEGIN
        LOOP
            UTL_HTTP.read_line(v_resp, v_line, TRUE);
        END LOOP;
    EXCEPTION
        WHEN UTL_HTTP.end_of_body THEN
            NULL;
    END;
    UTL_HTTP.end_response(v_resp);

    COMMIT;  -- autonomous transaction only
EXCEPTION
    WHEN OTHERS THEN
        -- Do not fail the INSERT if the webhook is down.
        BEGIN
            UTL_HTTP.end_response(v_resp);
        EXCEPTION
            WHEN OTHERS THEN NULL;
        END;
        NULL;
END;
/
