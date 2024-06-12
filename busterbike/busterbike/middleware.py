import json
from django.utils.deprecation import MiddlewareMixin

class JsonMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.body:
            try:
                request.json = json.loads(request.body)
            except json.JSONDecodeError:
                request.json = {}
        else:
            request.json = {}