from django.conf.urls import url

from Accounts import views


__author__ = 'Pratick'

urlpatterns = [

    url(r'^login/', views.LoginView.as_view()),
    url(r'^register/', views.RegisterView.as_view()),
    url(r'(?P<pk>.*)/', views.UserView.as_view()),
]