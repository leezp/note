<?php $result["status"] = base64_encode("success");
    $result["msg"] = base64_encode("k221343dsiudniufff13232");

   
	$data=json_encode($result);
	//$data=$result["status"];
	$key=e45e329feb5d925b;
	for($i=0;$i<strlen($data);$i++) {
    			 $data[$i] = $data[$i]^$key[$i+1&15]; 
    			}
				echo $data;
				for($i=0;$i<strlen($data);$i++) {
    			 $data[$i] = $data[$i]^$key[$i+1&15]; 
    			}
				echo $data;
				
	?>