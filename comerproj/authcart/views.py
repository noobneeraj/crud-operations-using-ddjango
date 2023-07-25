from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
# from django.views.generic import View
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
# from .utils import TokenGenerator,generate_token
# from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
# from django.core.mail import EmailMessage
# from django.conf import settings
# Create your views here.
def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']
        conform_password=request.POST['pass2']
        if password != conform_password:
            messages.warning(request,"Password is Not Matching")
            return render( request,'signup.html')
        try:
            User.objects.get(username=email)
            messages.info(request,"Email is already exists")
            return render(request,"signup.html")
        
        except Exception as identifier:
            pass
        user=User.objects.create_user(email,email,password)
        # user.is_active=False
        user.save()
        # email_subject="activate your Account"
        # message=render_to_string('Activate.html',{
        #     'user':user,
        #     'domain':'127.0.0.1:8000',
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token':generate_token.make_token(user)
        # })
        # EMAIL_HOST_USER=['20981a4257@raghuenggcollege.in']
        # email_message=EmailMessage(email_subject,message,settings,EMAIL_HOST_USER,[email])
        # email_message.send()
        # message.sucess(request,"Activate your Account by Clicking the link in your Gmail")
        messages.info(request,'Sign up Sucess')
        return redirect('/auth/login')
    return render(request,'signup.html')


# class ActivateAccountView(View):
#     def get(self,request,uidb64,token):
#         try:
#             uid=force_text(urlsafe_base64_decode(uidb64))
#             user=User.objects.get(pk=uid)
#         except Exception as identifier:
#             user=None

#         if user is not None and generate_token.check_token(user,token):
#             user.is_active=True
#             user.save()
#             messages.info(request,"Account Activated Sucessfully")
#             return redirect('/auth/login')
#         return render(request,'auth/activatefail.html')

def handlelogin(request):
    if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)

        if myuser is not None :
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')
        else:
            messages.error(request,"Login Success")
            return redirect('auth/login')

    return render(request,"login.html")

def handlelogout(request):
    logout(request)
    messages.info(request,'Log out Success')
    return redirect('/auth/login')
