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

exports.create = function(data) {
  var new_task = new CloudMotion(data);
  new_task.save(function(err, task) {
    if (err)
        console.log(err)
  });
};

exports.get_latest = function (req, res) {
    CloudMotion.find().sort({ "time": -1 }).limit(1).exec((err, doc) => {
      res.json(doc)
    });
};

exports.get_range = function(req, res) {
  res.writeHead(200, {
    'Content-Type': 'text/csv'
  });

  const fromDate = new Date(req.query.from_date);
  const toDate = new Date(req.query.to_date);

  CloudMotion.find({ "time" : {"$gte": fromDate, "$lt": toDate} }).sort({ "time": 1 })
    .stream()
    .pipe(CloudMotion.csvTransformStream())
    .pipe(res);
}