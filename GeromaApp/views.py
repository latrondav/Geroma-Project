from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from GeromaApp.forms import ProfileForm
from GeromaProject import settings
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . token import generate_token
from django.core.mail import EmailMessage, send_mail
from decimal import Decimal
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, F, Count

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

def blog(request):
    # Query to retrieve a list of blogs with the number of comments annotated
    blog_list = Blog.objects.annotate(num_comments=Count('comments'))

    # Pagination
    paginator = Paginator(blog_list, 5)  # Show 5 blogs per page
    page = request.GET.get('page')
    
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver the last page of results.
        blogs = paginator.page(paginator.num_pages)

    # Query to retrieve categories with the number of blogs per category
    categories = Blog.objects.values('blog_category').annotate(count=Count('blog_category'))

    context = {
        'Blogs': blogs,  # Change this variable name to 'blogs'
        'Categories': categories
    }
    return render(request, 'blog.html', context)

def blogdetail(request, bid):
    blogdetails = get_object_or_404(Blog, id=bid)
    blog_comments = BlogComment.objects.filter(comment_blog=blogdetails)
    comment_count = blog_comments.count()

    # Query to retrieve categories with the number of blogs per category
    categories = Blog.objects.values('blog_category').annotate(count=Count('blog_category'))

    context = {
        'BlogDetails': blogdetails,
        'blog_comments': blog_comments,
        'comment_count': comment_count,
        'Categories': categories
    }
    return render(request, 'blogdetail.html', context)

def postblog(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            blog_image = request.FILES.get('blog_image')
            blog_title = request.POST.get('blog_title')
            blog_category = request.POST.get('blog_category')
            blog_body_introduction = request.POST.get('blog_body_introduction')
            blog_body_main = request.POST.get('blog_body_main')
            blog_body_conclusion = request.POST.get('blog_body_conclusion')

            if all([blog_image, blog_title, blog_category, blog_body_introduction, blog_body_main, blog_body_conclusion]):
                PB = Blog(
                    blog_image=blog_image,
                    blog_title=blog_title,
                    blog_author=request.user,
                    blog_category=blog_category,
                    blog_body_introduction=blog_body_introduction,
                    blog_body_main=blog_body_main,
                    blog_body_conclusion=blog_body_conclusion
                )
                PB.save()
                messages.success(request, "Blog Posted Successfully")
                return redirect('/blog/')
            else:
                messages.error(request, 'Failed To Post Blog, Please Fill in All Required Fields.')
                return redirect('/blog/')
        else:
            messages.error(request, 'Failed To Post Blog, Please Try Again Later.')
            return redirect('/blog/')
    else:
        return redirect('/')

def submitblogcomment(request, bid):
    if request.method == 'POST':
        comment_author = request.POST.get('comment_author')
        comment_email = request.POST.get('comment_email')
        comment_body = request.POST.get('comment_body')
        
        # Retrieve the blog from the database or return 404 if it doesn't exist
        blog = get_object_or_404(Blog, id=bid)

        if all([comment_author, comment_email, comment_body]):
            BC = BlogComment(
                comment_author=comment_author,
                comment_email=comment_email,
                comment_body=comment_body,
                comment_blog=blog
            )
            BC.save()
            messages.success(request, "Blog Comment Posted Successfully")
        else:
            messages.error(request, 'Failed To Post Blog Comment, Please Fill in All Required Fields.')
    else:
        messages.error(request, 'Failed To Post Blog Comment, Please Try Again Later.')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Use the named URL pattern for blog list

def blogsearch(request):
    query = request.POST.get('blogsearch') if request.method == 'POST' else None

    if query:
        # Search and filter the blogs
        Blogs = Blog.objects.filter(
            Q(blog_title__icontains=query) |
            Q(blog_category__icontains=query) |
            Q(blog_author__first_name__icontains=query) |
            Q(blog_author__last_name__icontains=query)
        )
    else:
        # If no query, retrieve all blogs
        Blogs = Blog.objects.all()

    # Adding the count of comments for each blog
    for blog in Blogs:
        blog.num_comments = BlogComment.objects.filter(comment_blog=blog).count()

    paginator = Paginator(Blogs, 5)
    page = request.GET.get('page')
    Blogs = paginator.get_page(page)
    
    categories = Blog.objects.values('blog_category').annotate(count=Count('blog_category'))

    context = {
        'Blogs': Blogs,
        'Query': query,
        'Categories': categories
    }

    return render(request, 'blog.html', context)

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

def services(request):
    return render(request, 'services.html')

def team(request):
    userId = request.user.id
    Your_Orders = Orders.objects.filter(user_id = userId)
    if Your_Orders:
        context={
            'Your_Orders':Your_Orders
        }
        return render(request, 'team.html', context)
    else:
        context={
            'error':f'You have no orders yet, please browse through features and place an order, thank you.'
        }

    return render(request, 'team.html', context)

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

def hscodesguide(request):
    # Get all HSCodes objects
    hscodes = HSCodes.objects.all()

    # # Configure the number of items per page
    # items_per_page = 1000

    # # Initialize the Paginator with the HSCodes queryset and items per page
    # paginator = Paginator(hscodes, items_per_page)

    # # Get the current page number from the request's GET parameters
    # page_number = request.GET.get('page')

    # # Get the Page object for the current page number
    # hscodes_page = paginator.get_page(page_number)

    context = {
        'hscodes': hscodes  # Pass the paginated HSCodes Page object to the template
    }

    return render(request, 'hscodeguide.html', context)

def requesttaxrate(request):
    MVVGuideDetails = MotorVehicleValueGuide.objects.all()
    context = {
        'MVVGuideDetails': MVVGuideDetails
    }
    return render(request, 'requesttaxrate.html', context)

def calculategeneralgoodstaxes(request):
    if request.method == 'POST':
        cif = Decimal(request.POST.get('cifvalue'))
        currency = request.POST.get('currency')
        hscode = request.POST.get('hscode')
        unit_of_measure = request.POST.get('unitofmeasure')
        gross_unit = Decimal(request.POST.get('grossunit'))
        goods_description = request.POST.get('goodsdescription')

        if currency != 'UGX':
            exchange_rate = (Decimal(3754.27)).quantize(Decimal('0.00'))
            converted_cif = (cif * exchange_rate).quantize(Decimal('0.00'))
        else:
            exchange_rate = (Decimal(1)).quantize(Decimal('0.00'))
            converted_cif = (cif).quantize(Decimal('0.00'))
        
        hscodedetails = HSCodes.objects.get(hs_code=hscode)
        if hscodedetails:
            import_duty = (converted_cif * Decimal(hscodedetails.rate)).quantize(Decimal('0.00'))
            HSCodeDescription = hscodedetails.description
        else:
            messages.error(request, "Invalid Or Wrong HSCode Submitted")
            return render(request, 'requesttaxrate.html')
        
        vat = ((converted_cif + import_duty) * Decimal('0.18')).quantize(Decimal('0.00'))
        withholding_tax = (converted_cif * Decimal('0.06')).quantize(Decimal('0.00'))
        infrastructure_levy = (converted_cif * Decimal('0.015')).quantize(Decimal('0.00'))

        total_tax = (import_duty + vat + withholding_tax + infrastructure_levy).quantize(Decimal('0.00'))

        Category = 'General Goods'

        # Save the tax breakdown to the database
        tax_calculation = TaxCalculation.objects.create(
            cif=(cif).quantize(Decimal('0.00')),
            currency=currency,
            exchange_rate=exchange_rate,
            hscode=hscode,
            hscode_description=HSCodeDescription,
            unit_of_measure=unit_of_measure,
            measurement=gross_unit,
            goods_description=goods_description,
            converted_cif=converted_cif,
            import_duty=import_duty,
            vat=vat,
            withholding_tax=withholding_tax,
            infrastructure_levy=infrastructure_levy,
            total_tax=total_tax,
            category=Category
        )

        # Render the HTML template with the success flag
        return render(request, 'requesttaxrate.html', {'success': True, 'tax_calculation': tax_calculation})
    else:
        return render(request, 'requesttaxrate.html', {'failed': True, 'message': 'Failed To Calculate Taxes, Contact Geroma Admin For Assistance.'})  # Render the HTML template for initial page load

def calculatemotorvehicletaxes(request):
    if request.method == 'POST':
        mv_description = request.POST.get('MVDescriptions')
        hscode = request.POST.get('mvhscode')
        cif = Decimal(request.POST.get('mvcifvalue'))
        currency = request.POST.get('mvcurrency')
        engine_capacity = request.POST.get('enginecapacity')
        year_of_manufacture = request.POST.get('yom')
        country_of_origin = request.POST.get('mvcoc')
        vehicle_type = request.POST.get('vehicletype')
        seating_capacity = request.POST.get('seatingcapacity')
        gross_weight = Decimal(request.POST.get('grossweight'))

        if currency != 'UGX':
            exchange_rate = (Decimal(3754.27)).quantize(Decimal('0.00'))
            converted_cif = (cif * exchange_rate).quantize(Decimal('0.00'))
        else:
            exchange_rate = (Decimal(1)).quantize(Decimal('0.00'))
            converted_cif = (cif).quantize(Decimal('0.00'))

        hscodedetails = HSCodes.objects.get(hs_code=hscode)
        if hscodedetails:
            import_duty = (converted_cif * Decimal(hscodedetails.rate)).quantize(Decimal('0.00'))
            HSCodeDescription = hscodedetails.description
        else:
            messages.error(request, "Invalid Or Wrong HSCode Submitted")
            return render(request, 'requesttaxrate.html')

        vat = ((converted_cif + import_duty) * Decimal('0.18')).quantize(Decimal('0.00'))
        withholding_tax = (converted_cif * Decimal('0.06')).quantize(Decimal('0.00'))

        year_today = datetime.now().year
        if year_of_manufacture and (year_today - int(year_of_manufacture)) > 8:
            environmental_levy = (converted_cif * Decimal('0.5')).quantize(Decimal('0.00'))
        else:
            environmental_levy = (converted_cif * Decimal('0')).quantize(Decimal('0.00'))

        registration_fees = (Decimal('1500000')).quantize(Decimal('0.00'))
        stamp_duty = (Decimal('15000')).quantize(Decimal('0.00'))
        form_fees = (Decimal('35000')).quantize(Decimal('0.00'))

        total_tax = (import_duty + vat + withholding_tax + environmental_levy + registration_fees + stamp_duty + form_fees).quantize(Decimal('0.00'))

        Category = 'Motor Vehicle'
        unitofmeasure = 'Kgs'

        # Save the tax breakdown to the database
        tax_calculation = TaxCalculation.objects.create(
            cif=cif,
            currency=currency,
            exchange_rate=exchange_rate,
            converted_cif=converted_cif,
            hscode=hscode,
            hscode_description=HSCodeDescription,
            vehicle_type=vehicle_type,
            year_of_manufacture=year_of_manufacture,
            seating_capacity=seating_capacity,
            unit_of_measure=unitofmeasure,
            measurement=gross_weight,
            engine_capacity=engine_capacity,
            goods_description=mv_description,
            country_of_origin=country_of_origin,
            import_duty=import_duty,
            vat=vat,
            withholding_tax=withholding_tax,
            total_tax=total_tax,
            environmental_levy=environmental_levy,
            registration_fees=registration_fees,
            stamp_duty=stamp_duty,
            form_fees=form_fees,
            category=Category
        )

        # Render the HTML template with the success flag
        return render(request, 'requesttaxrate.html', {'success': True, 'tax_calculation': tax_calculation})
    else:
        return render(request, 'requesttaxrate.html', {'failed': True, 'message': 'Failed To Calculate Taxes, Contact Geroma Admin For Assistance.'})

  # Add this decorator for CSRF protection

def get_selected_vehicle_details(request, mvvgid):
    if request.method == 'GET':
        if mvvgid:
            try:
                # Retrieve the vehicle details based on the selected description
                vehicle = MotorVehicleValueGuide.objects.get(id=mvvgid)
                vehicle_details = {
                    'hscode': vehicle.HSCode,
                    'CountryOfOrigin': vehicle.CountryOfOrigin,
                    'yom': vehicle.YearOfManufacture,
                    'enginecapacity': vehicle.Engine,
                    'cifvalue': vehicle.CIF,
                }
                return JsonResponse(vehicle_details)
            except MotorVehicleValueGuide.DoesNotExist:
                return JsonResponse({'error': 'Vehicle not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
