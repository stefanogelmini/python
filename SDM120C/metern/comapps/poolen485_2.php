#!/usr/bin/php
<?php

if (isset($_SERVER['REMOTE_ADDR'])) {
    die('Direct access not permitted');
}
// This script will output a meterN compatible format for the main command
// You'll need to setup the path to meterN ($pathtomn). Put the meters numbers ($metnum) and the corresponding command ($cmd) :

$pathtomn = '/var/www/metern';

if (isset($argv[2])) {

  $metnum = $argv[2];
  $id = $argv[1];

} else if (isset($argv[1])) {

    $metnum = $argv[1];
    $id = 0;

} else {
    die("Usage: $argv[0] [id] metnum \n");
}

define('checkaccess', TRUE);
include("$pathtomn/config/config_main.php");
include("$pathtomn/config/config_met$metnum.php");

//echo "id = $id, metnum = $metnum\n";
//echo "ID = ${'ID'.$metnum}\n";
//echo "UNIT = ${'UNIT'.$metnum}\n";

if ($id == 0) {
    $id = ${'ID'.$metnum};
}

$tdir = "/run/shm";
$cmd = 'cat '.$tdir.'/metern'.$id.'.txt | egrep "^'.$id.'\(" | grep "*Wh)" | cut -d\( -f2 | cut -d* -f1';
$meter_val = (int) exec($cmd);
//echo "$cmd\n";
//echo "meter_val = $meter_val\n";
// End of setup

// acquisisce il valore precedente dal csv
$dir    = "$pathtomn/data/csv";
$output = array();
$output = glob($dir . '/*.csv');
sort($output);
$cnt = count($output);
    
if (file_exists($output[$cnt - 1])) {
    $file       = file($output[$cnt - 1]); // today
    $contalines = count($file);

    if ($contalines > 1) {
        $prevarray = preg_split("/,/", $file[$contalines - 1]);
        
    } elseif ($contalines == 1 && file_exists($output[$cnt - 2])) { // yesterday, only header
        $file       = file($output[$cnt - 2]);
        $contalines = count($file);
        $prevarray = preg_split("/,/", $file[$contalines - 1]);
    }
    $cons_val_first = trim($prevarray[$metnum]);
} else {
    $cons_val_first = null;
}      

sleep(1); // oh why ?
// Now retrieve the current value
$datareturn = shell_exec($cmd);
$datareturn = trim($datareturn);
$datareturn = preg_replace("/^${'ID'.$id}\(/i", '', $datareturn); // VALUE*UNIT)
$lastval    = preg_replace("/\*[a-z0-9]+\)$/i", '', $datareturn); // VALUE
//echo "last_val = $lastval\n";

settype($lastval, 'float');
settype($prevcount, 'float');
settype($cons_val_first, 'float');

$prevcount = file_get_contents("$pathtomn/data/correcons$id.txt"); // file correttore del totale
$lastval += $prevcount; // aggiunge il correttore del totale
//echo "prevcount = $prevcount\n";

if ($lastval < $cons_val_first) { // controlla se il contatore segna meno del valore precedente
    $blackout = abs ($lastval - $cons_val_first);
    $prevcount += $blackout;
    file_put_contents("$pathtomn/data/correcons$id.txt", $prevcount);
    $lastval = $cons_val_first;
}

$lastval = round($lastval, ${'PRECI' . $metnum});
$str     = utf8_decode("${'ID'.$metnum}($lastval*${'UNIT'.$metnum})\n");
file_put_contents("$tdir/consumi$id.txt", $str);
echo "$str";

?>
