from django.shortcuts import render

def about(request):
    return render(request, 'forecast/about.html')

def main(request):
    return render(request, 'forecast/main.html')

def contact(request):
    return render(request, 'forecast/contact.html')
