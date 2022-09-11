<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
# Get the language parameter from the URL (e.g. quote.php?lang=de) only if it is set
$lang = isset($_GET['lang']) ? $_GET['lang'] : 'en';
if (isset($_GET['lang'])) {
    // Update to new base URL https://raw.githubusercontent.com/OpenSourceSimon/QuoteAPI/main/main.json
    $URL = 'https://raw.githubusercontent.com/OpenSourceSimon/QuoteAPI/main/file_'.$lang.'.json';
} else {
    $URL = 'https://raw.githubusercontent.com/OpenSourceSimon/QuoteAPI/main/main.json';
}
$json = file_get_contents($URL);
$arr = json_decode($json, true);
$element = $arr[mt_rand(0, count($arr) - 1)];

$json = json_encode($element);

print($json);
?>
