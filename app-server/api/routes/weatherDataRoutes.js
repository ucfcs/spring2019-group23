'use strict';
var express = require('express'),
    weatherData = require('../controllers/weatherDataController');

var router = express.Router();

// weatherData Routes
router.route('/')
  .get(weatherData.get_latest);

router.route('/range')
  .get(weatherData.get_range);

module.exports = router;