from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone

from api.models.policy import Policy
from api.serializers.policy_serializer import PolicySerializer
from api.usecases.create_policy import create_policy_logic

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

    def perform_create(self, serializer):
        data = serializer.validated_data
        created_policy = create_policy_logic(data)
        
        serializer.instance = created_policy
        serializer.save()

    def perform_update(self, serializer):
        expiry_date = serializer.validated_data.get('expiry_date')
        if expiry_date and expiry_date < timezone.now().date():
            raise ValidationError({"expiry_date": "A expiry date deve ser no futuro!"})
        serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except ValidationError as e:
            return JsonResponse(e.detail if hasattr(e, 'detail') else str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except ValidationError as e:
            return JsonResponse(e.detail if hasattr(e, 'detail') else str(e), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)
