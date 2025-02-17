from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse


def about(request):
    return HttpResponse("О сайте")


def main(request):
    return HttpResponse("Выбор прогноза")
 
def contact(request):
    return HttpResponse("Контакты")
