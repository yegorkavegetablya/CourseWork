from django.shortcuts import render
from django.http import HttpResponse
from course_work.func import sum
# Create your views here.
def index1(request, a, b):
    return HttpResponse(f"Sum: {sum(a, b)}")