"use client";

import { useState, useEffect } from "react";
import ChatHeader from "../components/ChatHeader";
import MessageList from "../components/MessageList";
import ChatInput from "../components/ChatInput";
import ConnectingOverlay from "../components/ConnectingOverlay";

interface Message {
  content: string;
  sender: "user" | "bot";
  timestamp?: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [connecting, setConnecting] = useState(true);
  const [connected, setConnected] = useState(false);
  const [socket, setSocket] = useState<WebSocket | null>(null);

  // Initialize WebSocket connection
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");
    
    ws.onopen = () => {
      console.log("Connected to WebSocket");
      setConnected(true);
      setConnecting(false);
      setSocket(ws);
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === "message") {
        const newMessage: Message = {
          content: typeof data.message === "string" ? data.message : data.message.content,
          sender: "bot",
          timestamp: new Date().toISOString()
        };
        
        setMessages(prev => [...prev, newMessage]);
      } else if (data.type === "error") {
        console.error("WebSocket error:", data.message);
      }
    };
    
    ws.onclose = () => {
      console.log("Disconnected from WebSocket");
      setConnected(false);
      setConnecting(true);
    };
    
    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      setConnected(false);
    };
    
    return () => {
      ws.close();
    };
  }, []);

  const sendMessage = (content: string) => {
    if (!socket || socket.readyState !== WebSocket.OPEN || !content.trim()) {
      return;
    }
    
    const message: Message = {
      content,
      sender: "user",
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, message]);
    
    socket.send(JSON.stringify({
      type: "message",
      content: content
    }));
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100 dark:bg-gray-900">
      {connecting && <ConnectingOverlay />}
      
      <ChatHeader connected={connected} />
      
      <div className="flex-1 overflow-hidden">
        <MessageList messages={messages} />
      </div>
      
      <ChatInput onSendMessage={sendMessage} disabled={!connected} />
    </div>
  );
}
