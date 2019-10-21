var express = require('express'),
  mongoose = require('mongoose'),
  bodyParser = require('body-parser'),
  path = require('path'),
  http = require('http'),
  webSocket = require('ws');

var app = express(),
  streamServer = http.createServer(app),
  socketServer = new webSocket.Server({ server: streamServer }),
  port = process.env.PORT || 3000,
  mongodb = 'mongodb://localhost/cloudtracking';

function init_schema() {
  require('./api/models/cloudActivityModel')
  require('./api/models/cloudMotionModel')
}

function init_routes() {
  var cloudActivityRoute = require('./api/routes/cloudActivityRoutes'),
    cloudMotionRoute = require('./api/routes/cloudMotionRoutes'),
    livestreamRoute = require('./api/routes/livestreamRoutes')(socketServer);
  app.use('/activity', cloudActivityRoute)
  app.use('/motion', cloudMotionRoute)
  app.use('/uploadmayb', livestreamRoute)
}

function init() {
  mongoose.Promise = global.Promise
  mongoose.connect(mongodb, { useNewUrlParser: true, useUnifiedTopology: true },
    function (err, db) {
      if (err) {
        console.log('Unable to connect to the mongodb server. Please start the mongo daemon. Error:', err);
      } else {
        console.log('Connected to mongodb server successfully!');
      }
    });

  socketServer.broadcast = function (data) {
    socketServer.clients.forEach(function each(client) {
      if (client.readyState === webSocket.OPEN) {
        client.send(data);
      }
    });
  };

  app.use(bodyParser.json());
  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(express.static(path.join(__dirname, '/front_end/build')));
  app.get('/*', function (req, res) {
    res.sendFile(path.join(__dirname, '/front_end/build', 'index.html'));
  });

  init_schema()
  init_routes()

  streamServer.listen(port);
  console.log('REST API server started on: ' + port);
}

init();