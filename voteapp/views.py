from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views import generic
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from . import models
from . import serializers


# class Index(generic.View):
#     def get(self, request):
#         polls = list(models.Poll.objects.all().values('question', 'poll_owner__username', 'date_created'))
#         result = {
#             'result': polls
#         }
#         return JsonResponse(result)


# class Index(generic.View):
#     def get(self, request):
#         polls = models.Poll.objects.all()
#         pollz = serializers.PollSerializer(polls, many=True)
#         data = {
#             'result': pollz.data
#         }
#         return JsonResponse(data) # JsonResponse expects a dict always, no list allowed


class Index(APIView):
    def get(self, request):
        polls = models.Poll.objects.all()
        poll_data = serializers.PollSerializer(polls, many=True).data
        return Response(poll_data)

class PollDetail(generic.View):
    def get(self, request, poll_id):
        poll = models.Poll.objects.get(pk=poll_id)
        result = {
            'result': {
                'question': poll.question,
                'poll_owner__username': poll.poll_owner.username,
                'date_created': poll.date_created,
                'choices': list(poll.choices.all().values('text', 'poll__question'))
            }
        }
        return JsonResponse(result)