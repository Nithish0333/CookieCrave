import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
import random

class AdvancedChatbot:
    """
    Advanced AI Chatbot for CookieCrave with:
    - Context awareness
    - Memory of conversation
    - Dynamic responses
    - Product recommendations
    - Order tracking
    - Personalization
    """
    
    def __init__(self):
        self.conversation_history = {}
        self.user_profiles = {}
        self.product_knowledge = self._load_product_knowledge()
        self.response_templates = self._load_response_templates()
        
    def _load_product_knowledge(self) -> Dict:
        """Load comprehensive product knowledge base"""
        return {
            "cookies": {
                "chocolate_chip": {
                    "name": "Chocolate Chip Cookies",
                    "price": 199,
                    "description": "Classic chocolate chip cookies with premium Belgian chocolate chunks",
                    "ingredients": ["flour", "butter", "sugar", "eggs", "vanilla", "belgian chocolate"],
                    "allergens": ["gluten", "dairy", "eggs"],
                    "best_for": ["desserts", "snacks", "gifts"],
                    "rating": 4.8
                },
                "oatmeal_raisin": {
                    "name": "Oatmeal Raisin Cookies",
                    "price": 189,
                    "description": "Heart-healthy oatmeal cookies with plump raisins and cinnamon",
                    "ingredients": ["oats", "flour", "butter", "brown sugar", "raisins", "cinnamon"],
                    "allergens": ["gluten", "dairy", "nuts"],
                    "best_for": ["breakfast", "healthy_snacks", "tea_time"],
                    "rating": 4.6
                },
                "snickerdoodle": {
                    "name": "Snickerdoodle Cookies",
                    "price": 179,
                    "description": "Soft and chewy cinnamon-sugar coated cookies",
                    "ingredients": ["flour", "butter", "sugar", "eggs", "cream_of_tartar", "cinnamon"],
                    "allergens": ["gluten", "dairy", "eggs"],
                    "best_for": ["parties", "snacks", "kids"],
                    "rating": 4.7
                }
            },
            "pricing": {
                "single": 199,
                "half_dozen": 999,
                "dozen": 1899,
                "bulk_50": 8999,
                "gift_box_small": 1299,
                "gift_box_medium": 1999,
                "gift_box_large": 3299
            },
            "delivery": {
                "same_day": {"cutoff": "14:00", "fee": 99},
                "standard": {"time": "2-3 business days", "fee": 49},
                "express": {"time": "next day", "fee": 199},
                "free_threshold": 1500
            },
            "special_offers": {
                "first_order": {"discount": 10, "code": "WELCOME10"},
                "bulk_50": {"discount": 15, "code": "BULK15"},
                "student": {"discount": 5, "code": "STUDENT5"},
                "seasonal": {"discount": 20, "code": "SEASONAL20"}
            }
        }
    
    def _load_response_templates(self) -> Dict:
        """Load dynamic response templates"""
        return {
            "greeting": [
                "Hello! I'm your CookieCrave assistant! 🍪 What can I help you with today?",
                "Hi there! Ready to explore our delicious cookies? How can I assist you?",
                "Welcome to CookieCrave! I'm here to help with all your cookie needs. What's on your mind?"
            ],
            "product_recommendation": [
                "Based on your interest, I'd recommend our {product}. {description}. Would you like more details?",
                "You might love our {product}! {description}. It's one of our customer favorites!",
                "Great choice! Our {product} is perfect for {occasion}. {description}. Sound good?"
            ],
            "price_info": [
                "Our {product} is ₹{price}. {deal_info}",
                "The {product} costs ₹{price}. {deal_info}",
                "For {product}, the price is ₹{price}. {deal_info}"
            ],
            "delivery_info": [
                "We offer {delivery_type} delivery. {details}. Need it by a specific date?",
                "For delivery, we have {delivery_type} option. {details}. When do you need it?",
                "Delivery options include {delivery_type}. {details}. What works best for you?"
            ],
            "helpful_closing": [
                "Is there anything else I can help you with?",
                "Do you have any other questions about our cookies?",
                "Need more assistance? I'm here to help!"
            ]
        }
    
    def _get_user_context(self, user_id: str) -> Dict:
        """Get user context and history"""
        return self.user_profiles.get(user_id, {
            "preferences": [],
            "previous_orders": [],
            "viewed_products": [],
            "conversation_count": 0
        })
    
    def _update_user_context(self, user_id: str, message: str, response: str):
        """Update user context and conversation history"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "preferences": [],
                "previous_orders": [],
                "viewed_products": [],
                "conversation_count": 0
            }
        
        # Update conversation history
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            "timestamp": datetime.now(),
            "user_message": message,
            "bot_response": response
        })
        
        # Keep only last 10 conversations
        if len(self.conversation_history[user_id]) > 10:
            self.conversation_history[user_id] = self.conversation_history[user_id][-10:]
        
        self.user_profiles[user_id]["conversation_count"] += 1
    
    def _extract_intent(self, message: str) -> Dict:
        """Extract user intent and entities"""
        message_lower = message.lower()
        
        intents = {
            "product_inquiry": any(word in message_lower for word in ["cookie", "cookies", "product", "flavor", "variety"]),
            "pricing": any(word in message_lower for word in ["price", "cost", "how much", "₹", "rs", "rupees"]),
            "delivery": any(word in message_lower for word in ["delivery", "deliver", "shipping", "ship", "when", "time"]),
            "gifting": any(word in message_lower for word in ["gift", "present", "box", "wrap", "special occasion"]),
            "ordering": any(word in message_lower for word in ["order", "buy", "purchase", "checkout"]),
            "recommendation": any(word in message_lower for word in ["recommend", "suggest", "best", "popular", "favorite"]),
            "ingredients": any(word in message_lower for word in ["ingredient", "ingredients", "what's in", "contain", "allergen"]),
            "help": any(word in message_lower for word in ["help", "assist", "support", "question"])
        }
        
        # Extract entities
        entities = {}
        
        # Cookie types
        for cookie_type in self.product_knowledge["cookies"].keys():
            if cookie_type.replace("_", " ") in message_lower:
                entities["cookie_type"] = cookie_type
        
        # Numbers for quantities
        numbers = re.findall(r'\d+', message)
        if numbers:
            entities["quantity"] = int(numbers[0])
        
        return {"intents": intents, "entities": entities}
    
    def _generate_dynamic_response(self, intent_data: Dict, user_id: str) -> str:
        """Generate contextual, non-repetitive responses for any question"""
        intents = intent_data["intents"]
        entities = intent_data["entities"]
        user_context = self._get_user_context(user_id)
        message_lower = intent_data.get("original_message", "").lower()
        
        # Check for product catalog requests first (before intent checking)
        if any(word in message_lower for word in ["top products", "best products", "popular products", "top 5", "best sellers", "show top", "list top"]):
            return self._get_top_products()
        elif any(word in message_lower for word in ["categories", "list categories", "what categories", "cookie types", "show categories"]):
            return self._get_categories()
        elif any(word in message_lower for word in ["show images", "product images", "see pictures", "cookie pictures", "product photos", "view images", "display images"]):
            return self._get_product_images()
        elif any(word in message_lower for word in ["all products", "list products", "what products", "available products", "show all", "catalog"]):
            return self._get_all_products()
        
        # Check if any intents are True (meaning we detected a specific category)
        has_specific_intent = any(intents.values())
        
        # If no specific intent detected, handle as general question
        if not has_specific_intent:
            return self._handle_general_question(intent_data, user_id)
        
        # Greeting (when help intent is detected but no other specific intents)
        if intents.get("help") and not any(intents[k] for k in intents if k != "help"):
            return random.choice(self.response_templates["greeting"])
        
        # Product inquiry
        if intents.get("product_inquiry"):
            if entities.get("cookie_type"):
                product = self.product_knowledge["cookies"][entities["cookie_type"]]
                response = f"Our {product['name']} are amazing! {product['description']}. They're priced at ₹{product['price']} each and have a {product['rating']}⭐ rating."
                
                if user_context["conversation_count"] > 1:
                    response += f" {random.choice(self.response_templates['helpful_closing'])}"
                return response
            else:
                response = "We have several delicious cookie varieties! Our most popular are Chocolate Chip (₹199), Oatmeal Raisin (₹189), and Snickerdoodle (₹179). Which type interests you?"
                return response
        
        # Pricing inquiry
        if intents.get("pricing"):
            if entities.get("cookie_type"):
                product = self.product_knowledge["cookies"][entities["cookie_type"]]
                quantity = entities.get("quantity", 1)
                total_price = product["price"] * quantity
                
                if quantity >= 12:
                    deal_info = f"For {quantity} cookies, you'll get our bulk discount at ₹{total_price * 0.9:.0f} (10% off)!"
                elif quantity >= 6:
                    deal_info = f"For {quantity} cookies, that's ₹{total_price}. You might want to consider a dozen for ₹1899 to save money!"
                else:
                    deal_info = f"For {quantity} cookie{'s' if quantity > 1 else ''}, that's ₹{total_price}."
                
                return random.choice(self.response_templates["price_info"]).format(
                    product=product["name"],
                    price=product["price"],
                    deal_info=deal_info
                )
            else:
                return f"Our cookies range from ₹179-₹199 each. We offer great deals: 6 for ₹999, 12 for ₹1899, and bulk discounts for 50+ cookies!"
        
        # Delivery inquiry
        if intents.get("delivery"):
            delivery_options = []
            for option, details in self.product_knowledge["delivery"].items():
                if option != "free_threshold":
                    delivery_options.append(f"{option.replace('_', ' ').title()}: {details['time'] if 'time' in details else 'Same day if ordered before ' + details['cutoff']} for ₹{details['fee']}")
            
            delivery_info = " | ".join(delivery_options)
            delivery_info += f"\n\nFree delivery on orders over ₹{self.product_knowledge['delivery']['free_threshold']}!"
            
            return random.choice(self.response_templates["delivery_info"]).format(
                delivery_type="multiple",
                details=delivery_info
            )
        
        # Gifting inquiry
        if intents.get("gifting"):
            gift_options = []
            for option, price in self.product_knowledge["pricing"].items():
                if "gift_box" in option:
                    size = option.replace("gift_box_", "").title()
                    gift_options.append(f"{size} Gift Box: ₹{price}")
            
            gift_info = " | ".join(gift_options)
            gift_info += "\n\nAll gift boxes include beautiful packaging, custom message cards, and our freshest cookies!"
            
            return f"Perfect choice for gifting! We offer: {gift_info}. Which size would you prefer?"
        
        # Recommendation inquiry
        if intents.get("recommendation"):
            # Simple recommendation logic
            if user_context["viewed_products"]:
                last_viewed = user_context["viewed_products"][-1]
                recommendations = [k for k in self.product_knowledge["cookies"].keys() if k != last_viewed]
            else:
                recommendations = list(self.product_knowledge["cookies"].keys())
            
            if recommendations:
                recommended = random.choice(recommendations)
                product = self.product_knowledge["cookies"][recommended]
                
                return random.choice(self.response_templates["product_recommendation"]).format(
                    product=product["name"],
                    description=product["description"],
                    occasion=", ".join(product["best_for"][:2])
                )
        
        # Ingredients inquiry
        if intents.get("ingredients"):
            if entities.get("cookie_type"):
                product = self.product_knowledge["cookies"][entities["cookie_type"]]
                ingredients = ", ".join(product["ingredients"])
                allergens = ", ".join(product["allergens"])
                
                return f"Our {product['name']} contains: {ingredients}.\n\nAllergens: {allergens}. Need allergen-free options?"
            else:
                return "Our cookies are made with premium ingredients: flour, butter, sugar, eggs, vanilla extract, and high-quality chocolate. All cookies contain gluten and dairy. Do you have specific dietary concerns?"
        
        # Fallback to general question handler
        return self._handle_general_question(intent_data, user_id)
    
    def _handle_general_question(self, intent_data: Dict, user_id: str) -> str:
        """Handle general/random questions outside the cookie domain"""
        user_context = self._get_user_context(user_id)
        message_lower = intent_data.get("original_message", "").lower()
        
        # General knowledge responses
        general_responses = {
            "who_are_you": [
                "I'm your CookieCrave assistant! 🍪 I specialize in helping with cookies, products, and orders, but I'm happy to chat about anything!",
                "I'm the CookieCrave AI assistant! While my main focus is on our delicious cookies, I'm here to help with any questions you might have.",
                "I'm your friendly CookieCrave chatbot! I know all about our cookies, but I'm also here to assist with general questions."
            ],
            "what_can_you_do": [
                "I can help you with: 🍪 Cookie recommendations & details 💰 Pricing & deals 📦 Delivery & shipping 🎁 Gift options 📊 Order tracking 💬 General questions & conversation!",
                "I'm your all-in-one assistant! I can help with CookieCrave products, orders, and I'm also happy to chat about other topics or answer general questions.",
                "I'm here to help with everything CookieCrave-related, plus I'm great at general conversation! Ask me about cookies, life, or anything in between!"
            ],
            "how_are_you": [
                "I'm doing great, thanks for asking! Ready to help you find the perfect cookies or chat about anything else on your mind! 😊",
                "I'm feeling fantastic! Always excited to talk about cookies and help customers. How are you doing today?",
                "I'm doing wonderfully! Nothing makes me happier than helping people discover our delicious cookies. What can I help you with?"
            ],
            "weather": [
                "I don't have access to current weather information, but I can tell you that our cookies are perfect for any weather! ☀️🍪❄️ Would you like to know about our cookie varieties instead?",
                "I can't check the weather, but I can definitely recommend the perfect cookies for any weather condition! What's your favorite type of cookie?",
                "While I don't have weather data, I can suggest that our cookies are always a good choice, rain or shine! What kind of treats are you in the mood for?"
            ],
            "time": [
                f"I'm not sure about the current time, but it's always a good time for cookies! 🍪 Our bakery is open and ready to take your order. What cookies would you like?",
                "I don't have access to the current time, but I can tell you that our cookies are freshly baked daily! Would you like to know about our schedule?",
                "Time flies when you're thinking about cookies! While I can't tell you the time, I can definitely help you place an order for fresh cookies!"
            ],
            "joke": [
                "Why did the cookie go to the doctor? Because it felt crumbly! 😄 But seriously, our cookies are anything but crumbly - they're perfectly baked! Want to know more?",
                "What's a cookie's favorite life lesson? You can't make everyone happy, but you can make them cookies! 🍪 Speaking of which, what cookies would you like?",
                "Why do cookies never tell secrets? Because they're always getting baked! 😂 But our cookies are baked to perfection! Interested in trying some?"
            ],
            "compliment": [
                "Thank you so much! That's so sweet of you! Almost as sweet as our chocolate chip cookies! 🍪 What can I help you with today?",
                "Aw, thank you! You're making me blush - almost as red as our strawberry cookies! 😊 How can I assist you?",
                "That's so kind of you! I'm here to help, just like our cookies are here to delight! What would you like to know?"
            ],
            "default_general": [
                "That's an interesting question! While I specialize in helping with CookieCrave products and services, I'm always happy to chat. Is there anything about our cookies I can help you with?",
                "Interesting topic! I'm primarily focused on helping with all things CookieCrave-related, but I enjoy our conversations! Have you seen our cookie varieties?",
                "That's a great question! My main expertise is in cookies and customer service, but I'm here to help. Are you looking for something specific from CookieCrave?",
                "I appreciate your curiosity! While I'm designed to help with CookieCrave products and orders, I'm happy to chat. What brings you to our cookie shop today?"
            ]
        }
        
        # Check for product-related general questions
        if any(word in message_lower for word in ["top products", "best products", "popular products", "top 5", "best sellers", "show top", "list top"]):
            return self._get_top_products()
        elif any(word in message_lower for word in ["categories", "list categories", "what categories", "cookie types", "show categories"]):
            return self._get_categories()
        elif any(word in message_lower for word in ["show images", "product images", "see pictures", "cookie pictures", "product photos", "view images", "display images"]):
            return self._get_product_images()
        elif any(word in message_lower for word in ["all products", "list products", "what products", "available products", "show all", "catalog"]):
            return self._get_all_products()
        
        # Detect question type with better matching
        if "who are you" in message_lower or "what are you" in message_lower or "your name" in message_lower:
            return random.choice(general_responses["who_are_you"])
        elif "what can you do" in message_lower or "help me with" in message_lower or "what do you do" in message_lower:
            return random.choice(general_responses["what_can_you_do"])
        elif "how are you" in message_lower or "how you doing" in message_lower:
            return random.choice(general_responses["how_are_you"])
        elif "weather" in message_lower or "rain" in message_lower or "sunny" in message_lower or "cold" in message_lower or "hot" in message_lower:
            return random.choice(general_responses["weather"])
        elif "time" in message_lower or "clock" in message_lower or "what time" in message_lower:
            return random.choice(general_responses["time"])
        elif "joke" in message_lower or "funny" in message_lower or "laugh" in message_lower:
            return random.choice(general_responses["joke"])
        elif "thank" in message_lower or "thanks" in message_lower or "great" in message_lower or "awesome" in message_lower or "good job" in message_lower:
            return random.choice(general_responses["compliment"])
        else:
            return random.choice(general_responses["default_general"])
    
    def _get_top_products(self) -> str:
        """Get top 5 products"""
        try:
            import requests
            response = requests.get('http://127.0.0.1:8000/api/products/', timeout=5)
            if response.status_code == 200:
                products = response.json()
                # Sort by rating and get top 5
                top_products = sorted(products, key=lambda x: x.get('rating', 0), reverse=True)[:5]
                
                result = "🏆 **Top 5 Most Popular Cookies:**\n\n"
                for i, product in enumerate(top_products, 1):
                    result += f"{i}. **{product.get('name', 'Unknown')}** - ₹{product.get('price', 0)}\n"
                    result += f"   Rating: {product.get('rating', 'N/A')}⭐ | {product.get('description', 'No description')[:50]}...\n\n"
                
                result += "Would you like more details about any of these cookies?"
                return result
            else:
                return "I'm having trouble accessing our product catalog right now. Please try again later."
        except Exception as e:
            return f"Our top sellers include Chocolate Chip, Oatmeal Raisin, and Snickerdoodle cookies! Each is freshly baked with premium ingredients. Would you like to know more about any specific type?"
    
    def _get_categories(self) -> str:
        """Get product categories"""
        try:
            import requests
            response = requests.get('http://127.0.0.1:8000/api/categories/', timeout=5)
            if response.status_code == 200:
                categories = response.json()
                
                result = "🍪 **Available Cookie Categories:**\n\n"
                for i, category in enumerate(categories, 1):
                    result += f"{i}. **{category.get('name', 'Unknown')}**\n"
                    result += f"   {category.get('description', 'No description')}\n\n"
                
                result += f"We have {len(categories)} delicious categories to choose from! Which category interests you?"
                return result
            else:
                return "I'm having trouble accessing our categories right now. Please try again later."
        except Exception as e:
            return "We offer several cookie categories including Classic Favorites, Chocolate Lovers, and Seasonal Specials! Each category contains our freshest, most delicious cookies. What type of cookies are you in the mood for?"
    
    def _get_product_images(self) -> str:
        """Get product images information"""
        try:
            import requests
            response = requests.get('http://127.0.0.1:8000/api/products/', timeout=5)
            if response.status_code == 200:
                products = response.json()
                
                result = "📸 **Product Images Available:**\n\n"
                result += "You can view beautiful images of our cookies in the product catalog! Here's what you can see:\n\n"
                
                for i, product in enumerate(products[:6], 1):  # Show first 6 products
                    image_url = product.get('image', '')
                    if image_url:
                        result += f"{i}. **{product.get('name', 'Unknown')}**\n"
                        result += f"   📷 Image available: http://127.0.0.1:8000{image_url}\n"
                        result += f"   💰 Price: ₹{product.get('price', 0)}\n\n"
                    else:
                        result += f"{i}. **{product.get('name', 'Unknown')}**\n"
                        result += f"   📷 Image coming soon!\n"
                        result += f"   💰 Price: ₹{product.get('price', 0)}\n\n"
                
                result += "Visit our website at http://localhost:5173 to see all the delicious cookie images! 🍪"
                return result
            else:
                return "I'm having trouble accessing our product images right now. Please try again later."
        except Exception as e:
            return "Our cookie images are available on our website! You can see beautiful photos of all our cookies including Chocolate Chip, Oatmeal Raisin, and Snickerdoodle varieties. Visit http://localhost:5173 to view our complete catalog with images!"
    
    def _get_all_products(self) -> str:
        """Get all products"""
        try:
            import requests
            response = requests.get('http://127.0.0.1:8000/api/products/', timeout=5)
            if response.status_code == 200:
                products = response.json()
                
                result = f"🍪 **All Available Cookies ({len(products)} varieties):**\n\n"
                
                for i, product in enumerate(products[:10], 1):  # Show first 10 products
                    result += f"{i}. **{product.get('name', 'Unknown')}**\n"
                    result += f"   💰 Price: ₹{product.get('price', 0)}\n"
                    result += f"   ⭐ Rating: {product.get('rating', 'N/A')}\n"
                    result += f"   📝 {product.get('description', 'No description')[:60]}...\n\n"
                
                if len(products) > 10:
                    result += f"... and {len(products) - 10} more delicious varieties!\n\n"
                
                result += "Which cookie catches your eye? I can tell you more about any of them!"
                return result
            else:
                return "I'm having trouble accessing our full product catalog right now. Please try again later."
        except Exception as e:
            return "We have a wonderful variety of cookies including Chocolate Chip, Oatmeal Raisin, Snickerdoodle, Peanut Butter, and many more! Each is freshly baked daily with premium ingredients. What type of cookie would you like to know more about?"
    
    def _generate_openai_response(self, message: str, user_id: str) -> str:
        """Generate response using OpenAI with enhanced context"""
        api_key = os.getenv("OPENAI_API_KEY")
        # Force using dynamic responses for better control
        intent_data = self._extract_intent(message)
        intent_data["original_message"] = message
        return self._generate_dynamic_response(intent_data, user_id)
        
        user_context = self._get_user_context(user_id)
        conversation_history = self.conversation_history.get(user_id, [])
        
        # Build conversation context
        messages = [
            {
                "role": "system",
                "content": f"""You are an advanced AI assistant for CookieCrave, a premium cookie marketplace.

CONTEXTUAL INFORMATION:
- User has had {user_context['conversation_count']} conversations
- Previous interests: {', '.join(user_context['preferences'])}
- User conversation history: {len(conversation_history)} previous messages

PRODUCT KNOWLEDGE:
{json.dumps(self.product_knowledge, indent=2)}

RESPONSE GUIDELINES:
1. Be conversational and friendly
2. Use contextual information to personalize responses
3. Avoid repeating the same phrases
4. Ask follow-up questions to understand needs better
5. Provide specific, actionable recommendations
6. Use emojis appropriately for a friendly tone
7. Reference previous conversations when relevant
8. Never make up information not in your knowledge base

CURRENT DATE: {datetime.now().strftime('%Y-%m-%d')}
"""
            }
        ]
        
        # Add conversation history
        for conv in conversation_history[-3:]:  # Last 3 conversations
            messages.append({"role": "user", "content": conv["user_message"]})
            messages.append({"role": "assistant", "content": conv["bot_response"]})
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": messages,
                    "temperature": 0.7,  # Higher temperature for more variety
                    "max_tokens": 300,
                    "presence_penalty": 0.6,  # Reduce repetition
                    "frequency_penalty": 0.6,  # Reduce repetition
                },
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            return self._generate_dynamic_response(self._extract_intent(message), user_id)
    
    def get_response(self, message: str, user_id: str = "default") -> Dict:
        """Main method to get chatbot response"""
        message = message.strip()
        if not message:
            return {"reply": "Please tell me what you'd like to know about our cookies!", "user_id": user_id}
        
        # Extract intent and entities
        intent_data = self._extract_intent(message)
        intent_data["original_message"] = message  # Store original message for general questions
        
        # Generate response
        if os.getenv("OPENAI_API_KEY"):
            response = self._generate_openai_response(message, user_id)
        else:
            response = self._generate_dynamic_response(intent_data, user_id)
        
        # Update context
        self._update_user_context(user_id, message, response)
        
        # Update user preferences based on intent
        if intent_data["intents"].get("product_inquiry"):
            cookie_type = intent_data["entities"].get("cookie_type")
            if cookie_type and cookie_type not in self.user_profiles[user_id]["preferences"]:
                self.user_profiles[user_id]["preferences"].append(cookie_type)
        
        return {
            "reply": response,
            "user_id": user_id,
            "intent": intent_data,
            "context": self._get_user_context(user_id)
        }
