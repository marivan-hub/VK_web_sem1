from django.contrib import admin
from django.urls import path
from QA_project.views import index, login, ask, signup, question
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('login/', login, name='login'),
    path('ask/', ask, name='ask'),
    path('signup/', signup, name='signup'),
    path('question/', question, name='question'),
]
