# from django.http import HttpResponse
# from django.template import loader
from django.shortcuts import render


def start_page(request):
    # template = loader.get_template('index.html')
    # context = {}
    # render_page = template.render(context, request)
    # return HttpResponse(render_page)
    return render(request, 'index.html')
