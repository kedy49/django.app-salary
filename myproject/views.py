from django.shortcuts import render

def toppage_template(request):
    return render(request, 'toppage.html')