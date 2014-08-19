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
                send_mail('FeelKm', 'Here is the msg.', 'noreply@feelkm.com',['gutierrez.quezada@hotmail.com'], fail_silently=False)
                return HttpResponse("1")
                """try:
                    send_mail("Recuperar", "Recuperar Msg", "noreply@feelkm.com",email_user)
                    return HttpResponse("1")

                except BadHeaderError:
                    HttpResponse('0')"""

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

                    return render(request, 'User/editProfile.html', {
                        'usr':request.user.username,
                        'DATALOGIN':DATALOGIN,
                        })

                else:
                     DATALOGIN="0"
                     return HttpResponseRedirect("/")
        else:
            DATALOGIN = "0"
            return HttpResponseRedirect("/")