'use strict';
var mongoose = require ('mongoose'),
    multer = require('multer'),
    path = require('path'),
    CloudMotion = mongoose.model('CloudMotion');

// Disk Storage engine -- temporary, we want to use the Multer-GridFS storage engine
var diskStorage = multer.diskStorage({
  destination: './uploads/',
    filename: function(req, file, cb) {
      cb(null, Date.now() + path.extname(file.originalname))
    }
  }),
  upload = multer({
    storage: diskStorage
  }).single("file");

// Handle upload
exports.create_motion = function (req, res) {
  upload (req, res, (err) => {
      if (err) res.send("err")

      var alert = req.body.alert
      res.send(alert)
   });
};

/// TODO: Get the latest motion image that was uploaded
exports.get_latest_motion = function (req, res) {
    res.end()
};