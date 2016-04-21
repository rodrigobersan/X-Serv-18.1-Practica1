from django.shortcuts import render
from django.http import HttpResponse
from models import Urls
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# Create your views here.

@csrf_exempt
def main2(request):
    if request.method == 'GET':
        msg = 'Introduce una URL para acortarla:'
    elif request.method == 'POST':
        longurl = request.POST['url']
        isvalid,longurl = checkurl(longurl)
        if isvalid:
            urls = Urls.objects.all()
            url = Urls(longurl=longurl, shorturl=request.get_host() + '/' + str(len(urls) + 1))
            url.save()
            msg = 'Se ha agregado una nueva entrada a la base de datos:'
        elif not isvalid and longurl != '':
            msg = 'La URL que has introducido ya estaba almacenada en la base de datos:'
        elif not isvalid and longurl == '':
            msg = 'No se puede agregar una URL vacia a la base de datos.'
    template = get_template('template.html')
    urls = Urls.objects.all()
    context = ({'urls':urls,
                'msg':msg})
    return HttpResponse(template.render(context))

def number(request,ident):
    longurl = ''
    urls = Urls.objects.all()
    for url in urls:
        shorturl = url.shorturl
        index = shorturl.split('/')[-1]
        if ident == index:
            longurl = url.longurl
            break
    if longurl == '':
        msg = 'No hay ningun elemento con el identificador ' + str(ident) + ' en la base de datos.'
        template = get_template('template.html')
        urls = Urls.objects.all()
        context = ({'urls':urls,
                    'msg':msg})
        return HttpResponse(template.render(context))
    return redirect(longurl)

def checkurl(longurl):
    if longurl == '':
        return False, longurl
    if longurl[0:7] != 'http://' or longurl[0:8] != 'https://':
        longurl = 'http://' + longurl
    try:
        search = Urls.objects.get(longurl=longurl)
    except Urls.DoesNotExist:
        return True, longurl
    return False, longurl
