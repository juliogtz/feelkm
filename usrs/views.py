from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User, Permission, check_password, is_password_usable
from django.shortcuts import get_object_or_404, render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from api.models import users, events, comments_events



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
                return HttpResponse("1")

        else:
            return HttpResponseRedirect("/")


def MyProfile(request, username):

    data = User.objects.filter(username=username)
    if(str(data)=="[]"):
        return HttpResponseRedirect("/")
    else:

        if request.user.is_active:
                if request.user.is_authenticated:
                    DATALOGIN_ID=request.user.id
                    DATALOGIN = users.objects.get(id_user_admin_id=DATALOGIN_ID)
                    return render(request, 'User/myprofile.html', {
                            'poll': 1,
                            'error_message': "You didn't select a choice.",
                            'data': data,
                            'usr':username,
                            'DATALOGIN':DATALOGIN

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
