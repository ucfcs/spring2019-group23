'use strict';

var mongoose = require ('mongoose');
var mongoose_csv = require('mongoose-to-csv');
var Schema = mongoose.Schema;

const schemaOptions  = {
    timestamps: {
        createdAt: 'time',
        updatedAt: 'updated'
    }
};

var CloudCoverageSchema = new Schema({
    cloud_coverage: {
        type: Number
    }
}, schemaOptions);

CloudCoverageSchema.plugin(mongoose_csv, {
    headers: ['DateTime',
            'Cloud Coverage',
            ],
    constraints: {
      'Cloud Coverage': 'cloud_coverage',
    },
    virtuals: {
      'DateTime': function(doc) {
        return new Date(doc.time).toISOString()
      }
    }
});

module.exports = mongoose.model('CloudCoverage', CloudCoverageSchema);