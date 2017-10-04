import os
import subprocess as sub
from django.shortcuts import render

# Create your views here.
from blog.models import Blog, Category
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from blog.forms import ContactForm
from blog.register import Register
from blog.passphrase import UpdateUser

def index(request):
    return render(request, 'index.html', {
        'categories': Category.objects.all(),
        'posts': Blog.objects.all()[:5]
    })

def view_post(request, slug):   
    return render_to_response('view_post.html', {
        'post': get_object_or_404(Blog, slug=slug)
    })

def view_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render_to_response('view_category.html', {
        'category': category,
        'posts': Blog.objects.filter(category=category)[:5]
    })
def email(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, "email.html", {'form': form})
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
	    
        validateEmail(from_email)

        try:
            send_mail(subject, message, from_email, ['admin@example.com'])
            return redirect('thanks')
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        
    

def thanks(request):
    return HttpResponse('Thank you for your message.')

def added(request):
    return HttpResponse('You have been added. Thank you.')

def register(request):
    if request.method == 'GET':
        reg = Register()
    else:
        reg = Register(request.POST)
        if reg.is_valid():
            username = reg.cleaned_data['username']
            user_email = reg.cleaned_data['user_email']
            first_name = reg.cleaned_data['first_name']
            last_name = reg.cleaned_data['last_name']
        
            validateEmail(user_email)
	       #password1 = reg.cleaned_data['pasw']
        
        try:
		   ##add user to ldap
        
            os.environ['email'] = user_email
            os.environ['username'] = username
            os.environ['first'] = first_name
            os.environ['second'] =  last_name

            out = os.system('ldapsearch -H ldap://127.0.0.1 -x -D "cn=admin,dc=mysite,dc=com" -w "1234"  -b "uid=iliana,ou=users,dc=mysite,dc=com"')
            if out != 0:
                os.system("bash  /root/newuser.sh $email $username $first $second ")
                return redirect('added')
        			#os.system("ldappasswd -H ldap://127.0.0.1 -x -D 'cn=admin,dc=mysite,dc=com' -w '1234' -s '$password1' 'uid=$2,ou=users,dc=mysite,dc=com'")
            else: 
                return HttpResponse('User alredy exists')
        except BadHeaderError:
                return HttpResponse('Invalid header found.')
        # return redirect('thanks')
    return render(request, "register.html", {'reg': reg})


def updateuser(request):
    if request.method == 'GET':
        up = UpdateUser()
    else:
        up = UpdateUser(request.POST)
        if up.is_valid():
            username = up.cleaned_data['onoma']
            password1 = up.cleaned_data['pasw']
            os.environ['username'] = username
            os.environ['password1'] = password1
            try:    	
                p = os.system('ldappasswd -H ldap://127.0.0.1 -x -D "cn=admin,dc=mysite,dc=com" -w "1234" -s $password1 "uid=${username},ou=users,dc=mysite,dc=com"')
                if p == 0:    		  	
                    return HttpResponse('thanks')
                else:
                    return HttpResponse('user not found')
                #return redirect('added')
            except:
                return HttpResponse('Invalid header found.')
          		#return redirect('thanks')
        return render(request, "update.html", {'up': up})


def validateEmail( email ):

    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def sanitize(value):
	
    from bs4 import BeautifulSoup
    from django.core.exceptions import ValidationError

    VALID_TAGS = ['b','a','h1','h2','h3','h4','p','html','style','br']
    soup = BeautifulSoup(value, 'lxml')
	#try:
    for tag in soup.findAll(True):
    	if tag.name not in VALID_TAGS:
            tag.hidden = True
            return True

    return False 
		#return soup.renderContents()
			#return False;
				
	#except ValidationError:
		#return True

def user_exist(username, password):

    l = ldap.initialize('ldap://ldapserver')
    adminUser="uid=%s,ou=users,dc=mysite,dc=com"%username
    try:
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(username, password)
        valid = True
    except Exception as error:
        print(error)
