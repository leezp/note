oldifs="$IFS"
IFS=$'\n'


for LINE in `ps -aux |ts | grep -v  "TIME COMMAND"`
do	
	pid=$(echo $LINE | awk '{print $5}')

	if [ "$pid" -gt "1" ];then
		netinfo=$(netstat -anp | grep tcp | grep ESTABLISHED | grep "$pid/" | grep -v grep | awk '{print $4,$5,$7}')
                
		if [ -n "$netinfo" ]; then
			local_net=$(echo $netinfo | awk '{print $1}')
			local_ip=$(echo $local_net | awk -F: '{print $1}')
			local_port=$(echo $local_net | awk -F: '{print $2}')	
			foreign_net=$(echo $netinfo | awk '{print $2}')
			foreign_ip=$(echo $foreign_net | awk -F: '{print $1}')
			foreign_port=$(echo $foreign_net | awk -F: '{print $2}')
			pidname=$(echo $netinfo | awk '{print $3}')
			tmppid=$(echo $pidname | awk -F'/' '{print $1}')
			if [ "$local_port" -gt "10000" ] && [ "$tmppid" = "$pid" ]; then
				echo "$LINE $local_ip $local_port $foreign_ip $foreign_port" | jq -cR '[splits(" +")] |  {"month":.[0],"date":.[1],"times":.[2],"USER":.[3],"PID":.[4],"%CPU":.[5]|tonumber,"%MEM":.[6]|tonumber,"VSZ":.[7]|tonumber,"RSS":.[8]|tonumber,"TTY":.[9],"STAT":.[10],"START":.[11],"TIME":.[12],"COMMAND":.[13],"SIP":.[-4],"SPORT":.[-3],"DIP":.[-2],"DPORT":.[-1] }'||echo 'throw an error'
			fi
		fi
	fi
done
IFS="$oldifs"


