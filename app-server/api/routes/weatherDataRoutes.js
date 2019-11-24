'use strict';
var express = require('express'),
    weatherData = require('../controllers/weatherDataController');

var router = express.Router();

// weatherData Routes
router.route('/')
  .get(weatherData.get_latest);

module.exports = router;