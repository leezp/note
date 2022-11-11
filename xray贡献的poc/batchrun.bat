setlocal enabledelayedexpansion
set /a c=0
for /f %%i in (url.txt) do (
set m=%%i
set /a c+=1
.\xray_windows_amd64.exe webscan --basic-crawler http://%m% --html-output !c!.html
)