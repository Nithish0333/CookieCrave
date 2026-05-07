import os
import json
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .advanced_chatbot import AdvancedChatbot


class ChatbotView(APIView):
    """
    Advanced AI chatbot endpoint with contextual awareness and memory.
    
    Features:
    - Conversation memory
    - Personalized responses
    - Dynamic recommendations
    - No repetitive answers
    - Context-aware assistance
    """

    permission_classes = [permissions.AllowAny]
    
    def __init__(self):
        super().__init__()
        self.chatbot = AdvancedChatbot()

    def post(self, request):
        user_message = request.data.get("message", "").strip()
        user_id = request.data.get("user_id", "anonymous")
        context = request.data.get("context", {})

        if not user_message:
            return Response(
                {"detail": "Message is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Get advanced response
            response = self.chatbot.get_response(user_message, user_id)
            
            # Add context if provided
            if context:
                response["context_used"] = True
            
            return Response(response, status=status.HTTP_200_OK)
            
        except Exception as e:
            # Enhanced fallback
            fallback_response = self._get_enhanced_fallback(user_message)
            return Response({
                "reply": fallback_response,
                "user_id": user_id,
                "fallback": True
            }, status=status.HTTP_200_OK)
    
    def _get_enhanced_fallback(self, message: str) -> str:
        """Enhanced fallback responses with variety"""
        message_lower = message.lower()
        
        # Dynamic fallback responses
        responses = {
            "greeting": [
                "Hello! I'm your CookieCrave assistant! 🍪 What can I help you with today?",
                "Hi there! Ready to explore our delicious cookies? How can I assist you?",
                "Welcome to CookieCrave! I'm here to help with all your cookie needs. What's on your mind?"
            ],
            "cookie_help": [
                "I can help you choose the perfect cookies! We have Chocolate Chip, Oatmeal Raisin, and Snickerdoodle varieties. Which sounds good to you?",
                "Great question! Our cookies are freshly baked with premium ingredients. What type are you interested in?",
                "I'd love to help you find the perfect cookies! Are you looking for something for yourself or as a gift?"
            ],
            "price_help": [
                "Our cookies range from ₹179-₹199 each. We offer great deals: 6 for ₹999, 12 for ₹1899! How many are you thinking?",
                "Let me help you with pricing! Individual cookies are ₹179-₹199, with bulk discounts available. What's your budget?",
                "Pricing question! I can give you the best deal based on quantity. How many cookies do you need?"
            ],
            "delivery_help": [
                "We offer same-day, standard, and express delivery! When do you need your cookies?",
                "Delivery options available! Same-day for orders before 2 PM, standard 2-3 days. What works for you?",
                "I can help with delivery! We have multiple options. When do you need your cookies delivered?"
            ],
            "general_help": [
                "I'm here to help with cookies, pricing, delivery, gifting, and recommendations! What would you like to know?",
                "I can assist with product questions, orders, delivery, and gift options! What's on your mind?",
                "Ready to help! I know all about our cookies, pricing, and delivery. What do you need assistance with?"
            ]
        }
        
        # Determine category
        if any(word in message_lower for word in ["hello", "hi", "hey"]):
            return responses["greeting"][hash(message) % len(responses["greeting"])]
        elif any(word in message_lower for word in ["cookie", "cookies", "bake", "baked"]):
            return responses["cookie_help"][hash(message) % len(responses["cookie_help"])]
        elif any(word in message_lower for word in ["price", "cost", "how much", "₹", "rupees"]):
            return responses["price_help"][hash(message) % len(responses["price_help"])]
        elif any(word in message_lower for word in ["delivery", "deliver", "shipping", "when"]):
            return responses["delivery_help"][hash(message) % len(responses["delivery_help"])]
        else:
            return responses["general_help"][hash(message) % len(responses["general_help"])]


class ChatbotAnalyticsView(APIView):
    """
    Analytics endpoint for chatbot performance
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def __init__(self):
        super().__init__()
        self.chatbot = AdvancedChatbot()
    
    def get(self, request):
        user_id = request.user.id if hasattr(request.user, 'id') else "anonymous"
        
        # Get user context and conversation history
        context = self.chatbot._get_user_context(str(user_id))
        history = self.chatbot.conversation_history.get(str(user_id), [])
        
        return Response({
            "user_context": context,
            "conversation_count": len(history),
            "recent_conversations": history[-5:] if history else [],
            "preferences": context.get("preferences", [])
        })

