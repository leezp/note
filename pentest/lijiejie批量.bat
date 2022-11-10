:: lijiejie 批量

setlocal enabledelayedexpansion
for /f %%i in (url.txt) do (
python subDomainsBrute.py %%i  --full
)