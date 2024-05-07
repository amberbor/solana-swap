import asyncio
from src.app.use_case.job import job
from rest_framework.decorators import api_view
from django.http import JsonResponse

# Create your views here.
@api_view(['GET'])
def run(request):
    a = asyncio.run(job())
    return JsonResponse({'message' : 'Successful'})