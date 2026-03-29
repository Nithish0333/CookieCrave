import React, { useState, useEffect, useRef } from 'react';
import { Card, Button, Form, Spinner, Badge, Alert } from 'react-bootstrap';
import api from '../api';

const ChatbotPage = () => {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: 'Hello! I\'m your CookieCrave assistant! 🍪 I can help you with:\n\n🍪 **Products**: Top 5, categories, all products\n💰 **Pricing & Deals**: Cookie prices, bulk discounts\n📦 **Delivery**: Same-day, standard, express options\n🎁 **Gift Boxes**: Perfect for any occasion\n📊 **Analytics**: Track your conversation\n💬 **General Chat**: Ask me anything!\n\nWhat would you like to know?',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [userId, setUserId] = useState('anonymous');
  const [conversationStats, setConversationStats] = useState(null);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const messagesEndRef = useRef(null);

  const quickQuestions = [
    'What cookies do you have?',
    'How much do cookies cost?',
    'Delivery options',
    'Gift boxes',
    'Order tracking',
    'Recommend me something',
    'Ingredients and allergens',
    'Special offers',
  ];

  const productQuestions = [
    'Show top 5 products',
    'List categories',
    'List all products',
  ];

  const contextualQuestions = [
    'Tell me more about chocolate chip cookies',
    'What\'s your best deal?',
    'When can I get same-day delivery?',
    'Gift box recommendations',
    'Bulk ordering discounts',
  ];

  useEffect(() => {
    // Generate or retrieve user ID
    let storedUserId = localStorage.getItem('chatbot_user_id');
    if (!storedUserId) {
      storedUserId = 'user_' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('chatbot_user_id', storedUserId);
    }
    setUserId(storedUserId);

    // Auto-scroll to bottom
    scrollToBottom();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed) return;

    const userMsg = { 
      role: 'user', 
      content: trimmed,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      console.log('Sending request to chatbot API...');
      console.log('Message:', trimmed);
      console.log('User ID:', userId);
      
      const res = await api.post('chatbot/', {
        message: trimmed,
        user_id: userId,
        context: {
          page: window.location.pathname,
          timestamp: new Date().toISOString(),
        }
      });

      console.log('Chatbot response:', res);
      console.log('Response data:', res.data);

      const reply = res.data?.reply || 'Sorry, I could not understand that.';
      const assistantMsg = {
        role: 'assistant',
        content: reply,
        timestamp: new Date(),
        intent: res.data?.intent,
        context: res.data?.context,
      };
      
      setMessages((prev) => [...prev, assistantMsg]);

      // Update conversation stats if available
      if (res.data?.context) {
        setConversationStats(res.data.context);
      }

    } catch (err) {
      console.error('Chatbot error:', err);
      console.error('Error response:', err.response);
      console.error('Error message:', err.message);
      
      let errorMsg = 'Sorry, something went wrong while contacting the assistant. Please try again.';
      
      // Add more specific error information
      if (err.response) {
        errorMsg += ` (Error ${err.response.status}: ${err.response.statusText})`;
        console.log('Error data:', err.response.data);
      } else if (err.request) {
        errorMsg += ' (Network error - could not reach server)';
      } else {
        errorMsg += ` (${err.message})`;
      }
      
      const errorResponse = {
        role: 'assistant',
        content: errorMsg,
        timestamp: new Date(),
        error: true,
      };
      setMessages((prev) => [...prev, errorResponse]);
    } finally {
      setLoading(false);
    }
  };

  const handleQuickQuestion = (question) => {
    setInput(question);
  };

  const clearConversation = () => {
    setMessages([
      {
        role: 'assistant',
        content: 'Hello! I\'m your CookieCrave assistant! 🍪 I can help you with:\n\n🍪 **Products**: Top 5, categories, all products\n💰 **Pricing & Deals**: Cookie prices, bulk discounts\n📦 **Delivery**: Same-day, standard, express options\n🎁 **Gift Boxes**: Perfect for any occasion\n📊 **Analytics**: Track your conversation\n💬 **General Chat**: Ask me anything!\n\nWhat would you like to know?',
        timestamp: new Date(),
      },
    ]);
    setConversationStats(null);
  };

  const fetchAnalytics = async () => {
    try {
      const res = await api.get('chatbot/analytics/');
      setConversationStats(res.data);
      setShowAnalytics(true);
    } catch (err) {
      console.error('Failed to fetch analytics:', err);
    }
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getIntentBadge = (intent) => {
    if (!intent || !intent.intents) return null;
    
    const detectedIntents = Object.keys(intent.intents).filter(key => intent.intents[key]);
    if (detectedIntents.length === 0) return null;

    const intentColors = {
      'product_inquiry': 'info',
      'pricing': 'success',
      'delivery': 'warning',
      'gifting': 'danger',
      'ordering': 'primary',
      'recommendation': 'secondary',
    };

    return (
      <div className="mt-2">
        {detectedIntents.map((intentName, idx) => (
          <Badge 
            key={idx} 
            bg={intentColors[intentName] || 'light'} 
            className="me-1" 
            style={{ fontSize: '0.7em' }}
          >
            {intentName.replace('_', ' ')}
          </Badge>
        ))}
      </div>
    );
  };

  return (
    <>
      <style>{`
        .chatbot-card:hover {
          transform: none !important;
          box-shadow: 0 8px 24px rgba(0,0,0,0.04) !important;
        }
        .message-bubble {
          animation: fadeIn 0.3s ease-in;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .typing-indicator {
          display: inline-flex;
          align-items: center;
          gap: 4px;
        }
        .typing-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background-color: #6c757d;
          animation: typing 1.4s infinite;
        }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        @keyframes typing {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-10px); }
        }
      `}</style>
      
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h2 className="fw-bold mb-0">Advanced AI Assistant</h2>
        <div>
          <Button 
            variant="outline-info" 
            size="sm" 
            onClick={fetchAnalytics}
            className="me-2"
          >
            📊 Analytics
          </Button>
          <Button 
            variant="outline-secondary" 
            size="sm" 
            onClick={clearConversation}
          >
            🔄 Clear
          </Button>
        </div>
      </div>

      {showAnalytics && conversationStats && (
        <Alert variant="info" dismissible onClose={() => setShowAnalytics(false)}>
          <h6>Conversation Analytics</h6>
          <div className="row">
            <div className="col-md-3">
              <strong>Messages:</strong> {conversationStats.conversation_count}
            </div>
            <div className="col-md-3">
              <strong>Preferences:</strong> {conversationStats.preferences?.length || 0}
            </div>
            <div className="col-md-6">
              <strong>Interests:</strong> {conversationStats.preferences?.join(', ') || 'None detected'}
            </div>
          </div>
        </Alert>
      )}

      <Card className="shadow-sm chatbot-card">
        <Card.Body>
          <Card.Title className="fw-bold mb-3">
            🍪 CookieCrave Assistant
            <Badge bg="success" className="ms-2" style={{ fontSize: '0.6em' }}>Advanced</Badge>
          </Card.Title>
          
          <div
            className="border rounded p-3 mb-3"
            style={{ height: '450px', overflowY: 'auto', backgroundColor: '#f8f9fa' }}
          >
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`mb-3 d-flex ${
                  msg.role === 'user' ? 'justify-content-end' : 'justify-content-start'
                }`}
              >
                <div
                  className={`message-bubble px-3 py-2 rounded-3 ${
                    msg.role === 'user' ? 'bg-primary text-white' : 'bg-white border'
                  }`}
                  style={{ maxWidth: '85%' }}
                >
                  <div className="small text-muted mb-1" style={{ fontSize: '0.7em' }}>
                    {msg.role === 'user' ? 'You' : 'Assistant'} • {formatTime(msg.timestamp)}
                  </div>
                  <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                  
                  {msg.role === 'assistant' && getIntentBadge(msg.intent)}
                  {msg.error && (
                    <Badge bg="danger" className="mt-2" style={{ fontSize: '0.7em' }}>
                      Error
                    </Badge>
                  )}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="d-flex align-items-center text-muted mb-3">
                <div className="typing-indicator me-2">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
                <span>Assistant is thinking...</span>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          <Form onSubmit={sendMessage}>
            <div className="mb-3">
              <small className="text-muted d-block mb-2">Cookie questions:</small>
              <div className="d-flex flex-wrap gap-2 mb-2">
                {quickQuestions.map((question, idx) => (
                  <Button
                    key={idx}
                    variant="outline-primary"
                    size="sm"
                    onClick={() => handleQuickQuestion(question)}
                    disabled={loading}
                    className="rounded-pill"
                  >
                    {question}
                  </Button>
                ))}
              </div>
              
              <small className="text-muted d-block mb-2">Product catalog:</small>
              <div className="d-flex flex-wrap gap-2 mb-2">
                {productQuestions.map((question, idx) => (
                  <Button
                    key={idx}
                    variant="outline-info"
                    size="sm"
                    onClick={() => handleQuickQuestion(question)}
                    disabled={loading}
                    className="rounded-pill"
                  >
                    {question}
                  </Button>
                ))}
              </div>
              
              {conversationStats?.preferences && conversationStats.preferences.length > 0 && (
                <div className="mt-2">
                  <small className="text-muted d-block mb-2">Based on your interests:</small>
                  <div className="d-flex flex-wrap gap-2">
                    {contextualQuestions.map((question, idx) => (
                      <Button
                        key={idx}
                        variant="outline-success"
                        size="sm"
                        onClick={() => handleQuickQuestion(question)}
                        disabled={loading}
                        className="rounded-pill"
                      >
                        {question}
                      </Button>
                    ))}
                  </div>
                </div>
              )}
            </div>
            
            <Form.Group className="d-flex gap-2">
              <Form.Control
                type="text"
                placeholder="Ask me anything about cookies, products, orders, or recommendations..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={loading}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && sendMessage(e)}
              />
              <Button type="submit" variant="primary" disabled={loading || !input.trim()}>
                {loading ? 'Sending...' : 'Send'}
              </Button>
            </Form.Group>
          </Form>
        </Card.Body>
      </Card>
    </>
  );
};

export default ChatbotPage;

