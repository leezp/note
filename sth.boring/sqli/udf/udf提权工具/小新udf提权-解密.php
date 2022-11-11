<?php
/**
 * Created BY 独自等待
 * Date : 13-6-25
 * Time : 下午2:27
 * FileName : decode_gzinflate2.php
 * 欢迎访问独自等待博客www.waitalone.cn
 */
$a = file_get_contents("小新udf提权.php"); //含有eval语句的文本文件
//将有eval(gzinflate(base64_decode的加密文件只留eval(gzinflate(base64_decode('...');"语句
//其他诸如"<?"等信息都去掉并保存文件为"加密.php"
while (strstr($a, "eval")) {
    ob_start();
    eval(str_replace("eval", "echo", $a));
    $a = ob_get_contents();
}
echo $a;
?>