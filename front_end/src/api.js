import openSocket from 'socket.io-client';

const  socket = openSocket('http://cloudtrackingcloudserver.herokuapp.com');
// const  socket = openSocket('http://localhost:3001/');
function subscribeToCoverage(cb) {
  socket.on('coverage', imagestr => cb(null, imagestr));
}

function subscribeToFlow(cb) {
  socket.on('flow', imagestr => cb(null, imagestr));
}

function subscribeToData(cb) { 
    socket.on('data', data => cb(null, data))
}

export { subscribeToCoverage, subscribeToFlow, subscribeToData };