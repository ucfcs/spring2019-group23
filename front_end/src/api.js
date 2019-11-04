import openSocket from 'socket.io-client';

const  socket = openSocket('http://localhost:3001');

function subscribeToImage(cb) {
  socket.on('image', imagestr => cb(null, imagestr));
}

function subscribeToData(cb) { 
    socket.on('data', data => cb(null, data))
}

export { subscribeToImage, subscribeToData };