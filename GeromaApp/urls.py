from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home),
    path('login/', views.homelogin),
    path('register/', views.homeregister),
    path('profile/', views.profileview),
    path('updateprofile/', views.updateprofile),
    path('signout/', views.signout),
    path('activate/<uidb64>/<token>/', views.activate, name= "activate"),
    path('aboutus/', views.aboutus),
    path('alumnicarbinet/', views.alumnicarbinet),
    path('blog/', views.blog),
    path('blogdetail/<bid>/', views.blogdetail),
    path('postblog/', views.postblog),
    path('blogcomment/<bid>/', views.submitblogcomment),
    path('blogsearch/', views.blogsearch),
    path('contact/', views.contact),
    path('services/', views.services),
    path('team/', views.team),
    path('submitorder/', views.submit_orders),
    path('vieworders/', views.view_orders),
    path('submitorderstatus/', views.submit_orders_status),
    path('history/', views.history),
    path('hscodesguide/', views.hscodesguide),
    path('requesttaxrate/', views.requesttaxrate),
    path('calcggt/', views.calculategeneralgoodstaxes),
    path('calcmvt/', views.calculatemotorvehicletaxes),
    path('getselectedvehicledetails/<mvvgid>/', views.get_selected_vehicle_details),

    #reset password path
    path('resetpasswordform/', auth_views.PasswordResetView.as_view(template_name="passwordmgt/pw_reset_form.html"), name= "password_reset_form"),
    path('resetpassworddone/', auth_views.PasswordResetDoneView.as_view(template_name="passwordmgt/pw_reset_done.html"), name= "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="passwordmgt/pw_reset_confirm.html"), name= "password_reset_confirm"),
    path('resetpasswordcomplete/', auth_views.PasswordResetCompleteView.as_view(template_name="passwordmgt/pw_reset_complete.html"), name= "password_reset_complete"),

    #change password path
    path('changepasswordform/', auth_views.PasswordChangeView.as_view(template_name="passwordmgt/pw_change_form.html"), name="password_change_form"),
    path('changepassworddone/', auth_views.PasswordChangeDoneView.as_view(template_name="passwordmgt/pw_change_done.html"), name="password_change_done"),
]