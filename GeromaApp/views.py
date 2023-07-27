from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from GeromaApp.forms import ProfileForm
from GeromaProject import settings
from .models import Alumni_Carbinets, Contacts, Profile, Events, Orders
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . token import generate_token
from django.core.mail import EmailMessage, send_mail


# Create your views here.

def home(request):
    return render(request, 'home.html')

def homelogin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        try:
            remember = request.POST['remember-me']
            if remember:
                settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        except:
            is_private = False
            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True

        if user is not None:
            login(request, user)
            messages.success(request, "LOGGED IN SUCCESSFULLY!")
        else:
            messages.error(request, "BAD CREDENTIALS")
            return redirect('/')

    return render(request, 'home.html')

def profileview(request):
    context = {
        'user' : request.user,
        'Profile' : request.Profile
    }
    return render(request, 'profilemodal.html', 'includes/header.html', context)

def homeregister(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Student number already exist! Please use your student number, thank you.")
            return redirect('/')

        if len(username)>10:
            messages.error(request, "Student number must only be under 10 characters")
            return redirect('/')

        if not username.isnumeric():
            messages.error(request, "Student number must only be Numeric!")
            return redirect('/')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match")
            return redirect('/')

        user = User.objects.create_user(username, email, pass1)
        user.first_name = firstname.upper()
        user.last_name = lastname.upper()
        user.is_active = False
        user.save()

        # Email Address Confirmation Email

        current_site = get_current_site(request)
        email_subject = "SICA WELCOME AND ACCOUNT CONFIRMATION"
        message = render_to_string('email_confirmation.html', {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)
        })
        email = EmailMessage(
            email_subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
        )
        email.fail_silently = True
        email.send()
        messages.info(request, "SICA ACCOUNT CREATED, NOW TO LOGIN, PLEASE CHECK YOUR EMAIL TO ACTIVATE ACCOUNT.")
        return redirect('/')

    return render(request, 'home.html')

def updateprofile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "YOUR SICA ACCOUNT PROFILE HAS BEEN UPDATED SUCCESSFULLY")
            return redirect('/')
        else:
            messages.error(request, "SORRY, SICA ACCOUNT UPDATE FAILED, TRY AGAIN LATERf")
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, "home.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "SICA ACCOUNT HAS BEEN SUCCESSFULLY ACTIVATED, PLEASE LOGIN, THANK YOU.")
        return render(request, 'home.html')
    else:
        messages.info(request, "ACTIVATION FAILED, PLEASE TRY AGAIN!")
        return redirect('/')

def signout(request):
    logout(request)
    messages.success(request, "LOGGED OUT SUCCESSFULLY!")
    return redirect('/')

def aboutus(request):
    return render(request, 'aboutus.html')

def alumnicarbinet(request):
    Alumnus= Alumni_Carbinets.objects.all()

    context = {
        'Alumnus':Alumnus
    }

    return render(request, 'alumnicarbinet.html', context)

def carbinet(request):
    return render(request, 'carbinet.html')

def contact(request):
    if request.method == 'POST':
        contact_name = request.POST['contact_name']
        contact_email = request.POST['contact_email']
        contact_subject = request.POST['contact_subject']
        contact_message = request.POST['contact_message']

        new_message = Contacts(contact_name = contact_name, contact_email = contact_email, contact_subjectt = contact_subject, contact_message = contact_message)
        new_message.save()
        messages.success(request, "MESSAGE SENT, THANK YOU FOR CONTACTING PANDA")

    return render(request, 'contact.html')

def events(request):
    return render(request, 'events.html')

def features(request):
    userId = request.user.id
    Your_Orders = Orders.objects.filter(user_id = userId)
    if Your_Orders:
        context={
            'Your_Orders':Your_Orders
        }
        return render(request, 'features.html', context)
    else:
        context={
            'error':f'You have no orders yet, please browse through features and place an order, thank you.'
        }

    return render(request, 'features.html', context)

def submit_orders(request):
    if request.method == "POST":
        user_id = request.user.id
        order_name = request.user.first_name
        order_course = request.user.profile.course
        order_yos = request.user.profile.yos
        order_email = request.user.email
        order_contact = request.user.profile.contact
        order_exec_shirt = request.POST['order_exec_shirt']
        order_tshirt = request.POST['order_tshirt']
        order_sicaid = request.POST['order_sicaid']

        new_order = Orders(user_id = user_id, order_name = order_name, order_course = order_course, order_yos = order_yos, order_email = order_email, order_contact = order_contact, order_exec_shirt = order_exec_shirt, order_tshirt = order_tshirt, order_sicaid = order_sicaid)
        new_order.save()
        messages.success(request, 'YOUR ORDER HAS BEEN SUBMITTED SUCCESSFULLY, WE SHALL REACH OUT TO CONFIRM ORDER, THANK YOU.')
        return redirect('/features/')
    else:
        messages.error(request, 'FAILED TO SUBMIT ORDER, PLEASE REACH OUT TO ADMIN FOR MORE ASSISSTANCE, THANK YOU.')
        return redirect('/features/')

def view_orders(request):
    View_Orders = Orders.objects.all()
    
    context = {
        'View_Orders':View_Orders
    }
    
    return render(request, 'view_orders.html', context)

def submit_orders_status(request):
    if request.method == "POST":
        order_id = request.POST['order_id']
        order_status = request.POST['order_status']

        Orders.objects.filter(id = order_id).update(order_status = order_status)
        messages.success(request, 'ORDER STATUS HAS BEEN UPDATED SUCCESSFULLY, THANK YOU.')
        return redirect('/vieworders/')
    else:
        messages.success(request, 'ORDER STATUS HAS UPDATE FAILED, TRY AGAIN LATER OR CONTACT ADMIN FOR MORE ASSISTANCE, THANK YOU.')
        return redirect('/vieworders/')
    
    #return render(request, 'view_orders.html', context)

def history(request):
    return render(request, 'history.html')

def projects(request):
    return render(request, 'projects.html')

def softwarehub(request):
    return render(request, 'softwarehub.html')

