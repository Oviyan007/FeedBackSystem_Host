
from django.contrib import admin
from django.urls import include, path
from Home import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.Home,name='Home'),
    # path("login/",views.Login,name='Login'),
    path("login/",auth_views.LoginView.as_view(template_name='home/login.html'),name='Login'),
    path("logout/",auth_views.LogoutView.as_view(template_name='home/logout.html'),name='Logout'),
    path("register/",views.Register,name='Register'),
    path("profile/",views.profile,name='Profile'),
    path("FeedBack",views.feedback_view,name='FeedBack'),
    # path("GetReview",views.Review_feedback,name='GetReview'),
    #report generating 
    path('Report',views.feedback_report_view,name='Report'),
    # path('test',views.test,name='test')
   
]
