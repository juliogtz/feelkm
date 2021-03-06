from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponse
#from rest_framework import viewsets, status
#from api.serializers import UserSerializer, GroupSerializer

#class UserViewSet(viewsets.ModelViewSet):
#    queryset = User.objects.all()
#    serializer_class = UserSerializer


#class GroupViewSet(viewsets.ModelViewSet):
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer


#from rest_framework.decorators import api_view
#from rest_framework.response import Response
from api.models import events
#from api.serializers import SinippetSerializer
from django.db.models import Q
from django.core import serializers
from django.http import HttpResponse

import mandrill

import SocketServer
from wsgiref import handlers
SocketServer.BaseServer.handle_error = lambda *args, **kwargs: None
handlers.BaseHandler.log_exception = lambda *args, **kwargs: None

import json
from django.views.decorators.cache import cache_page

# Views from api.
#@api_view(['GET'])
#def event_list(request, ):


#    if request.method == 'GET':
#        snippets = events.objects.filter(name_event__icontains='Holasdsd')
#        serializer = SinippetSerializer(snippets, many=True)
#        return Response(serializer.data)


#Views Search api:
#@api_view(['GET'])
#def search(request):
#    #print query
#    if request.method == 'GET':
#        query= request.GET.get('query','')
#        snippets = events.objects.filter(Q(name_event__icontains=query) | Q(city__icontains=query) | Q(region__icontains=query) | Q(country__icontains=query) | Q(description__icontains=query) | Q(distan_txt__icontains=query) | Q(distan_txt__icontains=query) | Q(short_desc__icontains=query) | Q(region_l__icontains=query))
#        serializer = SinippetSerializer(snippets, many=True)
#        return Response(serializer.data)



#Views Search api:
@cache_page(60)
def autocomplete(request):
    #print query
    if request.method == 'GET':
        query= request.GET.get('query','')
        snippets = events.objects.filter(Q(name_event__icontains=query) | Q(city__icontains=query) | Q(region__icontains=query) | Q(country__icontains=query) | Q(description__icontains=query) | Q(distan_txt__icontains=query) | Q(distan_txt__icontains=query) | Q(short_desc__icontains=query) | Q(region_l__icontains=query))[:100]
        #serializer = SinippetSerializer(snippets, many=True)
        con = snippets.count()
        #print con
        auxcon=1
        objects = u'{"query": "Unit", \n "suggestions": [\n'
        for i in snippets:
            if(auxcon==con):
                objects += u'"%s"' % (i.name_event.replace('"',''))
            else:
                objects += u'"%s",' % (i.name_event.replace('"',''))
            auxcon=auxcon+1
        #objects=objects.strip(",\n")
        objects+=u']}'


        js =json.dumps(objects)

        js = json.loads(js)

        #return Response(serializer.data)
    return HttpResponse(js,content_type="application/json")

@cache_page(60)
def autocomplete_second(request):
    #print query
    if request.method == 'GET':
        query= request.GET.get('query','')
        snippets = events.objects.filter(Q(name_event__icontains=query) | Q(city__icontains=query) | Q(region__icontains=query) | Q(country__icontains=query) | Q(description__icontains=query) | Q(distan_txt__icontains=query) | Q(distan_txt__icontains=query) | Q(short_desc__icontains=query) | Q(region_l__icontains=query))[:100]
        #serializer = SinippetSerializer(snippets, many=True)
        con = snippets.count()
        #print con
        auxcon=1
        objects = u'{"query": "Unit", \n "suggestions": [\n'
        for i in snippets:
            if(auxcon==con):
                objects += u'{"value":"%s", "data":"%s"}' % (i.name_event.replace('"',''), i.country.replace('"',''))
            else:
                objects += u'{"value":"%s", "data":"%s"},' % (i.name_event.replace('"',''), i.country.replace('"',''))
            auxcon=auxcon+1
        #objects=objects.strip(",\n")
        objects+=u']}'

        js =json.dumps(objects)

        js = json.loads(js)

        #return Response(serializer.data)
    return HttpResponse(js,content_type="application/json")

"""
{
    // Query is not required as of version 1.2.5
    "query": "Unit",
    "suggestions": [
        { "value": "United Arab Emirates", "data": "AE" },
        { "value": "United Kingdom",       "data": "UK" },
        { "value": "United States",        "data": "US" }
    ]
}

{
    "query": "Unit",
    "suggestions": ["United Arab Emirates", "United Kingdom", "United States"]
}
"""

def SendFeedback(request):
     if request.method == 'POST':
        if request.user.is_active:
            if request.user.is_authenticated:
                try:
                    msg_user=request.POST['msg']
                    mandrill_client = mandrill.Mandrill('GxVtwaebpEBKwF2bOSYvtw')
                    message = {
                     'auto_html': None,
                     'auto_text': None,
                     'from_email': 'info@feelkm.com',
                     'from_name': 'FeelKm',
                     'global_merge_vars': [{'content': 'merge1 content', 'name': 'merge1'}],
                     'headers': {'Reply-To': 'message.reply@feelkm.com'},
                     'html': '<p>Mensaje: '+msg_user+'</p> <p>Mail: '+request.user.email+'</p> <p>Nombre: '+request.user.first_name+'</p>',
                     'important': False,
                     'inline_css': None,
                     'merge': True,
                     'preserve_recipients': None,
                     'return_path_domain': None,
                     'signing_domain': None,
                     'subject': 'Feedback FeelKm',
                     'text': 'Example text content',
                     'to': [{'email': 'jc.gutierrezq@gmail.com',
                             'name': 'Jul',
                             'type': 'to'}],
                     'track_clicks': None,
                     'track_opens': None,
                     'tracking_domain': None,
                     'url_strip_qs': None,
                     'view_content_link': None}
                    result = mandrill_client.messages.send(message=message, async=False, ip_pool='Main Pool')
                    '''
                    [{'_id': 'abc123abc123abc123abc123abc123',
                      'email': 'recipient.email@example.com',
                      'reject_reason': 'hard-bounce',
                      'status': 'sent'}]
                    '''
                    return HttpResponse("1")

                except mandrill.Error, e:
                    # Mandrill errors are thrown as exceptions
                    print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
                    # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'
                    return HttpResponse('2')
                    #raise

            else:
                return HttpResponse("-1")
        else:
            return HttpResponse("-2")
     else:
        return HttpResponseRedirect("/")