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
    okta: {
        type: Number,
        required: true,
        min: 0,
        max: 9
    }

}, schemaOptions);