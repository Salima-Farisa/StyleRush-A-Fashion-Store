from django.urls import path
from .views import login_page, signup_page, logout_page, forgotpassword_page

urlpatterns = [
    path('', login_page, name="login"),
    path('signup', signup_page, name="signup"),
    path('logout/', logout_page, name='logout'),
    path('forgotpassword/', forgotpassword_page, name='forgotpassword')
]