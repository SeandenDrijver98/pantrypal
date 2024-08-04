from rest_framework import serializers

from pantry.models import FoodInventory


class FoodInventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodInventory
        fields = "__all__"