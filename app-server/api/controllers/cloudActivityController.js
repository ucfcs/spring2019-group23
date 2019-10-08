'use strict';
var mongoose = require ('mongoose'),
  CloudActivity = mongoose.model('CloudActivity');

exports.get_all_activity = function(req, res) {
    CloudActivity.find({}, function(err, task) {
    if (err)
      res.send(err);
    res.json(task);
  });
};

exports.create_activity = function(req, res) {
  var new_task = new CloudActivity(req.body);
  new_task.save(function(err, task) {
    if (err)
      res.send(err);
    res.json(task);
  });
};