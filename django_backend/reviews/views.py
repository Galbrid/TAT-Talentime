import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import UserReview
from django.db import OperationalError


def serialize_review(r):
    return {
        'id': r.id,
        'name': r.name or (r.user.username if r.user else 'Anonymous'),
        'rating': r.rating,
        'comments': r.comments,
        'created_at': r.created_at.isoformat(),
    }


@csrf_exempt
def reviews_list(request):
    if request.method == 'GET':
        try:
            qs = UserReview.objects.order_by('-created_at')
            data = [serialize_review(r) for r in qs]
            return JsonResponse({'results': data})
        except OperationalError:
            # Table might not exist yet (migrations not applied)
            return JsonResponse({'results': []})

    if request.method == 'POST':
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        rating = int(payload.get('rating', 0))
        comments = payload.get('comments', '').strip()
        name = payload.get('name', '').strip()

        if rating < 1 or rating > 5 or not comments:
            return JsonResponse({'error': 'rating (1-5) and comments required'}, status=400)

        try:
            review = UserReview.objects.create(
                user=None,
                name=name,
                rating=rating,
                comments=comments,
                created_at=timezone.now()
            )
        except OperationalError:
            return JsonResponse({'error': 'Database not ready'}, status=500)

        return JsonResponse({'ok': True, 'review': serialize_review(review)})

    return JsonResponse({'error': 'Method not allowed'}, status=405)
