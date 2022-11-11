## 场景1

有一个文件中有很多行，每一行的长度不同，但是有规律，需要提取其中每一行大于多少字符的内容并保存。


文件名是 a

打印每行字符数：

	awk -F "" '{print NF}' a

编写 a.sh：

	num=0;
	for i in `awk -F "" '{print NF}' a`;
	do
	if [ $i -gt 292 ] ;then    # 提取大于292字符的行
	#echo $i;
	num=$[num+1];  			   # shell addition
	#echo $num;
	echo `awk NR=="$num" a`;   # 打印文件指定行号的内容
	fi
	done

执行完最终从89行中导出18行我需要的数据。