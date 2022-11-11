var es = require('event-stream');
var events = require('events');
var util = require('util');


exports.Encoder = function() {
  return es.map(function(d, cb) {
    cb(null, d.toString('base64'));
  });
  // Requires that d is a buffer
}

exports.Decoder = function() {
  return es.map(function(d, cb) {
    cb(null, new Buffer(d.toString(), 'base64'));
  });
  // Requires that d is a buffer
}


