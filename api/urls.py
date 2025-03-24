from django.urls import path
from .views import HelloWorld
from .views import Students
from .views import ContactListView
from .views import ContactUpdateDetailView

urlpatterns = [
 path('hello/', HelloWorld.as_view(), name='hello_world'),
 path('students/', Students.as_view(), name='student_list'),
 path('contact/', ContactListView.as_view(), name='contact_new'),
 path('contact/<int:contact_id>/', ContactListView.as_view(), name='contact_detail'),
 path('contacts/', ContactListView.as_view(), name='contact_list'),
 path('contacts/<int:contact_id>/', ContactUpdateDetailView.as_view(), name='contact_update_detail'),
 
]

