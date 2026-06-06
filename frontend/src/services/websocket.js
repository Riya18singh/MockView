let socket = null;

export const connectWebSocket = (sessionId, onMessage) => {
  socket = new WebSocket(
    `ws://localhost:8000/ws/interview/${sessionId}/`
  );

  socket.onopen = () => {
    console.log('Connected to interview!');
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };

  socket.onclose = () => {
    console.log('Interview ended!');
  };
};

export const sendMessage = (message) => {
  if (socket) {
    socket.send(JSON.stringify({
      type: 'user_answer',
      message: message
    }));
  }
};

export const closeWebSocket = () => {
  if (socket) socket.close();
};