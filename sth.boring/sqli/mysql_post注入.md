三种特殊注入

INSERT

UPDATE

DELETE


	INSERT INTO HACK VALUES(1,2,3);
	
	UPDATE HACK SET NAME = 'GUEST' WHERE id = 1;
	
	DELETE FROM HACK WHERE id = 2;


**检测方法**

DELETE 一般使用延时注入的方法判断是否存在注入

	DELETE FROM HACK WHERE id = 13 and if(1=1,sleep(5),0);

实际不会删除数据

条件判断	IF(exp,v1,v2)  

如果满足 条件，执行v1,否则执行v2,如果v2 是0或false,当不满足条件，if(0) 或if(false)返回的也是false。

如果满足条件，执行的是 ```DELETE FROM HACK WHERE id = 13 and sleep(2)```

mysql会延迟但不会删除数据。

	select sleep（0.5）

返回下表，说明**sleep() 函数在数据库中的bool值是false**

	+------------+
	| sleep(0.5) |
	+------------+
	|          0 |
	+------------+


UPDATE 语句与insert类似