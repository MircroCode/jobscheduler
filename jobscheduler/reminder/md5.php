<?php
$fieldInfo =  $_SERVER["argv"][1];
$fieldInfo = md5($fieldInfo);
echo $fieldInfo;

?>
