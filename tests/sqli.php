<?php
$con = mysqli_connect("127.0.0.1","test","test","test");
if (mysqli_connect_errno($con)) 
{ 
    die("连接 MySQL 失败: " . mysqli_connect_error()); 
} 

$uname = $_REQUEST['uname'];
$passwd = $_REQUEST['passwd'];
$query  = "SELECT * FROM users WHERE `username` = '$uname' and `password` = '$passwd' ";

$result = mysqli_query($con,$query);

if (!$result)
{
    die("错误描述: " . mysqli_error($con));
}

while($row = mysqli_fetch_array($result)){
  echo $row['0'] . " " . $row['1'];
  echo "<br />";
}
echo "<br/>";
echo $query;
mysqli_close($con);