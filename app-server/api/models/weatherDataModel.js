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

var WeatherDataSchema = new Schema(
    {
        temperature: {
            type: Number,
            // required: true
        },
        dew_point: {
            type: Number,
            // required: true
        },
        barometric_pressure: {
            type: Number,
            // required: true
        },
        cloud_base_height: {
            type: Number,
            // required: true
        },
        gt_cloud_coverage: {
            type: Number,
            // required: true
        },
        wind_direction: {
            type: Number,
            // required: true
        },
        wind_gust: {
            type: Number,
            // required: true
        },
        wind_speed: {
            type: Number,
            // required: true
        },
        humidity: {
            type: Number,
            // required: true
        },
        rain_probability: {
            type: Number,
            // required: true
        },
        rain_intensity: {
            type: Number,
            // required: true
        },
        latitude: {
            type: Number,
            // required: true
        },
        longitude: {
            type: Number,
            // required: true
        },
    }, schemaOptions);

WeatherDataSchema.plugin(mongoose_csv, {
    headers: ['DateTime',
            'Temperature',
            'Dew Point',
            'Barometric Pressure',
            'Cloud Base Height',
            'Ground Truth Coverage',
            'Wind Direction',
            'Wind Gust',
            'Wind Speed',
            'Humidity',
            'Rain Probability',
            'Rain Intensity',
            'Latitude',
            'Longitude'],
    constraints: {
      'Temperature': 'temperature',
      'Dew Point': 'dew_point',
      'Barometric Pressure': 'barometric_pressure',
      'Cloud Base Height': 'cloud_base_height',
      'Ground Truth Coverage': 'gt_cloud_coverage',
      'Wind Direction': 'wind_direction',
      'Wind Gust': 'wind_gust',
      'Wind Speed': 'wind_speed',
      'Humidity': 'humidity',
      'Rain Probability': 'rain_probability',
      'Rain Intensity': 'rain_intensity',
      'Latitude': 'latitude',
      'Longitude': 'longitude'
    },
    virtuals: {
      'DateTime': function(doc) {
        return new Date(doc.time).toISOString()
      }
    }
});

module.exports = mongoose.model('WeatherData', WeatherDataSchema);