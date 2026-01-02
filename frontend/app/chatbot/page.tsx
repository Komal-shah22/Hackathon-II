'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { FiSend, FiUser, FiMessageSquare, FiTrash2 } from 'react-icons/fi';
import { FaRobot } from 'react-icons/fa';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { useAuth } from '@/components/auth/auth-context';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export default function ChatbotPage() {
  const { user } = useAuth();
  const router = useRouter();

  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Redirect if not authenticated
  useEffect(() => {
    if (!user) {
      router.push('/signin');
    }
  }, [user, router]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Send message function
  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim() || isLoading) return;

    const token = localStorage.getItem('token'); // Get token from localStorage

    // ✅ Check authentication
    if (!user || !token) {
      console.error('Not authenticated');
      router.push('/signin');
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    // Add user message immediately (optimistic update)
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Get user info from auth context (assuming Better Auth is set up)
      // Replace with your actual auth implementation
      // const token = localStorage.getItem('auth_token'); // Adjust based on your auth
      // const userId = localStorage.getItem('user_id'); // Adjust based on your auth

      // Call backend chat endpoint
      const response = await fetch(`http://localhost:8000/api/${user.id}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: userMessage.content,
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        console.error('API Error:', response.status, errorData);
        throw new Error(`HTTP ${response.status}: ${errorData?.detail || 'Failed to get response'}`);
      }

      const data = await response.json();

      // Update conversation ID if it's a new conversation
      if (!conversationId && data.conversation_id) {
        setConversationId(data.conversation_id);
      }

      // Add assistant response
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);

    } catch (error) {
      console.error('Chat error:', error);
      
      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Clear conversation
  const clearConversation = () => {
    setMessages([]);
    setConversationId(null);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="max-w-4xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <FiMessageSquare className="text-cyan-500 text-2xl" />
            <h1 className="text-xl font-bold text-white">
              Task<span className="text-cyan-500">Bot</span>
            </h1>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={clearConversation}
            className="text-gray-400 hover:text-white"
          >
            <FiTrash2 className="mr-2" />
            Clear Chat
          </Button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4">
        <div className="max-w-4xl mx-auto space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-400 mt-20">
              <FaRobot className="text-6xl mx-auto mb-4 text-cyan-500" />
              <p className="text-lg mb-2">👋 Hi! I'm TaskBot, your AI assistant.</p>
              <p className="text-sm">Try: "Add a task to buy groceries"</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start gap-3 ${
                  message.role === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}
              >
                {/* Avatar */}
                <div
                  className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    message.role === 'user'
                      ? 'bg-cyan-500'
                      : 'bg-gray-700'
                  }`}
                >
                  {message.role === 'user' ? (
                    <FiUser className="text-white" />
                  ) : (
                    <FaRobot className="text-cyan-500" />
                  )}
                </div>

                {/* Message bubble */}
                <div
                  className={`max-w-[70%] rounded-lg p-3 ${
                    message.role === 'user'
                      ? 'bg-cyan-500 text-white'
                      : 'bg-gray-800 text-gray-100'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                </div>
              </div>
            ))
          )}

          {/* Loading indicator */}
          {isLoading && (
            <div className="flex items-start gap-3">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center">
                <FaRobot className="text-cyan-500" />
              </div>
              <div className="bg-gray-800 rounded-lg p-3">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input */}
      <div className="bg-gray-800 border-t border-gray-700 p-4">
        <form onSubmit={sendMessage} className="max-w-4xl mx-auto">
          <div className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type your message..."
              disabled={isLoading}
              className="flex-1 bg-gray-900 border-gray-700 text-white placeholder-gray-500 focus:border-cyan-500"
            />
            <Button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="bg-cyan-500 hover:bg-cyan-600 text-white"
            >
              <FiSend />
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
