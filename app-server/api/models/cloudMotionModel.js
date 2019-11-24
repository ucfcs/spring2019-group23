'use strict';

var mongoose = require ('mongoose');
var Schema = mongoose.Schema;

const schemaOptions  = {
    timestamps: {
        createdAt: 'time',
        updatedAt: 'updated'
    }
};

var CloudMotionSchema = new Schema({
    cloudPrediction: {
        type: Map,
        of: Number
    },
    image: {
        data: {
            type: Buffer,
            required: false
        },
        contentType: {
            type: String,
            required: false
        }
    },
}, schemaOptions);

module.exports = mongoose.model('CloudMotion', CloudMotionSchema);