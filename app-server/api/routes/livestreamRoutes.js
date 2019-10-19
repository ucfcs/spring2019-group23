'use strict';
var express = require('express');

var router = express.Router();

module.exports = (socketServer) => {
    router.route('/').post((request, response) => {
        console.log("Camera connected")
        request.on('data', function (data) {
            socketServer.broadcast(data);
        });
    });
    return router
};