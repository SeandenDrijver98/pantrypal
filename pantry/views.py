from rest_framework import viewsets

from pantry.models import FoodInventory
from pantry.serializers import FoodInventorySerializer


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = FoodInventory.objects.all()
    serializer_class = FoodInventorySerializer
