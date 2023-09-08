from django.shortcuts import render
# from django.http import HttpResponse
# from .models import College, Student


# # Create your views here.
# def select(r):
#     admittedto = Student.objects.select_related('admitted_to').values()
#     return render(r, HttpResponse(<h1>Select_Related</h1>), {'output': admittedto})