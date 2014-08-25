# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User, Permission, check_password, is_password_usable
from django.shortcuts import get_object_or_404, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from api.models import users, events, comments_events, events_favorites, photos
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail, BadHeaderError

import cloudinary
import cloudinary.uploader
import cloudinary.api
import random

import mandrill


import datetime

cloudinary.config(
  cloud_name = "htyoqtggc",
  api_key = "961935933259211",
  api_secret = "COwH0OL6qwHv5fhjD0ey2TjSdTo"
)


"""
# Register() - Return:
  0 = Someone is using the user.
  -1 = Problems with creating new user.
  -2 = The user was creating but no login
  -3 = Empty fields
  -4 = Email format error
  -5 = Someone is using email
"""

@csrf_protect
def Register(request):
        context = RequestContext(request)
        if request.method == 'POST':
            usr_usr=request.POST['user_user']
            email_user=request.POST['email_user']
            usr_exist = User.objects.filter(username=usr_usr.lower())
            email_exist = User.objects.filter(email=email_user.lower())


            if(request.POST['user_user']=="" or request.POST['email_user']=="" or request.POST['password_user']=="" or request.POST['name_user']=="" or request.POST['last_user']==""):
                return HttpResponse("-3")
            else:
                    if(str(usr_exist)=="[]"):
                        if(str(email_exist)=="[]"):

                            create_valid=User.objects.create(username = usr_usr.lower(), email = email_user.lower() , password = make_password(request.POST['password_user'], None, 'pbkdf2_sha256'), first_name = request.POST['name_user'], last_name = request.POST['last_user'])
                            getUserCreate = User.objects.get(username=usr_usr.lower())


                            if(str(create_valid)==str(usr_usr.lower())):


                                users.objects.create(id_user_admin_id=getUserCreate.id, id_facebook = request.POST['id_facebook'], firtsFacebookPic = request.POST['firtsFacebookPic'], auxData=request.POST['password_user'], status=1, mailing=0)
                                user_Auth=authenticate(username = usr_usr.lower(), password = request.POST['password_user'])

                                try:
                                    login(request, user_Auth)
                                    return HttpResponse("1")
                                except:
                                    return HttpResponse("-2")
                            else:
                                return HttpResponse("-1")
                        else:
                            return HttpResponse("-5") #-5

                    else:
                        return HttpResponse("0") # Someone is using the nameuser."""
        else:
            return HttpResponseRedirect("/")

"""
# LoginGo() - Return:
  0 = Error Login
  1 = Login !!
  -3 = Empty fields
  -4 = Email is no using

"""

@csrf_protect
def LoginGo(request):
    if request.method == 'POST':
        user_user=request.POST['user_user']
        if(request.POST['user_user']=="" or request.POST['password_user']==""):
            return HttpResponse("-3")
        else:
            usr_exist = User.objects.filter(username=user_user.lower())
            if(str(usr_exist)=="[]"):
                return HttpResponse("-4")
            else:
                user_Auth=authenticate(username =user_user.lower(), password =request.POST['password_user'])
                try:
                    logs=login(request, user_Auth)
                    return HttpResponse("1")
                except:
                    return HttpResponse("0")

    else:
        return HttpResponseRedirect("/")


@csrf_protect
def RecoveryPassword(request):
        if request.method == 'POST':
            email_user=request.POST['email_user']
            email_exist = User.objects.filter(email=email_user.lower())
            if(str(email_exist)=="[]"):
                return HttpResponse("0")
            else:
                # Enviar mail:

                try:

                    usr_recovery = User.objects.get(email = email_user )
                    mandrill_client = mandrill.Mandrill('GxVtwaebpEBKwF2bOSYvtw')
                    message = {
                     'auto_html': None,
                     'auto_text': None,
                     'from_email': 'info@feelkm.com',
                     'from_name': 'FeelKm',
                     'global_merge_vars': [{'content': 'merge1 content', 'name': 'merge1'}],
                     'headers': {'Reply-To': 'message.reply@feelkm.com'},
                     'html': '<html><head></head><body><div><img src="http://res.cloudinary.com/htyoqtggc/image/upload/v1408998865/logo-feelkm_b9mkca.png"></div><p style="font-family: Helvetica Neue; font-size: 14px; font-weight: normal; color:#4c4c4c; ">Recuperaci&oacute;n de contrase&ntilde;a FeelKm.</p><p style="font-family: Helvetica Neue; font-size: 13px; font-weight: normal; color:#4c4c4c;">Julio usted ha solicitado la recuperaci&oacute;n de su contrase&ntilde;a<br>Le recomendados entrar a la pltaforma lo antes posible y generar un nuevo cambio de contrase&ntilde;a.</p><p style="font-family: Helvetica Neue; font-size: 13px; font-weight: normal; color:#4c4c4c;">La contrase&ntilde;a actual: '+usr_recovery.password+'</p></body></html>',
                     'important': False,
                     'inline_css': None,
                     'merge': True,
                     'preserve_recipients': None,
                     'return_path_domain': None,
                     'signing_domain': None,
                     'subject': 'Recuperación de Contraseña',
                     'text': 'Example text content',
                     'to': [{'email': usr_recovery.email,
                             'name': usr_recovery.first_name,
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
                    return HttpResponse('-1')
                    #raise

        else:
            return HttpResponseRedirect("/")

@cache_page(60)
def MyProfile(request, username):
    data = User.objects.filter(username=username)
    if(str(data)=="[]"):
        return HttpResponseRedirect("/")
    else:

        if request.user.is_active:
                if request.user.is_authenticated:

                    user_aux = users.objects.get(id_user_admin=data)
                    DATALOGIN_ID=request.user.id
                    DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)

                    #Eventos favoritos:
                    eventsf = events_favorites.objects.filter(id_user_admin=request.user.id)
                    count_eventsf= eventsf.count()

                    #Pics of favorites events
                    list_pic_favorites = []
                    if(count_eventsf>0):
                        for envd in eventsf:
                            pics = photos.objects.filter(id_event=envd.id_event)
                            #print envd.id_event.id
                            contp=pics.count()
                            if(contp>0):
                                list_pic_favorites.append({envd.id_event.id:pics})
                            else:
                                list_pic_favorites.append({envd.id_event.id:0})

                    #print list_pic_favorites

                    #Pics add by the user login:
                    pics_add = photos.objects.filter(id_user_admin=request.user.id)
                    count_pics_add = pics_add.count()


                    #Comments of different events:
                    comments_add = comments_events.objects.filter(id_user_admin=request.user.id)
                    count_comments_add = comments_add.count()

                    list_comments_event =[]
                    for comn in comments_add:
                        #print comn.title_comment
                        #print comn.comment
                        #print comn.date
                        #print comn.id_event.name_event
                        #print comn.id_event.city
                        #print comn.id_event.region
                        #print comn.id_event.country
                        #print "\n"
                        pics_of_event = photos.objects.filter(id_event=comn.id_event.id)
                        count_pics_of_event= pics_of_event.count()
                        if(count_pics_of_event<=0):
                            list_comments_event.append({"comments":comn, "imgs":0})
                        else:
                            list_comments_event.append({"comments":comn, "imgs":pics_of_event})

                    print list_comments_event









                    return render(request, 'User/myprofile.html', {
                            'poll': 1,
                            'error_message': "You didn't select a choice.",
                            'data': data,
                            'usr':username,
                            'DATALOGIN':DATALOGIN,
                            'user_aux':user_aux,
                            'count_eventsf':count_eventsf,
                            'list_event_favorites':eventsf,
                            'list_pic_favorites':list_pic_favorites,
                            'count_pics_add':count_pics_add,
                            'list_pics_adds_user':pics_add,
                            'count_comments_add':count_comments_add,
                            'list_comments_event':list_comments_event,


                        })
                else:
                     DATALOGIN="0"
                     return HttpResponseRedirect("/")
        else:
            DATALOGIN = "0"
            return HttpResponseRedirect("/")



def Privacy(request):

     return render(request, 'Legal/privacy.html', {
        })


@csrf_protect
def Facebook_Register(request):

        if request.method == 'POST':

            id_facebook=request.POST['id_facebook']
            name_full=request.POST['name_full']
            email=request.POST['email']
            gender=request.POST['gender']
            last_name=request.POST['last_name']
            first_name=request.POST['first_name']
            locale=request.POST['locale']

            """
            # Return val:
            0 - El usuario de facebook no existe en nustro registro
            1 - El usuario de facebook si existe hacer login y direccionar.
            """

            # Verificar si el id_facebook se esta usando
            # Si se esta usando hacer login
            # Si no se esta usando redirigir a formulario de registro junto con los datos.
            idfacebook_exist = users.objects.filter(id_facebook=id_facebook)

            if(str(idfacebook_exist)=="[]"):
                return HttpResponse("0")
            else:
                # Hacer login
                getUSer=users.objects.get(id_facebook=id_facebook)
                DataUserLogin = User.objects.get(id=getUSer.id_user_admin_id)
                user_Auth=authenticate(username=DataUserLogin.username , password = getUSer.auxData)
                try:
                    logs=login(request, user_Auth)
                    return HttpResponse("1")
                except:
                    return HttpResponse("-1")

                #return HttpResponse(str(id_facebook)+" "+str(name_full)+" "+str(email)+" "+str(gender)+" "+str(last_name)+" "+str(first_name)+" "+str(locale))

        else:
            return HttpResponseRedirect("/")



def LogoutUser(request):

    logout(request)

    return HttpResponseRedirect("/")


def delFavorites(request, id):

    if request.user.is_active:
        if request.user.is_authenticated:

            id_event = events.objects.get(id=int(id))
            id_user_instance = User.objects.get(id=request.user.id)

            try:
                favorite=events_favorites.objects.get(id_event=id_event, id_user_admin=id_user_instance)
                favorite.delete()

                return HttpResponseRedirect("/km/"+request.user.username+"/")

            except:
                return HttpResponseRedirect("/km/"+request.user.username+"/")

        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def delComment(request, id):

    if request.user.is_active:
        if request.user.is_authenticated:

            #id_event = events.objects.get(id=int(id))
            id_user_instance = User.objects.get(id=request.user.id)

            try:
                comment=comments_events.objects.get(id=id, id_user_admin=id_user_instance)
                comment.delete()

                return HttpResponseRedirect("/km/"+request.user.username+"/")

            except:
                return HttpResponseRedirect("/km/"+request.user.username+"/")

        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def EditMyProfile(request,):

        if request.user.is_active:
                if request.user.is_authenticated:

                    DATALOGIN_ID=request.user.id
                    DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)

                    month=""
                    genero=""

                    if(DATALOGIN.birth):

                        if(DATALOGIN.birth.month == 0):
                            month="Mes"
                        if(DATALOGIN.birth.month == 1):
                            month="Enero"
                        if(DATALOGIN.birth.month == 2):
                            month="Febrero"
                        if(DATALOGIN.birth.month == 3):
                            month="Marzo"
                        if(DATALOGIN.birth.month == 4):
                            month="Abril"
                        if(DATALOGIN.birth.month == 5):
                            month="Mayo"
                        if(DATALOGIN.birth.month == 6):
                            month="Junio"
                        if(DATALOGIN.birth.month == 7):
                            month="Julio"
                        if(DATALOGIN.birth.month == 8):
                            month="Agosto"
                        if(DATALOGIN.birth.month == 9):
                            month="Septiembre"
                        if(DATALOGIN.birth.month == 10):
                            month="Octubre"
                        if(DATALOGIN.birth.month == 11):
                            month="Noviembre"
                        if(DATALOGIN.birth.month == 12):
                            month="Diciembre"

                        if(DATALOGIN.gender == ""):
                            genero="Genero"
                        if(DATALOGIN.gender == "F"):
                            genero="Mujer"
                        if(DATALOGIN.gender == "M"):
                            genero="Hombre"




                    return render(request, 'User/editProfile.html', {

                        'usr':request.user.username,
                        'DATALOGIN':DATALOGIN,
                        'month':month,
                        'genero':genero,




                        })

                else:
                     DATALOGIN="0"
                     return HttpResponseRedirect("/")
        else:
            DATALOGIN = "0"
            return HttpResponseRedirect("/")



def UpdateMyProfile(request):

    if request.user.is_active:
                if request.user.is_authenticated:
                    if request.method == 'GET':

                        return HttpResponseRedirect("/")
                        #return HttpResponse("1")

                    else:

                        user_name = request.POST["user_name"]
                        user_birth_month = request.POST["user_birth_month"]
                        user_birth_day = request.POST["user_birth_day"]
                        user_birth_country = request.POST["user_birth_country"]
                        user_sex = request.POST["user_sex"]
                        user_lastname = request.POST["user_lastname"]
                        user_birth_year = request.POST["user_birth_year"]
                        user_city = request.POST["user_city"]
                        user_favorite_distance = request.POST["user_favorite_distance"]

                        user_about = request.POST["user_about"]
                        filesend = ""
                        fileaux=""

                        if(user_name == "" or user_birth_month == "0" or user_birth_day == "0" or user_birth_country =="0" or user_sex == "0" or user_lastname == "" or user_birth_year == "0" or user_city == "" or user_favorite_distance == "0"):

                            return HttpResponseRedirect("/")
                            #return HttpResponse("1")

                        else:

                            for filename, file in request.FILES.iteritems():

                                file_txt=request.FILES[filename].name
                                file_txt=file_txt.split(".")
                                if(file_txt[1]=="jpeg"  or file_txt[1]=="jpg" or file_txt[1]=="png" or file_txt[1]=="gif"):

                                    try:
                                          filesend = ""+file_txt[0]+""+str(random.randrange(9999999999999999999999999))+""
                                          fileaux = filesend
                                          json=cloudinary.uploader.upload(
                                          request.FILES[filename],
                                          public_id = filesend,
                                          crop = 'limit',
                                          #width = 2000,
                                          #height = 2000,
                                          eager = [
                                            { 'width': 200, 'height': 200,
                                              'crop': 'thumb', 'gravity': 'face',
                                              'radius': 20, 'effect': 'sepia' },
                                            { 'width': 100, 'height': 150,
                                              'crop': 'fit', 'format': 'png' }
                                          ],
                                          tags = ['']
                                          )

                                    except:
                                        filesend = ""
                                else:
                                    filesend = ""


                            try:

                                    #Update first table
                                    request.user.first_name=user_name
                                    request.user.last_name=user_lastname
                                    request.user.save()

                                    newDateBirth = datetime.date(int(user_birth_year), int(user_birth_month), int(user_birth_day))

                                    #Update second table
                                    t = users.objects.get(id_user_admin=request.user)
                                    t.country = user_birth_country # change field
                                    t.city = user_city # change field
                                    t.prefer_km = user_favorite_distance  # change field
                                    t.gender = user_sex  # change field
                                    t.birth = newDateBirth # change field
                                    t.about = user_about

                                    if(filesend != ""):
                                        t.pic_url=filesend

                                    t.save() # this will update only

                                    return HttpResponseRedirect("/edit-profile/?edit=true#status-content-operation")


                            except:
                                return HttpResponseRedirect("/edit-profile/")


                else:

                    return HttpResponseRedirect("/")
    else:

         return HttpResponseRedirect("/")




def ChangePassword(request):

     if request.user.is_active:
                if request.user.is_authenticated:
                    if request.method == 'GET':
                        return HttpResponseRedirect("/")
                    else:

                        #DATALOGIN_ID=request.user.id
                        #DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)

                        #make_password(request.POST['password_user'], None, 'pbkdf2_sha256')

                        current_password=request.POST['currentpassword']
                        newpassword=request.POST['newpassword']


                        if(current_password == "" or newpassword == "" or current_password == None or newpassword == None ):

                           return  HttpResponse("0")

                        else:

                            checkpass = check_password(current_password, request.user.password)
                            if(checkpass == False or checkpass == 0 ):
                                return HttpResponse("-1")

                            if(checkpass == True or checkpass == 1 ):

                                try:


                                    request.user.set_password(newpassword)
                                    request.user.save()

                                    t = users.objects.get(id_user_admin=request.user)
                                    t.auxData = newpassword  # change field
                                    t.save() # this will update only

                                    return HttpResponse("1")

                                except:

                                    return HttpResponse("-2")


                else:

                     return HttpResponseRedirect("/")
     else:

            return HttpResponseRedirect("/")