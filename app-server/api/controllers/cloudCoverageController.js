'use strict';
var mongoose = require ('mongoose'),
  CloudCoverage = mongoose.model('CloudCoverage');

exports.get_all_coverage = function(req, res) {
    CloudCoverage.find({}, function(err, task) {
    if (err)
      res.send(err);
    res.json(task);
  });
};

exports.create = function(data) {
  var new_task = new CloudCoverage(data);
  new_task.save(function(err, task) {
    if (err)
        console.log(err)
  });
};

exports.get_latest = function(req, res) {
  CloudCoverage.find().sort({ "time": -1 }).limit(1).exec((err, doc) => {
    if (!err) {
      res.json(doc[0])
    }
  });
}

exports.get_range = function(req, res) {
  res.writeHead(200, {
    'Content-Type': 'text/csv'
  });

  const fromDate = new Date(req.query.from_date);
  const toDate = new Date(req.query.to_date);

  CloudCoverage.find({ "time" : {"$gte": fromDate, "$lt": toDate} }).sort({ "time": 1 })
    .stream()
    .pipe(CloudCoverage.csvTransformStream())
    .pipe(res);
}