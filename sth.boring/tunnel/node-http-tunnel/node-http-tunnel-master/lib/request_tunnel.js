var http = require('http');
var net = require('net');
var es = require('event-stream');
var util = require('util');
var request = require('request');
var b64 = require('./base64stream');

function StreamEndpoint() {

  var $this = this;

  var highest_stream_id = 0, generate_stream_id = function() {
    highest_stream_id++;
    return highest_stream_id-1;
  }

  var streams_to_tunnel = {};
  var streams_to_world = {};

  this.send_queue = [];
  this.open_queue = {};

  this.multiplex_decapsulate = function(chunks) {
    // Responsible for keeping control of streams based on their current state, and some JSON data chunks

    var handlers = {
      'open': function(chunk, callback) {
        var pair = new_stream_pair({stream_id: chunk.stream_id});
        var socket = net.connect({port: chunk.port, host: chunk.host}, function() {
          console.log('made a TCP connection to '+chunk.host+':'+chunk.port);
          pair[0].pipe(socket).pipe(pair[1]);
          // Send acknowledgement so client doesn't have to send data into an abyss
          $this.send_queue.push({method: 'openAck', stream_id: chunk.stream_id});
        });
      },
      'openAck': function(chunk, callback) {
        callback = $this.open_queue[chunk.stream_id];
        if (callback) {
          callback();
          delete callback;
        }
      },
      'data': function(chunk, callback) {
        var s = streams_to_world[chunk.stream_id]
        s.write(chunk.data);
        callback()
      },
      'end': function(chunk, callback) {
        var s = streams_to_world[chunk.stream_id]
        s.end(chunk.data, callback);
        callback()
      },
      'close': function(chunk, callback) {
        var s = streams_to_world[chunk.stream_id]
        s.destroy();
        s.end(chunk.data, callback);
        callback()
      }
    }

    chunks.forEach(function(chunk) {
      handlers[chunk.method](chunk, function() {
      });
    });
  }

  var encapsulate = function(stream, d) {
    // Encodes one piece of data
    return {method: 'data', stream_id: stream.stream_id, data: d};
  }


  this._push_streams = function(to_tunnel, to_world) {
    // Pushes a pair of half-duplex streams into the tunnel

    if (!to_world) to_world = to_tunnel;


    if (typeof(to_world.stream_id) === 'undefined') {
      to_tunnel.stream_id = to_world.stream_id = generate_stream_id();
    }

    streams_to_tunnel[to_tunnel.stream_id] = to_tunnel;
    streams_to_world[to_world.stream_id] = to_world;


    to_tunnel.on('data', function(d) {
      $this.send_queue.push(encapsulate(to_tunnel, d));
    });

    to_tunnel.on('end', function(d) {
      $this.send_queue.push({method: 'end', stream_id: to_tunnel.stream_id, data: d});
    });

    to_tunnel.on('close', function() {
      $this.send_queue.push({method: 'close', stream_id: to_tunnel.stream_id});
    })
  }

  this.TCPConnection = function(hash, readyCallback) {
    var sp = new_stream_pair();
    $this.send_queue.push({method: 'open', stream_id: sp[0].stream_id, port: hash.port, host: hash.host});
    $this.open_queue[sp[0].stream_id] = function() {
      var result =  es.duplex(sp[1], sp[0]);
      readyCallback(result);
    };
  }

  var new_stream_pair = function(hash) {
    if (!hash) hash = {};

    // Returns a new full duplex stream that can piped to and from

    var to_tunnel = new b64.Encoder();
    var to_world = new b64.Decoder();

    if (typeof(hash.stream_id) !== 'undefined') {
      to_tunnel.stream_id = hash.stream_id;
      to_world.stream_id = hash.stream_id;
    }

    this._push_streams(to_tunnel, to_world);

    return [to_world, to_tunnel];
  }.bind(this);

  return this;

}

exports.createPersistentClient = function(tunnelServerHost, port, readyCallback) {

  var t = StreamEndpoint();

  t.interval = setInterval(function() {
    var buffer = new Buffer('');

    // Make the request
    var url = 'http://'+tunnelServerHost+':'+port+'/';
    var req = request.put(url); // In the future, we will use the url to determine whether to use long polling or not

    req.write(JSON.stringify(t.send_queue));
    req.end();
    t.send_queue = [];

    req.on('data', function(d) {
      buffer += d;
    });

    req.on('end', function(d) {

      var chunks;
      if (d) buffer += d;
        // Decode the data in the buffer
      //try {
        chunks = JSON.parse(buffer);
        t.multiplex_decapsulate(chunks);
      //} catch(err) {
        // TODO - wait in case the connection closed
      //}

    });

  }, 200);

  t.destroy = function() {
    clearInterval(this.interval);
  }

  // born ready
  process.nextTick(function() {
    readyCallback(t);
  });

  return t;

}

exports.createServer = function(connectionListner) {

  var t = StreamEndpoint();

  t.httpServer = http.createServer(function(req, res) {

    try {

      var buffer = new Buffer('');

      req.on('data', function(d) {
        buffer += d
      });

      req.on('end', function(d) {
        var chunks;
        if (d) buffer += d;
          // Decode the data in the buffer
        //try {
          chunks = JSON.parse(buffer);
          t.multiplex_decapsulate(chunks);
        //} catch(err) {
          // TODO - wait in case the connection closed
        //}

        // Send the responses
        res.writeHead(200);
        res.write(JSON.stringify(t.send_queue));
        res.end();

        t.send_queue = [];
      });

    } catch(err) {
      console.log(err);
    }
  });
  // The callback gets executed after our handlers


  t.httpServer.on('request', connectionListner.bind(t));
  t.listen = function(a1, a2) {
    t.httpServer.listen(a1, a2);
  }
  return t
}


