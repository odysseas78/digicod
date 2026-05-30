// lib/websocket.ts
type MessageHandler = (data: any) => void;
type ConnectionHandler = () => void;
type ErrorHandler = (error: Event) => void;

class WebSocketManager {
   private ws: WebSocket | null = null;
   private reconnectAttempts = 0;
   private maxReconnectAttempts = 5;
   private reconnectInterval = 1000;
   private url: string = '';

   // Event handlers
   private onMessageHandlers: MessageHandler[] = [];
   private onConnectHandlers: ConnectionHandler[] = [];
   private onDisconnectHandlers: ConnectionHandler[] = [];
   private onErrorHandlers: ErrorHandler[] = [];

   connect(url?: string) {
     if (url) this.url = url;
     if (!this.url) {
       console.error('No WebSocket URL provided');
       return;
     }

     // Schließe bestehende Verbindung
     this.disconnect();

     try {
       console.log(`Connecting to WebSocket: ${this.url}`);
       this.ws = new WebSocket(this.url);

       this.ws.onopen = () => {
         console.log('WebSocket connected successfully');
         this.reconnectAttempts = 0;
         this.onConnectHandlers.forEach(handler => handler());
       };

       this.ws.onmessage = (event) => {
         try {
           const data = JSON.parse(event.data);
           this.onMessageHandlers.forEach(handler => handler(data));
         } catch (error) {
           console.error('Error parsing WebSocket message:', error);
           // Raw message weiterleiten
           this.onMessageHandlers.forEach(handler => handler(event.data));
         }
       };

       this.ws.onclose = (event) => {
         console.log(`WebSocket disconnected: ${event.code} ${event.reason}`);
         this.onDisconnectHandlers.forEach(handler => handler());
         this.handleReconnect();
       };

       this.ws.onerror = (error) => {
         console.error('WebSocket error:', error);
         this.onErrorHandlers.forEach(handler => handler(error));
       };

     } catch (error) {
       console.error('Failed to create WebSocket connection:', error);
       this.handleReconnect();
     }
   }

   private handleReconnect() {
     if (this.reconnectAttempts < this.maxReconnectAttempts) {
       const delay = this.reconnectInterval * Math.pow(2, this.reconnectAttempts); // Exponential backoff
       setTimeout(() => {
         this.reconnectAttempts++;
         console.log(`Reconnecting... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
         this.connect();
       }, delay);
     } else {
       console.error('Max reconnection attempts reached');
     }
   }

   send(data: any) {
     if (this.ws?.readyState === WebSocket.OPEN) {
       try {
         const message = typeof data === 'string' ? data : JSON.stringify(data);
         this.ws.send(message);
         return true;
       } catch (error) {
         console.error('Error sending WebSocket message:', error);
         return false;
       }
     } else {
       console.warn('WebSocket is not connected');
       return false;
     }
   }

   disconnect() {
     if (this.ws) {
       this.ws.close();
       this.ws = null;
     }
   }

   isConnected(): boolean {
     return this.ws?.readyState === WebSocket.OPEN;
   }

   getConnectionState(): string {
     if (!this.ws) return 'disconnected';
     switch (this.ws.readyState) {
       case WebSocket.CONNECTING: return 'connecting';
       case WebSocket.OPEN: return 'connected';
       case WebSocket.CLOSING: return 'closing';
       case WebSocket.CLOSED: return 'disconnected';
       default: return 'unknown';
     }
   }

   // Event handler registration
   onMessage(handler: MessageHandler) {
     this.onMessageHandlers.push(handler);
   }

   onConnect(handler: ConnectionHandler) {
     this.onConnectHandlers.push(handler);
   }

   onDisconnect(handler: ConnectionHandler) {
     this.onDisconnectHandlers.push(handler);
   }

   onError(handler: ErrorHandler) {
     this.onErrorHandlers.push(handler);
   }

   // Event handler removal
   offMessage(handler: MessageHandler) {
     this.onMessageHandlers = this.onMessageHandlers.filter(h => h !== handler);
   }

   offConnect(handler: ConnectionHandler) {
     this.onConnectHandlers = this.onConnectHandlers.filter(h => h !== handler);
   }

   offDisconnect(handler: ConnectionHandler) {
     this.onDisconnectHandlers = this.onDisconnectHandlers.filter(h => h !== handler);
   }

   offError(handler: ErrorHandler) {
     this.onErrorHandlers = this.onErrorHandlers.filter(h => h !== handler);
   }
}

// Singleton instance
export const wsManager = new WebSocketManager();

// Convenience function for quick setup
export function createWebSocketManager(url: string): WebSocketManager {
  const manager = new WebSocketManager();
  manager.connect(url);
  return manager;
}