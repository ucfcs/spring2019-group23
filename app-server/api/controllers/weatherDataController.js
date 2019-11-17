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