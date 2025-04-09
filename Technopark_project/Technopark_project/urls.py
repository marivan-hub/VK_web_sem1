from django.contrib import admin
from django.urls import path
from QA_project.views import index, login, ask, signup, question, settings, index_logout, tag, hot
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'), # главная страница
    path('hot/', hot, name='hot'), # список лучших вопросов
    path('index_logout/', index_logout, name='index_logout'), # тестовая страничка для демонстрации (потом удалить)
    path('tag/<str:tag_name>/', tag, name='tag'), # список вопросов по тегу
    path('question/<int:pk>/', question, name='question'), # страница одного вопроса со список ответов
    path('settings/', settings, name='settings'), # страница настроек
    path('login/', login, name='login'), # форма логина
    path('signup/', signup, name='signup'), # форма регистрации
    path('ask/', ask, name='ask'), # форма создания вопроса

]

