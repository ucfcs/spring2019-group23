var express = require('express'),
  mongoose = require('mongoose'),
  bodyParser = require('body-parser'),
  path = require('path'),
  http = require('http'),
  webSocket = require('ws'),
  cors = require('cors'),
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
  mongodb = process.env.MONGODB_URI || 'mongodb://localhost/cloudtracking';

function init_schema() {
  require('./api/models/cloudCoverageModel')
  require('./api/models/cloudMotionModel')
  require('./api/models/weatherDataModel')
}

function init_routes() {
  var cloudCoverageRoute = require('./api/routes/cloudCoverageRoutes'),
    cloudMotionRoute = require('./api/routes/cloudMotionRoutes'),
    livestreamRoute = require('./api/routes/livestreamRoutes')(socketServer),
    weatherDataRoute = require('./api/routes/weatherDataRoutes');

  app.use('/coverage', cloudCoverageRoute)
  app.use('/weather', weatherDataRoute) 
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
    client.on('predi', (data) => {
      require('./api/controllers/cloudMotionController').create(data)
      client.broadcast.emit('predi', data.cloudPrediction)
    })

    client.on('data', (data) => {
      require('./api/controllers/weatherDataController').create(data)
      client.broadcast.emit('data', data)
    })
    
    client.on('coverage_data', (data) => {
      require('./api/controllers/cloudCoverageController').create(data)
      client.broadcast.emit('coverage_data', data)
    })
    
    client.on('coverage', (frame) => {
      client.broadcast.emit('coverage', "data:image/png;base64,"+ frame.toString("base64"))
    })

    client.on('shadow', (frame) => {
      client.broadcast.emit('shadow', "data:image/png;base64,"+ frame.toString("base64"))
    })

    client.on('error', (err) => {
      console.log("Error from client: ", client.id);
      console.log(err)
    });
  });
  
  init_schema()
  init_routes()

  app.use(bodyParser.json());
  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(express.static(path.join(__dirname, 'front_end/build')));
  app.get('/*', function (req, res) {
    res.sendFile(path.join(__dirname, 'front_end/build', 'index.html'));
  });

  streamServer.listen(port);
  console.log('REST API server started on: ' + port);
}

init();
