<?php 
$name = $_POST['name'];
$email = $_POST['email'];
$message = $_POST['message'];
$formcontent="From: $name\nMessage: $message";
$recipient = "jessi.lynn.cook@gmail.com";
$subject = "Email Saga Contact Form";
$mailheader = "From: $email \r\n";
mail($recipient, $subject, $formcontent, $mailheader) or die("Error!");
echo "<script type='text/javascript'>location.href = '../index.html';</script>";
?>
