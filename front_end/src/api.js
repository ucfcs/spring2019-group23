import openSocket from 'socket.io-client';

const  socket = openSocket('http://cloudtrackingcloudserver.herokuapp.com');

function subscribeToImage(cb) {
  socket.on('image', imagestr => cb(null, imagestr));
}

function subscribeToData(cb) { 
    socket.on('data', data => cb(null, data))
}

export { subscribeToImage, subscribeToData };