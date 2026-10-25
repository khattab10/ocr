-- Run as SYS (or another DBA). Adjust host, port, and APP_USER.

BEGIN
    DBMS_NETWORK_ACL_ADMIN.APPEND_HOST_ACE(
        host       => '192.168.1.10',   -- IP/hostname of your Python server
        lower_port => 8000,
        upper_port => 8000,
        ace        => xs$ace_type(
            privilege_list => xs$name_list('http'),
            principal_name => 'APP_USER',
            principal_type => xs_acl.ptype_db
        )
    );
END;
/
