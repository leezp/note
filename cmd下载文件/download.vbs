iLocal=LCase(Wscript.Arguments(1))
iRemote=LCase(Wscript.Arguments(0))
Set xPost=createObject("Microsoft.XMLHTTP")
xPost.Open "GET",iRemote,0
xPost.Send()
set sGet=createObject("ADODB.Stream")
sGet.Mode=3
sGet.Type=1
sGet.Open()
sGet.Write xPost.ResponseBody
sGet.SaveToFile iLocal,2