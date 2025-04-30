from rest_framework.decorators import api_view
from django.http import JsonResponse
import random
from faker import Faker
from datetime import datetime, timedelta

@api_view(['GET'])
def ads_list(request):
  limit = int(request.GET.get('limit', 10))
  offset = int(request.GET.get('offset', 0))
  faker = Faker()

  ads = []
  for _ in range(limit):
    ads.append({
      'id': str(faker.uuid4()),
      'name': faker.catch_phrase(),
      'status': random.choice(['ACTIVE', 'PAUSED', 'DELETED', 'ARCHIVED']),
      'impressions': random.randint(500, 100000),
      'clicks': random.randint(100, 10000),
      'spend': round(random.uniform(10.0, 10000.0), 2),
      'ctr': round(random.uniform(0.1, 10.0), 2),
      'campaign_id': str(faker.uuid4()),
      'created_time': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat(),
      'targeting': {
         'age_min': random.randint(18, 25),
         'age_max': random.randint(26, 65),
         'locations': [faker.country_code() for _ in range(random.randint(1, 3))],
         'interests': [faker.word() for _ in range(random.randint(3, 5))]
      }
    })
  total_count = random.randint(100, 1000)
  response = {
    'data': ads,
    'paging': {
      'cursors': {
        'before': str(offset),
        'after': str(offset + limit)
      },
      'next': f'{request.build_absolute_uri()}?limit={limit}&offset={offset + limit}' if (offset + limit) < total_count else None
    },
    'summary': {
      'impressions': sum(ad['impressions'] for ad in ads),
      'clicks': sum(ad['clicks'] for ad in ads),
      'spend': round(sum(ad['spend'] for ad in ads), 2)  
    }
  }
  return JsonResponse(response)

@api_view(['GET'])
def campaigns_list(request):
    return Response({
      'client': request.client.username,
      'data': [
        {"id": 1, "name": "FB Campaign 1", "budget": 1000},
        {"id": 2, "name": "FB Campaign 2", "budget": 2000}
      ]
    })