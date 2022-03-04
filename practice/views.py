from django.shortcuts import render

def error_404(request, exception):
    data = {}
    return render(request, 'blog/404.html', data)