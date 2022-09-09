CREATE OR REPLACE TRIGGER TRIG_TEST
	AFTER UPDATE 
	ON emp
	FOR EACH ROW
DECLARE
	PRAGMA AUTONOMOUS_TRANSACTION;
	a VARCHAR2(10);
BEGIN
	select count(*) into a  from emp WHERE DEPTNO=2;
	dbms_output.put_line(a); 

-- 	UPDATE emp SET sal=:OLD.SAL; --出现死锁
END TRIG_TEST;

UPDATE emp SET sal=5000 where ename='nature';
