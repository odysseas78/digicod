const WebSocket = require('ws');
const http = require('http');

// WebSocket-Server auf separatem Port
const WS_PORT = 8080;

// HTTP-Server für WebSocket-Upgrade
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('WebSocket Server Running');
});

// WebSocket-Server erstellen
const wss = new WebSocket.Server({ server });

// Verbindung speichern
const clients = new Set();

wss.on('connection', (ws, req) => {
  console.log('Neuer WebSocket-Client verbunden');

  // Client zur Menge hinzufügen
  clients.add(ws);

  // Nachrichten vom Client empfangen
  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message.toString());
      console.log('Empfangene Nachricht:', data);

      // Nachricht an alle Clients weiterleiten (Broadcast)
      clients.forEach(client => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({
            type: 'broadcast',
            data: {data},
            timestamp: new Date().toISOString()
          }));
        }
      });

      // Bestätigung an Sender zurückschicken
      ws.send(JSON.stringify({
        type: 'acknowledgment',
        message: 'Nachricht empfangen',
        originalData: data
      }));

    } catch (error) {
      console.error('Fehler beim Verarbeiten der Nachricht:', error);
      ws.send(JSON.stringify({
        type: 'error',
        message: 'Ungültige Nachricht'
      }));
    }
  });

  // Client beim Trennen entfernen
  ws.on('close', () => {
    console.log('WebSocket-Client getrennt');
    clients.delete(ws);
  });

  // Fehler behandeln
  ws.on('error', (error) => {
    console.error('WebSocket-Fehler:', error);
    clients.delete(ws);
  });

  // Willkommensnachricht senden
  ws.send(JSON.stringify({
    type: 'welcome',
    message: 'Verbunden mit WebSocket-Server',
    connectedClients: clients.size
  }));
});

// Server starten
server.listen(WS_PORT, () => {
  console.log(`WebSocket-Server läuft auf ws://localhost:${WS_PORT}`);
});

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('WebSocket-Server wird beendet...');
  wss.close(() => {
    server.close(() => {
      process.exit(0);
    });
  });
});

module.exports = { wss, server };