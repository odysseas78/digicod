#!/usr/bin/env node

// WebSocket-Server starten
require('./websocket-server.js');

// Halte den Prozess am Laufen
process.on('SIGTERM', () => {
  console.log('WebSocket-Server wird beendet...');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('WebSocket-Server wird beendet...');
  process.exit(0);
});