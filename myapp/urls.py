from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.Dash_board, name='dash'),
    path('chat/', views.chat_view, name='chat'),
    path('upload_text/', views.uploads_text, name='uploads_text'),
    path('upload_file/', views.uploads_file, name='uploads_file'),
    path('task_planner/', views.task_planner, name='task_planner'),
    path('resolve_task_endpoint/<int:task_id>/', views.resolve_task_endpoint, name='resolve_task_endpoint'),
    path('notes/upload-file/', views.upload_note_file_view, name='upload_note_file'),
    path('notes/upload-text/', views.upload_note_text_view, name='upload_note_text'),
    path('notes/delete/<int:note_id>/', views.delete_note_view, name='delete_note'),
    path("notes/download/<int:note_id>/", views.download_note, name="download_note"),
    path("notes/share/<int:note_id>/", views.share_note, name="share_note"),
    path("notes/get/<int:note_id>/", views.get_note_data),
    path("notes/quiz/<int:note_id>/",views.generate_quiz,name="generate_quiz"),
    path("notes/flashcards/<int:note_id>/", views.generate_flashcard_view, name="generate_flashcards" ),
    path("notes/keyterms/<int:note_id>/", views.text_extractor_view, name="generate_text_extractor" ),
    path("notes/formulas/<int:note_id>/",views.formula_extractor_view,name="formula_extractor"),
    path("notes/exam/<int:note_id>/",views.exam_question_view,name="exam_questions"),
    path("notes/exam/evaluate/<int:note_id>/",views.exam_evaluate_view,name="exam_evaluate"),
]