<?php
$servername = "localhost";
$username = "root";
$password = "root";
$dbname = "t";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

$sql = "SELECT temp, time FROM temp";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
        echo "temp: " . $row["temp"]. " - time: " . $row["time"]. "<br>";
    }
} else {
    echo "0 results";
}
$conn->close();
?>