SELECT SYSDATE--获取当前时间yyyymmddhhmiss
,
CURRENT_TIMESTAMP --获取当前时间时间戳
,
ADD_MONTHS( to_date( '19970604', 'yyyymmdd' ), '3' ) --制定日期增加count月
,
last_day( to_date( '19970604', 'yyyymmdd' ) ) --指定日期这个月最后一天
,
ceil( months_between( to_date( '20220824', 'yyyymmdd' ), to_date( '20220704', 'yyyymmdd' ) ) ) AS months --获取两个日期之间相差月数
,
next_day( to_date( '20220824', 'yyyymmdd' ), 'Monday' ) --当第二个参数传的星期数比现有星期数小的时候，会返回下一个星期的日期；当第二个参数所传的星期数比 现有的星期数大的时候，则会返回本周的相应星期日期。
,
greatest( to_date( '20250824', 'yyyymmdd' ), to_date( '20230824', 'yyyymmdd' ) ) --获取日期最大值

FROM
	dual;