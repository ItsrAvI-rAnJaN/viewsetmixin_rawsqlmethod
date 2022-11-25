from rest_framework import serializers
from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    """
    Creates a new `Note`
    """

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'pub_date']
