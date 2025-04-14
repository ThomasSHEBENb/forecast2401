from django.shortcuts import render

def main_page(request):
    return render(request, 'main.html')

def about_page(request):
    return render(request, 'about.html')

def contact_page(request):
    return render(request, 'contact.html')
