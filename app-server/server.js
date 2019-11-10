var express = require('express'),
  mongoose = require('mongoose'),
  bodyParser = require('body-parser'),
  path = require('path'),
  http = require('http'),
  webSocket = require('ws'),
  fs = require('fs'),
  socketIO = require('socket.io');

if (process.env.NODE_ENV !== 'production'){
  require('longjohn');
}

var app = express(),
  streamServer = http.createServer(app),
  socketio = socketIO(streamServer),
  socketServer = new webSocket.Server({ server: streamServer, path: '/stream' }),
  port = process.env.PORT || 3001,
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
  app.use('/cloudtrackinglivestream', livestreamRoute)
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

  socketio.on('connection', (client) => {
    console.log("Connection from client");
    client.on('disconnect', () => console.log('Client disconnected'));
    
    client.on('data', (data) => {
      // TODO: Archive this weather data as it comes in
      client.broadcast.emit('data', data)
    })  

    client.on('image', (frame) => {
      client.broadcast.emit('image', "data:image/png;base64,"+ frame.toString("base64"))
    })

    client.on('error', (err) => {
      console.log("Error from client: ", client.id);
      console.log(err)
    });
  });

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