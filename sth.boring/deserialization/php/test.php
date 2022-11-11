<?php
class A
{
    public function __toString()
    {
        $file = fopen("test2.php", "w");
		fwrite($file, $this->target);
		fclose($file);
		return $this->target;
    }
}

$obj = unserialize($_GET['usr_serialized']);
//输出__toString
echo $obj;
?>