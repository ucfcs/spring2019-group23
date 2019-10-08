'use strict';
module.exports = function(app) {
  var cloudActivity = require('../controllers/cloudActivityController');

  // cloudActivity Routes
  app.route('/api/activity')
    .get(cloudActivity.get_all_activity)
    .post(cloudActivity.create_activity);
};
