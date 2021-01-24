from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from lms.role_permission import UserRole, MentorRole
from ..models import LmsUser, Question, Answer
from .question_answer_api_serializers import QuestionSerializer, AnswerSerializer


class SendQuery(GenericAPIView):

    """
        Send Query
    """

    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated & UserRole,)

    def get_serializer_class(self):
        return QuestionSerializer

    def post(self, request):

        """
            API to Send Query
        """

        response = {}
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            obj = serializer.save()
            if request.FILES:
                obj.document = request.FILES.get('document')
                obj.save()
            status_code = status.HTTP_201_CREATED
            response['message'] = 'Question posted successfully'
            response.update(self.serialize_response(obj))
            return Response(response, status=status_code)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def serialize_response(self, obj):

        """
            Serialize response
        """

        return {'question_text': obj.question_text}


class GetMyQuestions(GenericAPIView):

    """
        Retrieve question for specific mentor
    """

    permission_classes = (IsAuthenticated & MentorRole,)

    def get(self, request):

        """
            API to retrieve question
        """

        response = {}
        questions = list(Question.objects.filter(to_mentor__id=request.user_id).values())
        if questions:
            response['message'] = 'Questions retrieved successfully'
            response['data'] = questions
        else:
            response['message'] = 'No questions for you'
            response['data'] = questions
        return Response(response, status=status.HTTP_200_OK)


class AnswerViewSet(viewsets.ModelViewSet):

    """
        A viewset for viewing and editing answer.
        Save the answer posted from mentor
    """

    permission_classes = (IsAuthenticated & MentorRole,)
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = Answer.objects.filter(question__to_mentor__id=self.request.user_id)
        return queryset
