from django.contrib import admin
from django.urls import path
from QA_project.views import (index, login_view, ask, signup, question, settings, tag, hot, logout_view, like_question,
                              like_answer, mark_correct_answer)
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', index, name='index'), # главная страница
    path('hot/', hot, name='hot'), # список лучших вопросов
    # path('index_logout/', index_logout, name='index_logout'), # тестовая страничка для демонстрации (потом удалить)
    path('tag/<str:tag_name>/', tag, name='tag'), # список вопросов по тегу
    path('question/<int:pk>/', question, name='question'), # страница одного вопроса со список ответов
    path('settings/', settings, name='settings'), # страница настроек
    path('login/', login_view, name='login'), # форма логина
    path('signup/', signup, name='signup'), # форма регистрации
    path('ask/', ask, name='ask'), # форма создания вопроса
    path('logout/', logout_view, name='logout'),
    path('like-question/', like_question, name='like-question'),
    path('like-answer/', like_answer, name='like-answer'),
    path('mark-correct/', mark_correct_answer, name='mark-correct'),

]

# Для медиа:
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)