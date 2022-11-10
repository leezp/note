' downloadfile.vbs 

' Set your settings

strFileURL = "http://img5.cache.netease.com/photo/0001/2013-03-28/8R1BK3QO3R710001.jpg"

strHDLocation = "b.jpg" 'C:\\(sss.txt)

' Fetch the file

Set objXMLHTTP = CreateObject("MSXML2.XMLHTTP")

objXMLHTTP.open "GET", strFileURL, false

objXMLHTTP.send()

If objXMLHTTP.Status = 200 Then

Set objADOStream = CreateObject("ADODB.Stream")

objADOStream.Open

objADOStream.Type = 1 'adTypeBinary

objADOStream.Write objXMLHTTP.ResponseBody

objADOStream.Position = 0 'Set the stream position to the start

Set objFSO = Createobject("Scripting.FileSystemObject")

If objFSO.Fileexists(strHDLocation) Then objFSO.DeleteFile strHDLocation

Set objFSO = Nothing

objADOStream.SaveToFile strHDLocation

objADOStream.Close

Set objADOStream = Nothing

End if

Set objXMLHTTP = Nothing