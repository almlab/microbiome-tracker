<?php

### Authentication ###
function getIP(){
    //Check IP Address
    if (!empty($_SERVER['HTTP_CLIENT_IP'])){   //check ip from share internet
      $ip=$_SERVER['HTTP_CLIENT_IP'];
    }elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])){   //to check ip is pass from proxy
      $ip=$_SERVER['HTTP_X_FORWARDED_FOR'];
    }else{
      $ip=$_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}

$requesterIP = getIP();
if(strpos($requesterIP, '204.232.175') === false && strpos($requesterIP, '192.30.25') === false){
    echo 'IP Address not accepted<br />';
    echo $requesterIP;
    die();
}


### Deployment ###
$deployment = `/bin/bash /home/microbiome-tracker/serve/deploy.sh 2>&1`;

$message = '';
if(strpos($deployment, "No new code to deploy") === False){
    $message .=  "Deployment\n\n";
    $message .=  $deployment;
}

echo $message;
echo '<br />';

if($message != ''){
    $to = 'admin@microbiome.mit.edu';
    $subject = 'Deployment Log';
    $headers = "From: " . strip_tags('deploy@microbiome.mit.edu') . "\r\n";

    mail($to, $subject, $message, $headers);
    echo '<b>Mail Sent</b>';
}else{
    echo 'No deployments done';
}
?>
