"""
Unsplash API integration for fetching unique product images
"""
import requests
import logging
import time
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

class UnsplashAPI:
    def __init__(self):
        self.access_key = getattr(settings, 'UNSPLASH_ACCESS_KEY', None)
        self.base_url = "https://api.unsplash.com"
        self.headers = {
            'Authorization': f'Client-ID {self.access_key}',
            'Content-Type': 'application/json'
        }
    
    def search_photos(self, query, per_page=1):
        """Search for photos based on query"""
        if not self.access_key:
            logger.error("Unsplash API key not configured")
            return None
        
        # Rate limiting - cache results for 1 hour
        cache_key = f"unsplash_search_{query.replace(' ', '_')}_{per_page}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result
        
        try:
            url = f"{self.base_url}/search/photos"
            params = {
                'query': query,
                'per_page': per_page,
                'content_filter': 'high',  # Only high-quality images
                'order_by': 'relevant'     # Most relevant first
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            # Cache the result for 1 hour
            cache.set(cache_key, data, 3600)
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching from Unsplash API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error with Unsplash API: {e}")
            return None
    
    def get_food_image_url(self, product_name, category_name=None):
        """Get a relevant food image URL for a product"""
        
        # Create search queries based on product name and category
        search_queries = []
        
        # Primary query - product name
        clean_name = self._clean_product_name(product_name)
        search_queries.append(clean_name)
        
        # Secondary queries
        if category_name:
            search_queries.append(self._clean_category_name(category_name))
        
        # Fallback queries
        if 'cookie' in product_name.lower():
            search_queries.extend(['homemade cookies', 'fresh baked cookies', 'chocolate chip cookies'])
        elif 'cake' in product_name.lower():
            search_queries.extend(['chocolate cake', 'birthday cake', 'dessert cake'])
        elif 'milkshake' in product_name.lower():
            search_queries.extend(['chocolate milkshake', 'ice cream shake', 'sweet beverage'])
        elif 'chocolate' in product_name.lower():
            search_queries.extend(['dark chocolate', 'chocolate bar', 'chocolate truffles'])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_queries = []
        for query in search_queries:
            if query.lower() not in seen:
                seen.add(query.lower())
                unique_queries.append(query)
        
        # Try each query until we find a good image (limit to 2 attempts for speed)
        for query in unique_queries[:2]:
            result = self.search_photos(query, per_page=1)
            if result and result.get('results'):
                photo = result['results'][0]
                # Get the regular quality image URL
                image_url = photo['urls']['regular']
                logger.info(f"Found Unsplash image for '{product_name}' using query: {query}")
                return image_url
        
        # If no results, return a default food image immediately
        logger.warning(f"No Unsplash image found for '{product_name}', using default")
        return self._get_default_food_image()
    
    def _clean_product_name(self, product_name):
        """Clean product name for better search results"""
        # Remove common prefixes/suffixes that don't help with image search
        name = product_name.lower()
        
        # Remove product numbers and variants
        words_to_remove = ['#', 'premium', 'artisan', 'deluxe', 'classic', 'ultimate', 
                          'signature', 'handcrafted', 'gourmet', 'decadent']
        
        for word in words_to_remove:
            name = name.replace(word, '')
        
        # Clean up extra spaces and return
        name = ' '.join(name.split())
        return name if name else 'cookies'
    
    def _clean_category_name(self, category_name):
        """Clean category name for search"""
        return category_name.lower() if category_name else 'food'
    
    def _get_default_food_image(self):
        """Get a default food image URL"""
        return 'https://images.unsplash.com/photo-1495521821757-a1efb6729352?w=800&q=80'

# Global instance
unsplash_api = UnsplashAPI()

def get_unique_product_image(product_name, category_name=None):
    """Get a unique image URL for a product using Unsplash API"""
    return unsplash_api.get_food_image_url(product_name, category_name)
