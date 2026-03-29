#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from analytics.models import UserBehavior
from django.db.models import Count

print('Current action types in database:')
action_types = UserBehavior.objects.values('action_type').annotate(count=Count('id')).order_by('-count')
for item in action_types:
    print(f'- {item["action_type"]}: {item["count"]} records')

print('\nModel ACTION_TYPES choices:')
for choice in UserBehavior.ACTION_TYPES:
    print(f'- {choice[0]}: {choice[1]}')

print('\nChecking for any action types not in choices:')
db_actions = set(UserBehavior.objects.values_list('action_type', flat=True).distinct())
model_actions = set(choice[0] for choice in UserBehavior.ACTION_TYPES)
invalid_actions = db_actions - model_actions

if invalid_actions:
    print(f'Invalid action types found: {invalid_actions}')
else:
    print('All action types are valid!')

print('\nSample records:')
for behavior in UserBehavior.objects.order_by('-timestamp')[:5]:
    print(f'- {behavior.action_type}: {behavior.page_title or "No title"}')
