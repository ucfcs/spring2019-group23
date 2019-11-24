'use strict';
var express = require('express'),
    cloudMotion = require('../controllers/cloudMotionController');

var router = express.Router();

// cloudMotion Routes
router.route('/')
  .get(cloudMotion.get_latest)
  .post(cloudMotion.create_motion);

module.exports = router
