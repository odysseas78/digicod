'use client';
import { useEffect, useRef, useState } from 'react';

export default function WebSocketComponent() {
  const wsRef = useRef(null);
  const [messages, setMessages] = useState([]);
  const [connectionStatus, setConnectionStatus] = useState('disconnected');
  const [inputMessage, setInputMessage] = useState('');

  useEffect(() => {
    // WebSocket-Verbindung herstellen
    const wsUrl = process.env.NODE_ENV === 'production'
      ? `wss://${'window.location.host'}`
      : 'ws://localhost:8080';

    console.log('Connecting to WebSocket:', wsUrl);
    wsRef.current = new WebSocket(wsUrl);

    wsRef.current.onopen = () => {
      console.log('WebSocket connected');
      setConnectionStatus('connected');
    };

    wsRef.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log('Received:', data);

        setMessages(prev => [...prev, {
          type: 'received',
          data: data,
          timestamp: new Date().toLocaleTimeString()
        }]);
      } catch (error) {
        console.error('Error parsing message:', error);
        setMessages(prev => [...prev, {
          type: 'received',
          data: event.data,
          timestamp: new Date().toLocaleTimeString()
        }]);
      }
    };

    wsRef.current.onclose = (event) => {
      console.log('WebSocket disconnected:', event.code, event.reason);
      setConnectionStatus('disconnected');
    };

    wsRef.current.onerror = (error) => {
      console.error('WebSocket error:', error);
      setConnectionStatus('error');
    };

    return () => {
      wsRef.current?.close();
    };
  }, []);

  const sendMessage = (message) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      const messageData = {
        message: message,
        timestamp: new Date().toISOString(),
        user: 'client'
      };

      wsRef.current.send(JSON.stringify(messageData));

      setMessages(prev => [...prev, {
        type: 'sent',
        data: messageData,
        timestamp: new Date().toLocaleTimeString()
      }]);
    } else {
      console.error('WebSocket is not connected');
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputMessage.trim()) {
      sendMessage(inputMessage.trim());
      setInputMessage('');
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto">
      <div className="mb-4">
        <div className={`text-sm px-2 py-1 rounded ${
          connectionStatus === 'connected' ? 'bg-green-100 text-green-800' :
          connectionStatus === 'error' ? 'bg-red-100 text-red-800' :
          'bg-gray-100 text-gray-800'
        }`}>
          Status: {connectionStatus}
        </div>
      </div>

      <div className="border rounded p-4 mb-4 h-64 overflow-y-auto bg-gray-50">
        {messages.length === 0 ? (
          <p className="text-gray-500 text-sm">Keine Nachrichten...</p>
        ) : (
          messages.map((msg, index) => (
            <div key={index} className={`mb-2 p-2 rounded text-sm ${
              msg.type === 'sent' ? 'bg-blue-100 ml-8' : 'bg-white mr-8'
            }`}>
              <div className="text-xs text-gray-500">{msg.timestamp}</div>
              <pre className="whitespace-pre-wrap text-xs">
                {typeof msg.data === 'object' ? JSON.stringify(msg.data, null, 2) : msg.data}
              </pre>
            </div>
          ))
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Nachricht eingeben..."
          className="flex-1 px-3 py-2 border rounded"
          disabled={connectionStatus !== 'connected'}
        />
        <button
          type="submit"
          disabled={connectionStatus !== 'connected' || !inputMessage.trim()}
          className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
        >
          Senden
        </button>
      </form>

      <div className="mt-4 text-xs text-gray-500">
        <p>Beispiel-Nachrichten:</p>
        <button
          onClick={() => sendMessage('Hello Server!')}
          className="mr-2 px-2 my-1 py-1 bg-gray-200 rounded text-xs"
          disabled={connectionStatus !== 'connected'}
        >
          Hello Server!
        </button>
        <button
          onClick={() => sendMessage(JSON.stringify({ type: 'ping', data: 'test' }))}
          className="px-2 py-1 bg-gray-200 rounded text-xs"
          disabled={connectionStatus !== 'connected'}
        >
          Ping Test
        </button>
      </div>
    </div>
  );
}