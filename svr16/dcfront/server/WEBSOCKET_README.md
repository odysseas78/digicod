# WebSocket-Implementierung für Echtzeit-Updates

## Übersicht

Diese Implementierung verwendet einen separaten WebSocket-Server neben Next.js für Echtzeit-Updates ohne Socket.IO.

## Architektur

- **WebSocket-Server**: Läuft auf Port 8080 (`server/websocket-server.js`)
- **Next.js App**: Läuft auf dem Standard-Port (normalerweise 3000)
- **Client-Komponenten**: Verwenden native WebSocket-API

## Installation & Setup

### 1. Abhängigkeiten installieren
```bash
npm install
```
(Die WebSocket-Abhängigkeiten wurden bereits hinzugefügt)

### 2. WebSocket-Server starten

**Option A: Beide Server gleichzeitig starten**
```bash
npm run dev:ws
```

**Option B: Server separat starten**
```bash
# Terminal 1: Next.js
npm run dev

# Terminal 2: WebSocket-Server
npm run ws-server
```

### 3. Testen

1. Öffne die App im Browser
2. Verwende die WebSocket-Komponente (`components/wsComponent.jsx`)
3. Sende Test-Nachrichten

## API

### WebSocket-Server

**URL**: `ws://localhost:8080` (Entwicklung) / `wss://yourdomain.com` (Produktion)

**Nachrichten-Format**:
```json
{
  "type": "custom",
  "data": "your data",
  "timestamp": "2024-01-15T10:00:00.000Z"
}
```

**Server sendet automatisch**:
- `acknowledgment`: Bestätigung empfangener Nachrichten
- `broadcast`: Nachrichten an alle anderen Clients
- `welcome`: Begrüßung bei Verbindung
- `error`: Fehler-Nachrichten

### Client-Verwendung

#### Einfache Verwendung:
```jsx
import WebSocketComponent from '@/components/wsComponent';

export default function Page() {
  return <WebSocketComponent />;
}
```

#### Mit WebSocket-Manager:
```jsx
'use client';
import { wsManager } from '@/lib/websocket';
import { useEffect } from 'react';

export default function MyComponent() {
  useEffect(() => {
    // Verbinden
    wsManager.connect('ws://localhost:8080');

    // Event-Handler registrieren
    wsManager.onMessage((data) => {
      console.log('Received:', data);
    });

    wsManager.onConnect(() => {
      console.log('Connected!');
    });

    return () => {
      wsManager.disconnect();
    };
  }, []);

  const sendMessage = () => {
    wsManager.send({ type: 'test', message: 'Hello!' });
  };

  return (
    <button onClick={sendMessage}>
      Send Message
    </button>
  );
}
```

## Dateien

- `server/websocket-server.js`: WebSocket-Server-Implementierung
- `server/start-ws-server.js`: Start-Script für den Server
- `components/wsComponent.jsx`: Beispiel-Client-Komponente
- `lib/websocket.ts`: WebSocket-Manager-Klasse mit Event-System

## Features

- ✅ Automatische Wiederverbindung mit Exponential Backoff
- ✅ Broadcast-Nachrichten an alle Clients
- ✅ JSON-Nachrichten-Verarbeitung
- ✅ Fehlerbehandlung
- ✅ Connection-State-Management
- ✅ Event-basierte Architektur

## Troubleshooting

### Fehler: "WebSocket error: Event"

1. **Server läuft nicht**: Stelle sicher, dass der WebSocket-Server läuft (`npm run ws-server`)
2. **Falsche URL**: Überprüfe die WebSocket-URL in der Client-Komponente
3. **Port-Konflikt**: Stelle sicher, dass Port 8080 verfügbar ist

### Fehler: "Connection failed"

1. **CORS**: WebSocket hat keine CORS-Einschränkungen, aber der Server muss erreichbar sein
2. **Firewall**: Stelle sicher, dass Port 8080 nicht blockiert ist
3. **HTTPS**: Verwende `wss://` für HTTPS-Verbindungen

## Produktion

Für die Produktion:

1. **Environment-Variable**: Setze die WebSocket-URL basierend auf der Umgebung
2. **SSL/TLS**: Verwende `wss://` für sichere Verbindungen
3. **Load Balancing**: Implementiere Sticky Sessions für WebSocket-Verbindungen
4. **Monitoring**: Füge Logging und Monitoring hinzu

## Erweiterungen

- **Authentifizierung**: Token-basierte Authentifizierung hinzufügen
- **Rooms**: Client-Gruppen für gezielte Broadcasts
- **Heartbeat**: Keep-Alive-Mechanismen
- **Rate Limiting**: Nachrichten-Rate begrenzen