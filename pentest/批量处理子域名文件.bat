:: author : leezp
@echo off
pushd "%~dp0"
:: md 1  创建文件夹 1
md 1
type nul > 1/a_output.txt
for /f "delims=" %%i in ('dir /b  /a-d "*.txt"') do (
	:: == 判断文件大小为 0字节
	if %%~zi == 0 (
		:: 以 _ 作分隔符 分割， www.baidu.com_full.txt
		for /f "delims=_" %%j in ('dir /b  /a-d "%%i"') do (
			echo %%j >> "1/a_output.txt"
		)
	)
    if %%~zi gtr 0 (
		if %%~zi LSS 10000 (
			type "%%i" >> "1/a_output.txt"
			echo %%i
		)
	)
	if %%~zi == 10000 (
		move "%%i" "1\"
	)
	if %%~zi gtr 10000 (
		move "%%i" "1\"
	)
)


:: gtr 表示大于 多少 字节 , LSS 表示 小于 多少字节，遍历当前目录  *.txt  文件  
:: move "%%i" "1\"  将文件移动到当前目录 1文件夹下
:: dir /b /s /a-d "*.txt"  其中 /s 表示遍历，去掉/s 只判断当前目录      
:: for默认是以空格和，：；/等标点符号作分割符的，所以要取得整行内容通常会用"delims="这样的形式来取消for的默认分割符。
:: echo %%~ni >> "1/a_output.txt"	 ::只输出文件名，不输出扩展名