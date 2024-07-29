from http.client import HTTPResponse
from django.shortcuts import render
from django.views import View

# Create your views here.
class PrivacyView(View):
    def get(self, request):
        return render(request, 'privacy.html')
    
class DeleteAccountView(View):
    def get(self, request):
        return render(request, 'delete.html')