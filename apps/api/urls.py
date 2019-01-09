from django.urls import path
from .views import CreatePerson

app_name = 'api'
urlpatterns = [
    # Person urls
    path('person', CreatePerson.as_view(), name='create_person'),
]