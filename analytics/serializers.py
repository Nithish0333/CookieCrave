from rest_framework import serializers
from .models import UserBehavior, UserSession, UserJourney, HeatmapData
from products.models import Product


class UserBehaviorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBehavior
        fields = [
            'id', 'user', 'session_id', 'action_type', 'page_url', 'page_title',
            'product', 'search_query', 'button_text', 'element_selector',
            'timestamp', 'time_on_page', 'scroll_depth', 'ip_address',
            'user_agent', 'referrer', 'metadata'
        ]
        read_only_fields = ['id', 'timestamp', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        
        # Extract IP address and user agent from request
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            validated_data['ip_address'] = ip
            validated_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
            validated_data['referrer'] = request.META.get('HTTP_REFERER', '')
        
        # Handle product_id from metadata
        metadata = validated_data.get('metadata', {})
        if 'product_id' in metadata and not validated_data.get('product'):
            product_id = metadata.pop('product_id')  # Remove from metadata
            try:
                product = Product.objects.get(id=product_id)
                validated_data['product'] = product
            except Product.DoesNotExist:
                # If product doesn't exist, just keep the product_id in metadata
                metadata['product_id'] = product_id
        
        # Update metadata after processing
        validated_data['metadata'] = metadata
        
        return super().create(validated_data)


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = [
            'id', 'session_id', 'user', 'start_time', 'end_time', 'duration',
            'page_views', 'products_viewed', 'searches_made', 'items_added_to_cart',
            'purchases_made', 'total_scroll_depth', 'device_type', 'browser',
            'operating_system', 'screen_resolution'
        ]
        read_only_fields = ['id', 'start_time', 'user']


class UserJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJourney
        fields = [
            'id', 'user', 'session', 'start_time', 'end_time', 'entry_point',
            'exit_point', 'conversion_goal', 'goal_completed', 'steps'
        ]
        read_only_fields = ['id', 'start_time', 'user']


class HeatmapDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeatmapData
        fields = [
            'id', 'page_url', 'click_x', 'click_y', 'viewport_width',
            'viewport_height', 'timestamp', 'user', 'session_id'
        ]
        read_only_fields = ['id', 'timestamp', 'user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)


class BulkBehaviorSerializer(serializers.Serializer):
    """Serializer for bulk tracking of multiple behaviors"""
    behaviors = UserBehaviorSerializer(many=True)

    def create(self, validated_data):
        behaviors_data = validated_data.get('behaviors', [])
        request = self.context.get('request')
        
        created_behaviors = []
        for behavior_data in behaviors_data:
            if request and hasattr(request, 'user') and request.user.is_authenticated:
                behavior_data['user'] = request.user
            
            # Extract IP address and user agent from request
            if request:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')
                behavior_data['ip_address'] = ip
                behavior_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
                behavior_data['referrer'] = request.META.get('HTTP_REFERER', '')
            
            # Use the single behavior serializer to handle creation and its custom logic
            serializer = UserBehaviorSerializer(data=behavior_data, context=self.context)
            if serializer.is_valid():
                behavior = serializer.save()
                created_behaviors.append(behavior)
            else:
                # Log or handle individual errors if needed
                print(f"Bulk tracking error for item: {serializer.errors}")
        
        return {'behaviors': created_behaviors}
