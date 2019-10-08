var express = require('express'),
  app = express(),
  port = process.env.PORT || 3000,
  mongoose = require('mongoose'),
  CloudActivity = require('./api/models/cloudActivityModel'), //created model loading here
  bodyParser = require('body-parser');
  
// mongoose instance connection url connection
mongoose.Promise = global.Promise;
mongoose.connect('mongodb://localhost/cloudtracking', {useNewUrlParser: true, useUnifiedTopology: true}); 

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

var routes = require('./api/routes/cloudActivityRoutes'); //importing  route
routes(app); //register the route

app.listen(port);
console.log('REST API server started on: ' + port);