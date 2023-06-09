from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TodoSerializer
from .models import Todo

class TodoViewSet(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()  # Obtém a instância da tarefa antes da atualização

        super().perform_update(serializer)

        if instance.completed != serializer.instance.completed and serializer.instance.completed:
            subject = 'Tarefa Concluída'
            message = f'A tarefa "{serializer.instance.name}" foi concluída.\nDescrição: {serializer.instance.description}'
            from_email = 'amadeu@aupi.com'
            recipient_list = ['alexandre@aupi.com.br']

            send_mail(subject, message, from_email, recipient_list)

    @action(detail=False, methods=['post'])
    def bulk_list(self, request):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_bulk_create(serializer)
        return Response(serializer.data)

    def perform_bulk_create(self, serializer):
        instances = []
        for obj in serializer.validated_data:
            instance = self.get_queryset().create(**obj)
            instances.append(instance)
        self.send_bulk_list_email(instances)

    def send_bulk_list_email(self, instances):
        subject = 'Tarefas Adicionadas'
        message = 'As seguintes tarefas foram adicionadas:\n'
        for instance in instances:
            message += f'Nome: {instance.name}\nDescrição: {instance.description}\n\n'
        from_email = 'amadeu@aupi.com'
        recipient_list = ['alexandre@aupi.com.br']

        send_mail(subject, message, from_email, recipient_list)
