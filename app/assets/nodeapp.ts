import { Terminal } from 'xterm';
import * as io from 'socket.io-client'
import * as attach from 'xterm/lib/addons/attach/attach';
import 'xterm/dist/xterm.css';

Terminal.applyAddon(attach);


let term;
let socket;
let buffer: string;
let namespace: string = "/webapp"

const messages = document.querySelector('#messages');
const wsButton = document.querySelector('#wsButton');

function showMessage(message): void {
  term.write(message)
};

buffer = "";
term = new Terminal();

term.open(document.getElementById('terminal'));

//term.on('data', function(data){
//  console.log( data);
//});



term.on('key', (key: string, event: KeyboardEvent) => {
    console.log(key, event);
    if(event.key === "Enter"){
      console.log('here we go!');
      socket.emit("message", buffer);
      buffer = "";
    }else{
      buffer += key;
    }
    console.log(buffer);
});


socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

socket.on('message', function (data) {
  term.write(data);
})

socket.on('connect', function () {
  showMessage('Websocket connected');
  socket.emit('message', "im connected")
})


socket.on('disconnect', function (err) {
  showMessage('WEBSOCKET SERVER DISCONNECTED' );
  socket.io.reconnection(false)
})
