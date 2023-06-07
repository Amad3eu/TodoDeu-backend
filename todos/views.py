from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TodoSerializer
from .models import Todo
from django.core.mail import send_mail

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()  # Obtém a instância da tarefa antes da atualização

        super().perform_update(serializer)

        if not instance.completed and serializer.instance.completed:
            subject = 'Tarefa Concluída'
            message = f'A tarefa "{serializer.instance.name}" foi concluída.\nDescrição: {serializer.instance.description}'
            from_email = 'amadeu@aupi.com'
            recipient_list = ['alexandre@aupi.com.br']

            send_mail(subject, message, from_email, recipient_list)