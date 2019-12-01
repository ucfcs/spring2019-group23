'use strict';
var express = require('express'),
    cloudCoverage = require('../controllers/cloudCoverageController');

var router = express.Router();

// cloudCoverage Routes
router.route('/')
  .get(cloudCoverage.get_latest);

router.route('/range')
  .get(cloudCoverage.get_range);

module.exports = router;