from django.shortcuts import render
from .models import User, Group, Userinfo
from django.http import HttpResponse, QueryDict
from django.contrib.auth import authenticate, login, logout
from json import dumps
from .user_signup.password_checker import get_password_strength
from .user_signup.email_checker import get_email_report
from .user_signup.username_checker import get_username_strength
from annoying.functions import get_object_or_None
from django.contrib.auth.decorators import login_required
from .util import get_report , get_recently
from submission.judge_result import Judge_info
from Lutece.config import RECENT_NUMBER


def user_login(request):
    status = {
        'login_status': False}
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if username == None or password == None:
                raise ValueError("username or password do not exist")
            login_user = get_object_or_None( User , username = username )
            if login_user == None:
                raise ValueError("user not exist")
            if login_user.check_password(password):
                login(request, login_user)
                status['login_status'] = True
    except Exception as e:
        print( 'Error on user_login' , str( e ) )
    finally:
        return HttpResponse(dumps(status), content_type='application/json')


def user_logout(request):
    status = {
        'logout_status': True}
    logout(request)
    return HttpResponse(dumps(status), content_type='application/json')


def user_signup(request):
    status = {
        'signup_status': False,
        'error_msg': []}
    errormsg_list = status['error_msg']
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            displayname = request.POST.get('displayname')
            if username == None or password == None or email == None or displayname == None:
                raise ValueError( "Some sign up info do not exist." )
            # Check username
            if len( username ) > 0:
                login_user = get_object_or_None( User,
                    username = username)
                if login_user != None:
                    errormsg_list.append('Username already exists.')
                else:
                    usr_report = get_username_strength( username )
                    if len( usr_report ) > 0:
                        errormsg_list.append( usr_report )
            else:
                errormsg_list.append( 'Username can not be empty.' )
            # Check password
            if len( password ) > 0:
                pwd_check_report = get_password_strength( password )
                for _ in pwd_check_report:
                    errormsg_list.append( _ )
            else:
                errormsg_list.append( 'Password can not be empty.' )
            # Check email
            if len( email ) > 0:
                login_user = get_object_or_None( User,
                    email = email)
                if login_user != None:
                    errormsg_list.append('Email already exists.')
                else:
                    email_report = get_email_report( email )
                    if( len( email_report ) > 0 ):
                        errormsg_list.append( email_report )
            else:
                errormsg_list.append( 'Email can not be empty.' )
            # Check displayname
            if len( displayname ) == 0:
                errormsg_list.append( 'Displayname can not be empty.' )
            elif len( displayname ) > 12:
                errormsg_list.append( 'The length of displayname too long.' )                
            # Check error_msg
            if len( errormsg_list ) == 0:
                new_user = User(
                    username = username,
                    email = email,
                    display_name = displayname,
                    is_staff = False,
                    is_superuser = False,
                )
                new_user.set_password( password )
                status['signup_status'] = True
                new_user.set_group( Group.normal_user )
                new_user.save()
                login(request,new_user)
    except Exception as e:
        print( 'Error on user_signup' , str( e ) )
    finally:
        return HttpResponse( dumps( status ) , content_type = 'application/json' )


@login_required
def user_detail( request ):
    return render( request , 'user/user_detail.html' , {
        'info' : Userinfo.objects.get( user = request.user ),
        'analysis' : get_report( request.user ),
        'judge_color' : Judge_info.colour,
        'recently' : get_recently( request.user , RECENT_NUMBER ) })
