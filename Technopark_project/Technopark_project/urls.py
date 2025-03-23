from django.contrib import admin
from django.urls import path
from QA_project.views import index, login, ask, signup, question, settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login, name='login'),
    path('ask/', ask, name='ask'),
    path('signup/', signup, name='signup'),
    path('question/', question, name='question'),
    path('settings/', question, name='settings'),
]
