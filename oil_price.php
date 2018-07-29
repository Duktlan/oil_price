<?php
$con=mysqlI_connect("localhost","root","","oil_price");
mysqli_query($con,"SET NAMES utf8");
#$sql = "SELECT * FROM `oil_price_table`";
$result=mysqli_query($con,"SELECT * FROM `oil_price_table`");
$num = mysqli_num_rows($result);
$demo = array();
$k=0;
while($data = mysqli_fetch_array($result)){
    $demo[$k] = $data;
    $k++;
}
mysqli_free_result($result);
mysqli_close($con);
?>

<body bgcolor = "#99FFFF">
<style>
        table, th, td {
            border: 1px solid #888888;
            border-collapse: collapse;
            }
        th, td {
            padding: 15px;
            }
        th, td {
            text-align: center;
            }
    </style>
    <table style="width:100%">
        <tr>
            <th>柴油油價</th>
            <th>預測起伏</th>
        </tr>
<?php
            for($n=0;$n<$num;$n++){
                echo "<tr>";
                for($i=0; $i<2; $i++){
                    echo "<td>{$demo[$n][$i]}</td>";
                }
                echo "<tr>";
            }
        ?>
</body>