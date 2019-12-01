'use strict';
var mongoose = require ('mongoose'),
  WeatherData = mongoose.model('WeatherData');

exports.get_all = function(req, res) {
    WeatherData.find({}, function(err, task) {
    if (err)
      res.send(err);
    res.json(task);
  });
};

exports.create = function(data) {
  var new_task = new WeatherData(data);
  new_task.save(function(err, task) {
    if (err)
        console.log(err)
  });
};

exports.get_latest = function(req, res) {
  WeatherData.find().sort({ "time": -1 }).limit(1).exec((err, doc) => {
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

  WeatherData.find({ "time" : {"$gte": fromDate, "$lt": toDate} }).sort({ "time": 1 })
    .stream()
    .pipe(WeatherData.csvTransformStream())
    .pipe(res);
}