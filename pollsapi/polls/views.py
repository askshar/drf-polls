from ast import Delete
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ChoiceSerializer, QuestionSerializer,
    QuestionDetailSerializer, VoteSerializer,
    QuestionResultPageSerializer)
from .models import Question, Choice

# Create your views here.


@api_view(['GET'])
def questions_view(request):

    questions = Question.objects.order_by('-pub_date')

    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def question_add(request):

    serializer = QuestionSerializer(data=request.data)

    if serializer.is_valid():
        question = serializer.save()

        return Response(QuestionSerializer(question).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail_view(request, id):

    question = get_object_or_404(Question, pk=id)

    if request.method == 'GET':
        serializer = QuestionDetailSerializer(question)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        question.delete()
        return Response("Question Deleted.", status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def add_choices(request, question_id):

    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        serializer = ChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def vote_view(request, question_id):

    question = get_object_or_404(Question, id=question_id)

    if request.method == 'PATCH':
        serializer = VoteSerializer(data=request.data)
        if serializer.is_valid():
            choice = get_object_or_404(Choice, pk=serializer.validated_data['choice_id'], question=question)
            choice.votes += 1
            choice.save()
            return Response("Voted!")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def question_result_view(request, question_id):

    question = get_object_or_404(Question, id=question_id)

    serializer = QuestionResultPageSerializer(question)
    return Response(serializer.data)