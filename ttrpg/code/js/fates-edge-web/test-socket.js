// Simple test script for Socket.IO
const io = require('socket.io-client');

// Connect to server
const socket = io('http://localhost:3001', {
  auth: {
    token: 'your-jwt-token',
    userId: 'test-user-id'
  }
});

socket.on('connect', () => {
  console.log('Connected to server');
  
  // Join a campaign
  socket.emit('join_campaign', 'test-campaign-id');
  
  // Send a test message
  setTimeout(() => {
    socket.emit('send_message', {
      campaignId: 'test-campaign-id',
      content: 'Hello from test client!',
      channel: 'general'
    });
  }, 1000);
});

socket.on('new_message', (data) => {
  console.log('New message received:', data);
});

socket.on('dice_rolled', (data) => {
  console.log('Dice roll result:', data);
});

socket.on('error', (data) => {
  console.log('Error:', data);
});

socket.on('disconnect', () => {
  console.log('Disconnected from server');
});

