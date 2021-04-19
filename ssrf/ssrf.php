<?php
error_reporting(0);
$ch = curl_init(); //创建新的 cURL 资源
curl_setopt($ch, CURLOPT_URL, $_GET['url']);
curl_setopt($ch, CURLOPT_HEADER, 0);
curl_exec($ch);
curl_close($ch);  //关闭 cURL 资源，并且释放系统资源
?>
