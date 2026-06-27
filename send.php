<?php
$to = "info@niddvalleybp.co.uk";
$redirect_success = "/contact/?sent=1";
$redirect_error   = "/contact/?error=1";

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header("Location: /contact/");
    exit;
}

function clean($val) {
    return htmlspecialchars(strip_tags(trim($val)), ENT_QUOTES, 'UTF-8');
}

$name     = clean($_POST['name']     ?? '');
$phone    = clean($_POST['phone']    ?? '');
$email    = clean($_POST['email']    ?? '');
$service  = clean($_POST['service']  ?? '');
$location = clean($_POST['location'] ?? '');
$message  = clean($_POST['message']  ?? '');

// Only name and phone are required
if (empty($name) || empty($phone)) {
    header("Location: $redirect_error");
    exit;
}

// Validate email only if provided
if (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    header("Location: $redirect_error");
    exit;
}

$subject = "New Enquiry from $name - Nidd Valley Building Preservation";

$body  = "You have a new enquiry from the website.\n\n";
$body .= "Name:     $name\n";
$body .= "Phone:    $phone\n";
$body .= "Email:    " . ($email ?: "Not provided") . "\n";
$body .= "Service:  $service\n";
$body .= "Location: $location\n\n";
$body .= "Message:\n$message\n";

$reply_to = !empty($email) ? $email : $to;

$headers  = "From: website@niddvalleybp.co.uk\r\n";
$headers .= "Reply-To: $reply_to\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

$sent = mail($to, $subject, $body, $headers);

header("Location: " . ($sent ? $redirect_success : $redirect_error));
exit;
