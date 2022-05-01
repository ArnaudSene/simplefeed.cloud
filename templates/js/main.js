let socket = new WebSocket("ws://localhost:8000/ws");

// socket.onopen = function(e) {
//     alert("[open] Connection established");
//     alert("Sending to server");
//     socket.send("My name is John");
// };

socket.onmessage = function(event) {
    console.log(`[message] Data received from server: ${event.data}`);
};
