function Invoke-Conveigh
{
<#
.SYNOPSIS
Invoke-Conveigh is a Windows PowerShell LLMNR/NBNS spoofer detection tool.

.DESCRIPTION
Invoke-Conveigh is a Windows PowerShell LLMNR/NBNS spoofer detection tool with the following features:

    Generates and sends IPv4 LLMNR/NBNS requests with random or set hostnames
    Detects responses to sent IPv4 LLMNR/NBNS requests using a packet sniffer
    Optionally displays all received IPv4 LLMNR/NBNS requests using a packet sniffer
    File output 
    Run time control

LLMNR/NBNS requests sent by Conveigh are not legitimate requests to any enabled LLMNR/NBNS services. The requests
will not result in name resolution in the event that a spoofer is present.

Conveigh requires an elevated shell and will work with the local LLMNR/NBNS services either enabled or disabled.

.PARAMETER CaptureRequests
Default = Disabled: (Y/N) Enable/Disable displaying and logging all received LLMNR/NBNS requests.

.PARAMETER IP
Set local IP address for the packet sniffer.

.PARAMETER Hostnames
Array of hostnames that will be randomly selected for LLMNR/NBNS requests. Hostnames must meet NBNS hostname
requirements. If this parameter is not used, hostnames will be randomly generated.

.PARAMETER MaxSendRequestTime
Default = 30 Minutes: Set the maximum random time in minutes for sending LLMNR/NBNS requests.

.PARAMETER FileOutput
Default = Disabled: (Y/N) Enable/Disable log file output.

.PARAMETER OutputDir
Default = Working Directory: Set a valid path to an output directory for log and capture files. FileOutput must
also be enabled.

.PARAMETER RunTime
(Integer) Set the run time duration in hours.
  
.EXAMPLE
Import-Module .\Conveigh.ps1;Invoke-Conveigh
Import full module and execute with all default settings.

Invoke-Conveigh -Hostnames host1,host2,host3 -RunTime 8
Execute with a list of three hostnames and a run time of 8 hours.

.LINK
https://github.com/Kevin-Robertson/Conveigh
#>

# Parameter default values can be modified in this section: 
[CmdletBinding()]
param
( 
    [parameter(Mandatory=$false)][ValidateSet("Y","N")][String]$FileOutput="N",
    [parameter(Mandatory=$false)][ValidateSet("Y","N")][String]$CaptureRequests="Y",
    [parameter(Mandatory=$false)][ValidateScript({$_ -match [System.Net.IPAddress]$_})][String]$IP="",
    [parameter(Mandatory=$false)][ValidateScript({Test-Path $_})][String]$OutputDir="",
    [parameter(Mandatory=$false)][ValidateScript({$_ -ge 2})][Int]$MaxSendRequestTime="30",
    [parameter(Mandatory=$false)][Int]$RunTime="",
    [parameter(Mandatory=$false)][Array]$Hostnames="",
    [parameter(ValueFromRemainingArguments=$true)]$invalid_parameter
)

if ($invalid_parameter)
{
    throw "$($invalid_parameter) is not a valid parameter."
}

if(!$IP)
{ 
    $IP = (Test-Connection 127.0.0.1 -count 1 | Select-Object -ExpandProperty Ipv4Address)
}

if(!$OutputDir)
{ 
    $output_directory = $PWD.Path
}
else
{
    $output_directory = $OutputDir
}

if(!$conveigh)
{
    $conveigh = [HashTable]::Synchronized(@{})
    $conveigh.log = New-Object System.Collections.ArrayList
}

$conveigh.console_queue = New-Object System.Collections.ArrayList
$conveigh.log_file_queue = New-Object System.Collections.ArrayList
$conveigh.file_output = $false
$conveigh.log_out_file = $output_directory + "\Conveigh-Log.txt"
$conveigh.running = $true

If (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator"))
{    
    Throw "This script needs to be run in an elevated shell to enable the packet sniffer."
}

# Write startup messages
Write-Output "Conveigh started at $(Get-Date -format 's')"
$conveigh.log_file_queue.Add("$(Get-Date -format 's') - Conveigh started") > $null

Write-Output "Packet Sniffer IP Address = $IP"
Write-Output "Max Send Request Time = $MaxSendRequestTime Minutes"

if($CaptureRequests -eq 'Y')
{
    Write-Output "Display/Log Incoming LLMNR/NBNS Requests = Enabled"
}
else
{
    Write-Output "Display/Log Incoming LLMNR/NBNS Requests = Disabled"
}

if($FileOutput -eq 'Y')
{
    Write-Output "File Output = Enabled"
    Write-Output "Output Directory = $output_directory"
    $conveigh.file_output = $true
}
else
{
    Write-Output "File Output = Disabled"
}

if($RunTime)
{
    $conveigh_timeout = New-TimeSpan -Hours $RunTime
    $conveigh_stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

    if($RunTime -eq 1)
    {
        Write-Output "Run Time = $RunTime Hour"
    }
    elseif($RunTime -gt 1)
    {
        Write-Output "Run Time = $RunTime Hours"
    }

}

Write-Output "Press CTRL+C to exit`n"

# Begin ScriptBlocks

# Shared Basic Functions ScriptBlock
$shared_basic_functions_scriptblock =
{

    function DataToUInt16($field)
    {
	   [Array]::Reverse($field)
	   return [System.BitConverter]::ToUInt16($field,0)
    }

    function DataToUInt32($field)
    {
	   [Array]::Reverse($field)
	   return [System.BitConverter]::ToUInt32($field,0)
    }

}

$LLMNR_request_scriptblock = 
{
    param ($Hostnames,$MaxSendRequestTime)

    $LLMNR_request_random = 0
    $LLMNR_request_timeout = New-TimeSpan -Minutes $LLMNR_request_random
    $LLMNR_request_stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
    
    while($conveigh.running)
    {
        
        if($LLMNR_request_stopwatch.Elapsed -ge $LLMNR_request_timeout)
        {
            $LLMNR_request_random = Get-Random -Minimum 1 -Maximum $MaxSendRequestTime
            $LLMNR_request_timeout = New-TimeSpan -Minutes $LLMNR_request_random
            $LLMNR_request_stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
            $conveigh.LLMNR_transaction_ID_bytes = [String](1..2 | ForEach-Object {"{0:X2}" -f (Get-Random -Minimum 1 -Maximum 255)})
            $conveigh.LLMNR_transaction_ID_bytes = $conveigh.LLMNR_transaction_ID_bytes.Split(" ") | ForEach-Object{[Char][System.Convert]::ToInt16($_,16)}
            $LLMNR_UDP_client = new-Object System.Net.Sockets.UdpClient 

            if($Hostnames)
            {
                $LLMNR_hostname = $Hostnames[(Get-Random -Minimum 0 -Maximum $Hostnames.Count)]
            }
            else
            {
                $LLMNR_hostname_random_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".ToCharArray()
                [String]$LLMNR_hostname = Get-Random -Count (Get-Random -Minimum 5 -Maximum 10) -Input $LLMNR_hostname_random_characters
                $LLMNR_hostname = $LLMNR_hostname -replace " ",""
            }

            [Byte[]]$LLMNR_hostname_bytes = [System.Text.Encoding]::UTF8.GetBytes($LLMNR_hostname)

            $LLMNR_request_packet = $conveigh.LLMNR_transaction_ID_bytes +
                                     0x00,0x00,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00 +
                                     $LLMNR_hostname_bytes.Length +
                                     $LLMNR_hostname_bytes +
                                     0x00,0x00,0x01,0x00,0x01

            $LLMNR_destination_endpoint = New-Object System.Net.IPEndpoint([IPAddress]"224.0.0.252",5355)
            $LLMNR_UDP_client.Connect($LLMNR_destination_endpoint)
            $LLMNR_UDP_client.Send($LLMNR_request_packet,$LLMNR_request_packet.Length)
            $conveigh.LLMNR_UDP_client_port = ($LLMNR_UDP_client.Client.LocalEndPoint).Port
            $LLMNR_UDP_client.Close()
            $conveigh.console_queue.Add("$(Get-Date -format 's') - LLMNR request for $LLMNR_hostname sent to 224.0.0.252")
            $conveigh.log_file_queue.Add("$(Get-Date -format 's') - LLMNR request for $LLMNR_hostname sent to 224.0.0.252")

            Start-Sleep -m 100

            if($LLMNR_request_random -eq 1)
            {
                $conveigh.console_queue.Add("$(Get-Date -format 's') - Next LLMNR request will be sent in $LLMNR_request_random minute")
            }
            else
            {
                $conveigh.console_queue.Add("$(Get-Date -format 's') - Next LLMNR request will be sent in $LLMNR_request_random minutes")
            }

        }

        Start-Sleep -m 100
    }

    $LLMNR_UDP_client.Close()
 }

$NBNS_request_scriptblock = 
{
    param ($Hostnames,$MaxSendRequestTime)

    $NBNS_request_random = 0
    $NBNS_request_timeout = New-Timespan -Minutes $NBNS_request_random
    $NBNS_request_stopwatch = [System.Diagnostics.Stopwatch]::StartNew()

    while($conveigh.running)
    {

        if($NBNS_request_stopwatch.Elapsed -ge $NBNS_request_timeout)
        {
            $NBNS_request_random = Get-Random -Minimum 1 -Maximum $MaxSendRequestTime
            $NBNS_request_timeout = New-TimeSpan -Minutes $NBNS_request_random
            $NBNS_request_stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
            $conveigh.NBNS_transaction_ID_bytes = [String](1..2 | ForEach-Object {"{0:X2}" -f (Get-Random -Minimum 1 -Maximum 255)})
            $conveigh.NBNS_transaction_ID_bytes = $conveigh.NBNS_transaction_ID_bytes.Split(" ") | ForEach-Object{[Char][System.Convert]::ToInt16($_,16)}
            $NBNS_UDP_client = new-Object System.Net.Sockets.UdpClient 137

            if($Hostnames)
            {
                $NBNS_hostname = $Hostnames[(Get-Random -Minimum 0 -Maximum $Hostnames.Count)]
                $NBNS_hostname = $NBNS_hostname.ToUpper()
            }
            else
            {
                $NBNS_hostname_random_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".ToCharArray()
                [String]$NBNS_hostname = Get-Random -Count (Get-Random -Minimum 5 -Maximum 10) -Input $NBNS_hostname_random_characters
                $NBNS_hostname = $NBNS_hostname -replace " ",""
            }

            $NBNS_hostname_bytes = 0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,
                              0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x43,0x41,0x41,0x41,0x00

            $NBNS_hostname_encoded = [System.Text.Encoding]::UTF8.GetBytes($NBNS_hostname)
            $NBNS_hostname_encoded = [System.BitConverter]::ToString($NBNS_hostname_encoded)
            $NBNS_hostname_encoded = $NBNS_hostname_encoded.Replace("-","")
            $NBNS_hostname_encoded = [System.Text.Encoding]::UTF8.GetBytes($NBNS_hostname_encoded)

            for($i=0; $i -lt $NBNS_hostname_encoded.Count; $i++)
            {

                if($NBNS_hostname_encoded[$i] -gt 64)
                {
                    $NBNS_hostname_bytes[$i] = $NBNS_hostname_encoded[$i] + 10
                }
                else
                {
                    $NBNS_hostname_bytes[$i] = $NBNS_hostname_encoded[$i] + 17
                }
    
            }

            $NBNS_request_packet = $conveigh.NBNS_transaction_ID_bytes +
                                    0x01,0x10,0x00,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x20 +
                                    $NBNS_hostname_bytes +
                                    0x00,0x20,0x00,0x01

            $NBNS_destination_endpoint = New-Object System.Net.IPEndpoint([IPAddress]::broadcast,137)
            $NBNS_UDP_client.Connect($NBNS_destination_endpoint)
            $NBNS_UDP_client.Send($NBNS_request_packet,$NBNS_request_packet.Length)
            $conveigh.NBNS_UDP_client_port = ($LLMNR_UDP_client.Client.LocalEndPoint).Port
            $NBNS_UDP_client.Close()
            $conveigh.console_queue.Add("$(Get-Date -format 's') - NBNS request for $NBNS_hostname sent to " + $NBNS_destination_endpoint.Address.IPAddressToString)
            $conveigh.log_file_queue.Add("$(Get-Date -format 's') - NBNS request for $NBNS_hostname sent to " + $NBNS_destination_endpoint.Address.IPAddressToString)

            Start-Sleep -m 100

            if($NBNS_request_random -eq 1)
            {
                $conveigh.console_queue.Add("$(Get-Date -format 's') - Next NBNS request will be sent in $NBNS_request_random minute")
            }
            else
            {
                $conveigh.console_queue.Add("$(Get-Date -format 's') - Next NBNS request will be sent in $NBNS_request_random minutes")
            }

        }

        Start-Sleep -m 100
    }

    $NBNS_UDP_client.Close()
 }

# Sniffer/Spoofer ScriptBlock - LLMNR/NBNS Spoofer and SMB sniffer
$sniffer_scriptblock = 
{
    param ($IP,$CaptureRequests)

    $byte_in = New-Object System.Byte[] 4	
    $byte_out = New-Object System.Byte[] 4	
    $byte_data = New-Object System.Byte[] 4096
    $byte_in[0] = 1
    $byte_in[1-3] = 0
    $byte_out[0] = 1
    $byte_out[1-3] = 0
    $conveigh.sniffer_socket = New-Object System.Net.Sockets.Socket([Net.Sockets.AddressFamily]::InterNetwork,[Net.Sockets.SocketType]::Raw,[Net.Sockets.ProtocolType]::IP)
    $conveigh.sniffer_socket.SetSocketOption("IP","HeaderIncluded",$true)
    $conveigh.sniffer_socket.ReceiveBufferSize = 1024
    $end_point = New-Object System.Net.IPEndpoint([System.Net.IPAddress]"$IP",0)
    $conveigh.sniffer_socket.Bind($end_point)
    $conveigh.sniffer_socket.IOControl([System.Net.Sockets.IOControlCode]::ReceiveAll,$byte_in,$byte_out)

    while($conveigh.running)
    {
        $packet_data = $conveigh.sniffer_socket.Receive($byte_data,0,$byte_data.Length,[System.Net.Sockets.SocketFlags]::None)
        $memory_stream = New-Object System.IO.MemoryStream($byte_data,0,$packet_data)
        $binary_reader = New-Object System.IO.BinaryReader($memory_stream)
        $version_HL = $binary_reader.ReadByte()
        $type_of_service= $binary_reader.ReadByte()
        $total_length = DataToUInt16 $binary_reader.ReadBytes(2)
        $identification = $binary_reader.ReadBytes(2)
        $flags_offset = $binary_reader.ReadBytes(2)
        $TTL = $binary_reader.ReadByte()
        $protocol_number = $binary_reader.ReadByte()
        $header_checksum = [System.Net.IPAddress]::NetworkToHostOrder($binary_reader.ReadInt16())
        $source_IP_bytes = $binary_reader.ReadBytes(4)
        $source_IP = [System.Net.IPAddress]$source_IP_bytes
        $destination_IP_bytes = $binary_reader.ReadBytes(4)
        $destination_IP = [System.Net.IPAddress]$destination_IP_bytes
        $IP_version = [Int]"0x$(('{0:X}' -f $version_HL)[0])"
        $header_length = [Int]"0x$(('{0:X}' -f $version_HL)[1])" * 4
        
        switch($protocol_number)
        {
                
            17 
            {  # UDP
                $source_port =  $binary_reader.ReadBytes(2)
                $endpoint_source_port = DataToUInt16 ($source_port)
                $destination_port = DataToUInt16 $binary_reader.ReadBytes(2)
                $UDP_length = $binary_reader.ReadBytes(2)
                $UDP_length_uint  = DataToUInt16 ($UDP_length)
                $binary_reader.ReadBytes(2)
                $payload_bytes = $binary_reader.ReadBytes(($UDP_length_uint - 2) * 4)

                # Incoming packets 
                switch ($destination_port)
                {

                    137 # NBNS
                    {
                        if(($payload_bytes[5] -eq 1 -or [System.BitConverter]::ToString($conveigh.NBNS_transaction_ID_bytes) -eq [System.BitConverter]::ToString($payload_bytes[0..1])) -and $IP -ne $source_IP)
                        {
                            $NBNS_query_type = [System.BitConverter]::ToString($payload_bytes[43..44])
                    
                            switch ($NBNS_query_type)
                            {

                                '41-41'
                                {
                                    $NBNS_query_type = '00'
                                }

                                '41-44'
                                {
                                    $NBNS_query_type = '03'
                                }

                                '43-41'
                                {
                                    $NBNS_query_type = '20'
                                }

                                '42-4C'
                                {
                                    $NBNS_query_type = '1B'
                                }

                                '42-4D'
                                {
                                    $NBNS_query_type = '1C'
                                }

                                '42-4E'
                                {
                                    $NBNS_query_type = '1D'
                                }

                                '42-4F'
                                {
                                    $NBNS_query_type = '1E'
                                }

                            }

                            $NBNS_query = [System.BitConverter]::ToString($payload_bytes[13..($payload_bytes.Length - 4)])
                            $NBNS_query = $NBNS_query -replace "-00",""
                            $NBNS_query = $NBNS_query.Split("-") | ForEach-Object{[Char][System.Convert]::ToInt16($_,16)}
                            $NBNS_query_string_encoded = New-Object System.String ($NBNS_query,0,$NBNS_query.Length)
                            $NBNS_query_string_encoded = $NBNS_query_string_encoded.Substring(0,$NBNS_query_string_encoded.IndexOf("CA"))
                            $NBNS_query_string_subtracted = ""
                            $NBNS_query_string = ""
                            $n = 0
                            
                            do
                            {
                                $NBNS_query_string_sub = (([Byte][Char]($NBNS_query_string_encoded.Substring($n,1))) - 65)
                                $NBNS_query_string_subtracted += ([System.Convert]::ToString($NBNS_query_string_sub,16))
                                $n += 1
                            }
                            until($n -gt ($NBNS_query_string_encoded.Length - 1))
                    
                            $n = 0
                    
                            do
                            {
                                $NBNS_query_string += ([Char]([System.Convert]::ToInt16($NBNS_query_string_subtracted.Substring($n,2),16)))
                                $n += 2
                            }
                            until($n -gt ($NBNS_query_string_subtracted.Length - 1) -or $NBNS_query_string.Length -eq 15)
                            
                            if($CaptureRequests -eq 'Y' -and $payload_bytes[5] -eq 1)
                            {
                                $conveigh.console_queue.Add("$(Get-Date -format 's') - NBNS request for $NBNS_query_string<$NBNS_query_type> received from $source_IP")
                                $conveigh.log_file_queue.Add("$(Get-Date -format 's') - NBNS request for $NBNS_query_string<$NBNS_query_type> received from $source_IP")
                            }
                            elseif([System.BitConverter]::ToString($conveigh.NBNS_transaction_ID_bytes) -eq [System.BitConverter]::ToString($payload_bytes[0..1]))
                            {
                                [byte[]]$NBNS_response_IP_bytes = $payload_bytes[($payload_bytes.Length - 4)..($payload_bytes.Length)]
                                $NBNS_response_IP = [System.Net.IPAddress]$NBNS_response_IP_bytes
                                $NBNS_response_IP = $NBNS_response_IP.IPAddressToString
                                Start-Sleep -m 5
                                $conveigh.console_queue.Add("$(Get-Date -format 's') - NBNS spoofer detected at $source_IP")
                                $conveigh.log_file_queue.Add("$(Get-Date -format 's') - NBNS spoofer detected at $source_IP")
                                $conveigh.console_queue.Add("$(Get-Date -format 's') - NBNS response $NBNS_response_IP for $NBNS_query_string<$NBNS_query_type> received from $source_IP")
                                $conveigh.log_file_queue.Add("$(Get-Date -format 's') - NBNS response $NBNS_response_IP for $NBNS_query_string<$NBNS_query_type> received from $source_IP")
                            }

                        }
                        
                    }

                    5355 # LLMNR
                    {

                        if($CaptureRequests -eq 'Y' -and $source_IP -ne $IP -and [System.BitConverter]::ToString($payload_bytes[($payload_bytes.Length - 4)..($payload_bytes.Length - 3)]) -ne '00-1c') # ignore AAAA for now
                        {
                            $LLMNR_query = [System.BitConverter]::ToString($payload_bytes[13..($payload_bytes.Length - 4)])
                            $LLMNR_query = $LLMNR_query -replace "-00",""

                            if($LLMNR_query.Length -eq 2)
                            {
                                $LLMNR_query = [Char][System.Convert]::ToInt16($LLMNR_query,16)
                                $LLMNR_query_string = New-Object System.String($LLMNR_query)
                            }
                            else
                            {
                                $LLMNR_query = $LLMNR_query.Split("-") | ForEach-Object{[Char][System.Convert]::ToInt16($_,16)}
                                $LLMNR_query_string = New-Object System.String($LLMNR_query,0,$LLMNR_query.Length)
                            }

                            $conveigh.console_queue.Add("$(Get-Date -format 's') - LLMNR request for $LLMNR_query_string received from $source_IP")
                            $conveigh.log_file_queue.Add("$(Get-Date -format 's') - LLMNR request for $LLMNR_query_string received from $source_IP")
                        }
                    }

                    $conveigh.LLMNR_UDP_client_port # LLMNR Random Port
                    {

                        if([System.BitConverter]::ToString($conveigh.LLMNR_transaction_ID_bytes) -eq [System.BitConverter]::ToString($payload_bytes[0..1]))
                        {
                            $LLMNR_query = [System.BitConverter]::ToString($payload_bytes[13..($payload_bytes[12] + 13)])
                            $LLMNR_query = $LLMNR_query -replace "-00",""

                            if($LLMNR_query.Length -eq 2)
                            {
                                $LLMNR_query = [Char][System.Convert]::ToInt16($LLMNR_query,16)
                                $LLMNR_query_string = New-Object System.String($LLMNR_query)
                            }
                            else
                            {
                                $LLMNR_query = $LLMNR_query.Split("-") | ForEach-Object{[Char][System.Convert]::ToInt16($_,16)}
                                $LLMNR_query_string = New-Object System.String($LLMNR_query,0,$LLMNR_query.Length)
                            }
                            
                            [byte[]]$spoofer_response_IP_bytes = $payload_bytes[($payload_bytes.Length - 4)..($payload_bytes.Length)]
                            $spoofer_response_IP = [System.Net.IPAddress]$spoofer_response_IP_bytes
                            $spoofer_response_IP = $spoofer_response_IP.IPAddressToString
                            Start-Sleep -m 5
                            $conveigh.console_queue.Add("$(Get-Date -format 's') - LLMNR spoofer detected at $source_IP")
                            $conveigh.log_file_queue.Add("$(Get-Date -format 's') - LLMNR spoofer detected at $source_IP")
                            $conveigh.console_queue.Add("$(Get-Date -format 's') - LLMNR response $spoofer_response_IP for $LLMNR_query_string received from $source_IP")
                            $conveigh.log_file_queue.Add("$(Get-Date -format 's') - LLMNR response $spoofer_response_IP for $LLMNR_query_string received from $source_IP")
                        }

                    }

                }

            }

        }

    }

    $binary_reader.Close()
    $memory_stream.Dispose()
    $memory_stream.Close()
}

# End ScriptBlocks

# Begin Startup Functions

# LLMNR Request Sender Startup Function
function LLMNR_request()
{
    $LLMNR_request_runspace = [RunspaceFactory]::CreateRunspace()
    $LLMNR_request_runspace.Open()
    $LLMNR_request_runspace.SessionStateProxy.SetVariable('conveigh',$conveigh)
    $LLMNR_request_powershell = [PowerShell]::Create()
    $LLMNR_request_powershell.Runspace = $LLMNR_request_runspace
    $LLMNR_request_powershell.AddScript($LLMNR_request_scriptblock).AddArgument($Hostnames).AddArgument($MaxSendRequestTime) > $null
    $LLMNR_request_powershell.BeginInvoke() > $null
}

# NBNS Request Sender Startup Function
function NBNS_request()
{
    $NBNS_request_runspace = [RunspaceFactory]::CreateRunspace()
    $NBNS_request_runspace.Open()
    $NBNS_request_runspace.SessionStateProxy.SetVariable('conveigh',$conveigh)
    $NBNS_request_powershell = [PowerShell]::Create()
    $NBNS_request_powershell.Runspace = $NBNS_request_runspace
    $NBNS_request_powershell.AddScript($NBNS_request_scriptblock).AddArgument($Hostnames).AddArgument($MaxSendRequestTime) > $null
    $NBNS_request_powershell.BeginInvoke() > $null
}

# Sniffer Startup Function
function Sniffer()
{
    $sniffer_runspace = [RunspaceFactory]::CreateRunspace()
    $sniffer_runspace.Open()
    $sniffer_runspace.SessionStateProxy.SetVariable('conveigh',$conveigh)
    $sniffer_powershell = [PowerShell]::Create()
    $sniffer_powershell.Runspace = $sniffer_runspace
    $sniffer_powershell.AddScript($shared_basic_functions_scriptblock) > $null
    $sniffer_powershell.AddScript($sniffer_scriptblock).AddArgument($IP).AddArgument($CaptureRequests) > $null
    $sniffer_powershell.BeginInvoke() > $null
}

# End Startup Functions

# Startup Services

Sniffer

Start-Sleep -m 5

LLMNR_request

NBNS_request

#Console Loop
:console_loop while($conveigh.running)
{
    
    if($conveigh.file_output)
    {

        while($conveigh.log_file_queue.Count -gt 0)
        {
            $conveigh.log_file_queue[0]|Out-File $conveigh.log_out_file -Append
            $conveigh.log_file_queue.RemoveRange(0,1)
        }

    }

    while($conveigh.console_queue.Count -gt 0)
    {

        switch -wildcard ($conveigh.console_queue[0])
        {

            "* spoofer detected *"
            {
                Write-Warning $conveigh.console_queue[0]
                $conveigh.console_queue.RemoveRange(0,1)
            }

            "* response *"
            {
                Write-Warning $conveigh.console_queue[0]
                $conveigh.console_queue.RemoveRange(0,1)
            }

            "* wpad*"
            {
                Write-Warning $conveigh.console_queue[0]
                $conveigh.console_queue.RemoveRange(0,1)
            }

            default
            {
                Write-Output $conveigh.console_queue[0]
                $conveigh.console_queue.RemoveRange(0,1)
            }

        } 

    }

    if($RunTime)
    {

        if($conveigh_stopwatch.Elapsed -ge $conveigh_timeout)
        {
            Write-Output "Conveigh exited due to run time at $(Get-Date -format 's')"
            
            if($conveigh.file_output)
            {
                $conveigh.log.Add($conveigh.log_file_queue[$conveigh.log_file_queue.Add("$(Get-Date -format 's') - Conveigh exited due to run time")]) > $null
            }
            
            Start-Sleep -m 100
            $conveigh.running = $false
        }

    }
    
    [Console]::TreatControlCAsInput = $true

    if($Host.UI.RawUI.KeyAvailable -and (3 -eq [int]$Host.UI.RawUI.ReadKey("AllowCtrlC,IncludeKeyUp,NoEcho").Character))
    {
        Write-Output "Conveigh exited at $(Get-Date -format 's')"
        
        if($conveigh.file_output)
        {
            $conveigh.log.Add($conveigh.log_file_queue[$conveigh.log_file_queue.Add("$(Get-Date -format 's') - Conveigh exited")]) > $null
        }

        Start-Sleep -m 100
        $conveigh.log_file_queue = $null
        $conveigh.running = $false
    }

    Start-Sleep -m 10
}

}