'use strict';
var express = require('express'),
    cloudMotion = require('../controllers/cloudMotionController');

var router = express.Router();

// cloudMotion Routes
router.route('/')
  .get(cloudMotion.get_latest_motion)
  .post(cloudMotion.create_motion);

module.exports = router
