<h2>HTTP tunnel for node.js</h2>
<h3>
Objective
</h3>
Tunnel arbitrary TCP connections through HTTP.
<h3>
Security
</h3>
Use an SSH tunnel over the HTTP tunnel
<h3>
Forward ports over the HTTP tunnel
</h3>
Use an SSH tunnel over the HTTP tunnel
<h3>
How to use
</h3>
<code>
# On server outside the firewall
./server &
disown
exit

# On your machine inside the firewall
./client # This sets up a SOCKS5 server on your local machine

# Use with SSH
ssh <your normal options> -o ProxyCommand "./ssh-connect <address of tunnelling server> %h %p"

# pwnt.
</code>
