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
    image: {
        data: {
            type: Buffer,
            required: true
        },
        contentType: {
            type: String,
            required: true
        }
    },
    // If we have an alert associated with this cloud motion image, here it goes
    alert: {
        type: String,
        required: false
    }
}, schemaOptions);

module.exports = mongoose.model('CloudMotion', CloudMotionSchema);