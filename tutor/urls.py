from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.register_api import RegisterUser
from .api.question_answer_api import SendQuery, GetMyQuestions, AnswerViewSet


urlpatterns = [
    path(r'api/register/', RegisterUser.as_view()),
    path(r'api/send_query/', SendQuery.as_view()),
    path(r'api/get_my_questions/', GetMyQuestions.as_view()),
]


router = DefaultRouter()
router.register(r'api/answer', AnswerViewSet, basename='mentor_answer')


urlpatterns += router.urls

# {"email": "test@gmail.com", "password": "tesT@123"}
# {"email": "mentor1@gmail.com", "password": "Test@123"}
