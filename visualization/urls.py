from django.urls import path,include
from . import views

app_name='visualization'

urlpatterns=[
path('',views.index,name="analysis"),
]