from django.urls import path
from .views import *


urlpatterns = [
    path('word_list/', WordListAPIView.as_view()),
    path('word_create/', CreateWordAPIView.as_view()),
    path('word_update/<int:pk>/', UpdateWordAPIView.as_view()),
    path('word_detail/<int:pk>/', WordDetailAPIView.as_view()),
    path('word_delete/<int:pk>/', DeleteWordAPIView.as_view()),


]