<?php 
$user="ist153890";
$host="db.ist.utl.pt";
$port=5432;
$password="thlt7466";
$dbname = $user;

// Specify domains from which requests are allowed
header('Access-Control-Allow-Origin: *');

// Specify which request methods are allowed
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');

$connection = pg_connect("host=$host port=$port user=$user password=$password dbname=$dbname") or die(pg_last_error());


/*
CREATE TABLE certs (
  serialNumber varchar(255) NOT NULL,
  issuerName varchar(255) NOT NULL,
  subjectName varchar(255) NOT NULL,
  notBefore varchar(255) NOT NULL,
  notAfter varchar(255) NOT NULL,
  timesChecked int,
  valid int,
  PRIMARY KEY (serialNumber, issuerName),
  CHECK (timesChecked > 0)
);
*/
/*
$_POST['host']
$_POST['commonName']
$_POST['organization']
$_POST['organizationalUnit']
$_POST['serialNumber']
$_POST['emailAddress']
$_POST['notBefore']
$_POST['notAfter']
$_POST['issuerCommonName']
$_POST['issuerOrganization']
$_POST['issuerOrganizationUnit']
$_POST['md5Fingerprint']
$_POST['sha1Fingerprint']
$_POST['issuerMd5Fingerprint']
$_POST['issuerSha1Fingerprint']
$_POST['cert']
*/

$sql = "SELECT * FROM certs WHERE serialnumber = '" . $_POST['serialNumber'] . "' AND issuername = '" . $_POST['issuerCommonName'] . "'";

$result = pg_query($sql) or die(pg_last_error());

$row = pg_fetch_assoc($result);

$currentDate  = mktime(0, 0, 0, date("m")  , date("d"), date("Y"));
if($row) {
	if($row['valid']) {
		if($currentDate > strtotime($row['notbefore']) && $currentDate < strtotime($row['notafter'])) {
			$valid = true;
			$valid = ($_POST['commonName'] == $row['subjectname']) && $valid;
			$valid = (strtotime($_POST['notBefore']) == strtotime($row['notbefore'])) && $valid;
			$valid = (strtotime($_POST['notAfter']) == strtotime($row['notafter'])) && $valid;
			if($valid) {
				echo "OK";
			} else {
				echo "NEG";
			}
		} else {
			echo "NEG";
		}
	} else {
		echo "NEG";
	}
} else {
	echo "NUL";
}

//var_dump($_POST);

?>