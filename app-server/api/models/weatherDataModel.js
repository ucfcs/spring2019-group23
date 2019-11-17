'use strict';

var mongoose = require ('mongoose');
var Schema = mongoose.Schema;

const schemaOptions  = {
    timestamps: {
        createdAt: 'time',
        updatedAt: 'updated'
    }
};

var WeatherDataSchema = new Schema(
    {
        cloud_coverage: {
            type: Number,
            required: false
        },
        temperature: {
            type: Number,
            required: true
        },
        dew_point: {
            type: Number,
            required: true
        },
        barometric_pressure: {
            type: Number,
            required: true
        },
        cloud_base_height: {
            type: Number,
            required: true
        },
        gt_cloud_coverage: {
            type: Number,
            required: true
        },
        wind_direction: {
            type: Number,
            required: true
        },
        wind_gust: {
            type: Number,
            required: true
        },
        wind_speed: {
            type: Number,
            required: true
        },
        humidity: {
            type: Number,
            required: true
        },
        rain_probability: {
            type: Number,
            required: true
        },
        rain_intensity: {
            type: Number,
            required: true
        },
        latitude: {
            type: Number,
            required: true
        },
        longitude: {
            type: Number,
            required: true
        },
    }, schemaOptions);

module.exports = mongoose.model('WeatherData', WeatherDataSchema);