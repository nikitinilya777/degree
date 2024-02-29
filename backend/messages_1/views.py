from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import *
from RSA import e, d, n, encrypted, decrypted


class KeysView(APIView):
    def get(self, request, *args, **kwargs):

        data = {
            'e': str(e),
            'n': str(n),
        }
        return Response(data, status=status.HTTP_200_OK)


class MessagesListView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        e1 = int(data['e'])
        n1 = int(data['n'])

        data = {'massages': list()}
        messages_all = Message.objects.all()
        for message in messages_all:
            data['massages'].append({
                'id': encrypted(str(message.id), e1, n1),
                'message': encrypted(str(message.message), e1, n1),
                'date': encrypted(str(message.date), e1, n1)
            })
        return Response(data, status=status.HTTP_201_CREATED)


class MessageCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        message_enc = list()
        for block in data['message']:
            message_enc.append(int(block))
        Message.objects.create(message=decrypted(message_enc))
        return Response(data, status=status.HTTP_201_CREATED)
