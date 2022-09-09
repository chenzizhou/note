CREATE or REPLACE PROCEDURE index_table_test IS
	TYPE alter_type IS table OF varchar2(100) INDEX BY BINARY_INTEGER; 
	a alter_type;
	c INTEGER;
BEGIN
	select count(*) into c from user_tables;
	for i in 1..1000
		LOOP
			SELECT
			t.table_name INTO a ( i ) 
			FROM
			( SELECT table_name, rank ( ) over ( ORDER BY table_name ) AS n FROM user_tables ) t 
			WHERE t.n=i;
			DBMS_OUTPUT.PUT_LINE(a(i)||i);
		EXIT WHEN i=c;
		END LOOP;
		EXCEPTION
			WHEN OTHERS THEN 
				DBMS_OUTPUT.PUT_LINE('error');
END;

