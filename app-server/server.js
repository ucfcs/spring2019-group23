const express = require('express'),
      mongoose = require('mongoose'),
      bodyParser = require('body-parser');

const app = express(),
      port = process.env.PORT || 3000,
      mongodb = 'mongodb://localhost/cloudtracking';

function init_schema() {
  require('./api/models/cloudActivityModel')
  require('./api/models/cloudMotionModel')
}

function init_routes () {
  var cloudActivityRoute = require('./api/routes/cloudActivityRoutes'),
      cloudMotionRoute = require('./api/routes/cloudMotionRoutes');
  app.use('/activity', cloudActivityRoute)
  app.use('/motion', cloudMotionRoute)
}

function init() {
  mongoose.Promise = global.Promise
  mongoose.connect(mongodb, {useNewUrlParser: true, useUnifiedTopology: true},
    function(err, db) {
      if (err) {
          console.log('Unable to connect to the mongodb server. Please start the mongo daemon. Error:', err);
      } else {
          console.log('Connected to mongodb server successfully!');
      }
  });

  app.use(bodyParser.json());
  app.use(bodyParser.urlencoded({ extended: true }));

  init_schema()
  init_routes()

  app.listen(port);
  console.log('REST API server started on: ' + port);
}

init()