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

CloudMotionSchema.plugin(mongoose_csv, {
    headers: [ 'DateTime', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'],
    constraints: {
        '0': 'cloudPrediction.0', '1': 'cloudPrediction.1', '2': 'cloudPrediction.2', '3': 'cloudPrediction.3',
        '4': 'cloudPrediction.4', '5': 'cloudPrediction.5', '6': 'cloudPrediction.6', '7': 'cloudPrediction.7',
        '8': 'cloudPrediction.8', '9': 'cloudPrediction.9', '10': 'cloudPrediction.10', '11': 'cloudPrediction.11',
        '12': 'cloudPrediction.12', '13': 'cloudPrediction.13', '14': 'cloudPrediction.14', '15': 'cloudPrediction.15',
        '16': 'cloudPrediction.16', '17': 'cloudPrediction.17', '18': 'cloudPrediction.18', '19': 'cloudPrediction.19',
        '20': 'cloudPrediction.20', '21': 'cloudPrediction.21', '22': 'cloudPrediction.22', '23': 'cloudPrediction.23',
        '24': 'cloudPrediction.24', '25': 'cloudPrediction.25', '26': 'cloudPrediction.26', '27': 'cloudPrediction.27',
        '28': 'cloudPrediction.28', '29': 'cloudPrediction.29', '30': 'cloudPrediction.30'
    },
    virtuals: {
        'DateTime': function(doc) {
          return new Date(doc.time).toISOString()
        }
      }
})

module.exports = mongoose.model('CloudMotion', CloudMotionSchema);