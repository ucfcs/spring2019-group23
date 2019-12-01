'use strict';
var express = require('express'),
    cloudMotion = require('../controllers/cloudMotionController');

var router = express.Router();

// cloudMotion Routes
router.route('/')
  .get(cloudMotion.get_latest)
  .post(cloudMotion.create_motion);

router.route('/range')
  .get(cloudMotion.get_range)

module.exports = router
