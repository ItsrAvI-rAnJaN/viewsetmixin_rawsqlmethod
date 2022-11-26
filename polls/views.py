from rest_framework import mixins, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from polls.models import Question, Choice
import logging
from polls.serializer import QuestionSerializer
from django.db import connection


class PollsAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if "id" not in kwargs:
            return self.list(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ChoiceAPI(APIView):
    def post(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO polls_choice(choice_text, votes, question_id) VALUES(%s, %s, %s)",
                               [request.data.get("choice_text"), request.data.get("votes"),
                                request.data.get("question")])
                cursor.execute("SELECT * FROM polls_choice WHERE question_id = %s", [request.data.get("question")])
                fields = [col[0] for col in cursor.description]
                created_data = [
                    dict(zip(fields, records))
                    for records in cursor.fetchall()
                ]
            return Response({"message": "choice created", "data": created_data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            choices = Choice.objects.raw("SELECT * FROM polls_choice where question_id = %s",
                                         [request.data.get("question")])
            fields = choices.columns
            retrieved_data = [
                dict(zip(fields, (record.id, record.choice_text, record.votes, record.question_id)))
                for record in choices
             ]
            return Response({"message": "Data retrieved", "data": retrieved_data}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE polls_choice SET choice_text = %s, votes = %s WHERE id = %s",
                               [request.data.get("choice_text"), request.data.get("votes"), request.data.get("id")])
                cursor.execute("SELECT * FROM polls_choice where id = %s", [request.data.get("id")])
                fields = [col[0] for col in cursor.description]
                updated_data = [dict(zip(fields, cursor.fetchone()))]
            return Response({"message": "Update successful", "data": updated_data},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM polls_choice WHERE id = %s", [request.data.get("id")])
            return Response({"message": "choice Deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)