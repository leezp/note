var socks = require('node-socks/socks.js');
var http = require('http');

console.log('Establishing connection to localhost');
var tunnel_params = {address: 'www.behiring.com', port: 80};
var request = http.request({
    host: 'ec2-176-34-215-115.eu-west-1.compute.amazonaws.com',
    port: 3001,
    method: 'POST',
    path: '/'+(new Buffer(JSON.stringify(tunnel_params))).toString('base64')
  }, function(res) {
    res.on('data', function(d) {
      console.log('receiving data::'+d);
    });
    res.on('end', function() {
      console.log('The response ended');
    });
    res.on('close', function() {
      console.log('The tunnel closed');
    });
  }
);
request.write('Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla'+'Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla'+'Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla'+'Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla'+'Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla'+'Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla'+'Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla'+'Testing the HTTP tunnel. (1) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla');
request.write('Testing the HTTP tunnel. (2) This should have come out the other end. Bla bla bla bla bla bla bla bla bla bla bla bla');
