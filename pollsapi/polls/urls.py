from django.urls import path

from . import views


urlpatterns = [
    path('questions/', views.questions_view, name='questions'),
    path('questions/<int:id>/', views.question_detail_view, name='question-detail'),
    path('questions/add/', views.question_add, name='add-question'),
    path('questions/<int:question_id>/choices/', views.add_choices, name='add-choices'),
    path('questions/<int:question_id>/votes/', views.vote_view, name='add-votes'),
    path('questions/<int:question_id>/result/', views.question_result_view, name='question-result'),
]
