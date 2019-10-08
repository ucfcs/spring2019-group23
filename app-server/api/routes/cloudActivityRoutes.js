'use strict';
var express = require('express'),
    cloudActivity = require('../controllers/cloudActivityController');

var router = express.Router();

// cloudActivity Routes
router.route('/')
  .get(cloudActivity.get_all_activity)
  .post(cloudActivity.create_activity);

module.exports = router;