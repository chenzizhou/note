SELECT
	d.dname,
	sum( e.sal ) 
FROM
	emp e,
	dept d 
WHERE
	e.deptno = d.deptno 
GROUP BY
	rollup ( d.dname ) 
ORDER BY
	d.dname;