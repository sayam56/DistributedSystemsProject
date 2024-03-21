from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string


# Create your views here.
def homepage(request):
    return render(request, 'django_app/homepage.html')

def searchView(request):
    return render(request, 'django_app/search.html')
#
# def temp1(request):
#     return render(request, 'ByteBusterApp/template1.html', )
#
#
# def temp1edit(request):
#     return render(request, 'ByteBusterApp/template1editor.html', )
#
#
# def temp2(request):
#     return render(request, 'ByteBusterApp/template2.html', )
#
#
# def temp3(request):
#     return render(request, 'ByteBusterApp/template3.html', )
#
#
# def load_template(request, template_id):
#     template_name = 'ByteBusterApp/' + template_id + '.html'
#     html = render_to_string(template_name, request=request)
#     return HttpResponse(html)
