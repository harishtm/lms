from rest_framework import serializers
from django.conf import settings
from django.core import exceptions
from ..models import LmsUser, Question, Answer
from .register_api_serializers import LmsUserSerializer


def required(value):
    if value is None:
        raise serializers.ValidationError('This field is required')


class QuestionSerializer(serializers.ModelSerializer):

    from_user = serializers.CharField(validators=[required], source='from_user.email')

    to_mentor = serializers.CharField(validators=[required], source='to_mentor.email')

    class Meta:
        model = Question
        fields = ('from_user', 'to_mentor', 'question_text')

    def to_representation(self, instance):
        rep = super(QuestionSerializer, self).to_representation(instance)
        rep['from_user'] = instance.from_user.email
        rep['to_mentor'] = instance.to_mentor.email
        return rep

    def validate(self, data):
        from_user = data['from_user']['email']
        to_mentor = data['to_mentor']['email']
        if Question.objects.filter(question_text__iexact=data['question_text']).exists():
            raise serializers.ValidationError('Question already exists')
        if not LmsUser.objects.filter(email__iexact=from_user, role='1').exists():
            raise serializers.ValidationError('Invalid user')
        if not LmsUser.objects.filter(email__iexact=to_mentor, role='2').exists():
            raise serializers.ValidationError('Invalid Mentor')
        return data

    def create(self, validated_data):
        from_user = LmsUser.objects.get(email__iexact=validated_data['from_user']['email'])
        to_mentor = LmsUser.objects.get(email__iexact=validated_data['to_mentor']['email'])
        obj = Question(from_user=from_user,
                       to_mentor=to_mentor,
                       question_text=validated_data['question_text'])
        obj.save()
        return obj


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

    def validate(self, data):
        request = self.context.get("request")
        user_id = request.user_id
        answer_queryset = Answer.objects.filter(question=data['question'],
                                                question__to_mentor=user_id)
        if self.instance:
            answer_queryset = answer_queryset.exclude(id=self.instance.id)
        if answer_queryset.exists():
            raise serializers.ValidationError('Already answered the question please update the answer')
        return data
