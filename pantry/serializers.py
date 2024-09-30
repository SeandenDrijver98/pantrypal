from rest_framework import serializers

from pantry.models import FoodInventory, Food, User, Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class FoodInventorySerializer(serializers.ModelSerializer):
    user = UserSerializer
    food = serializers.SerializerMethodField

    class Meta:
        model = FoodInventory
        fields = "__all__"

    def get_food(self, obj):
        return obj.food.name

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"
