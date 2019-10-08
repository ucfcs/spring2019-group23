'use strict';

var mongoose = require ('mongoose');
var Schema = mongoose.Schema;

const schemaOptions  = {
    timestamps: {
        createdAt: 'time',
        updatedAt: 'updated'
    }
};

var CloudActivitySchema = new Schema({
    // Weather data also, depending on what is used on power prediction
    powerPrediction: {
        type: Number,
        required: true
    },
    cloudBaseHeight: {
        type: Number,
        required: true
    },
    okta: {
        type: Number,
        required: true,
        min: 0,
        max: 9
    }
}, schemaOptions);

module.exports = mongoose.model('CloudActivity', CloudActivitySchema);