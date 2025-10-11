from django.contrib.auth.models import User
from rest_framework import serializers

from pantry.models import FoodInventory, Recipe, Chef, Tag, UserSave, MealPlan, ShoppingList, ShoppingListLine


class FoodInventorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodInventory
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ChefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chef
        fields = ['id', 'name', 'avatar', 'specialty', 'verified', 'followers', 'recipes_count', 'rating']


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    chef = ChefSerializer(read_only=True)
    
    class Meta:
        model = Recipe
        fields = [
            'id', 'name', 'description', 'directions', 'calories', 'protein',
            'prep_time', 'cook_time', 'servings', 'difficulty', 'image',
            'rating', 'likes', 'tags', 'chef', 'created_at'
        ]


class UserSaveSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    
    class Meta:
        model = UserSave
        fields = ['id', 'recipe', 'saved_at']


class MealPlanSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    
    class Meta:
        model = MealPlan
        fields = ['id', 'recipe', 'planned_date', 'meal_type', 'created_at']

class ShoppingListLineSerializer(serializers.ModelSerializer):

    food = serializers.CharField(source='food.name')

    class Meta:
        model = ShoppingListLine
        fields = ['id', 'food', 'quantity', 'quantity_uom']

class ShoppingListSerializer(serializers.ModelSerializer):

    lines = ShoppingListLineSerializer(many=True, read_only=True)
    class Meta:
        model = ShoppingList
        fields = ['id','created_at', 'lines']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}


class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    chef_name = serializers.CharField(required=False)
    chef_specialty = serializers.CharField(required=False)
    chef_avatar = serializers.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'chef_name', 'chef_specialty', 'chef_avatar']

    def create(self, validated_data):
        chef_name = validated_data.pop('chef_name',
                                       None) or f"{validated_data.get('first_name', '')} {validated_data.get('last_name', '')}".strip()
        chef_specialty = validated_data.pop('chef_specialty', '')
        chef_avatar = validated_data.pop('chef_avatar', None)

        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # Create associated chef profile
        Chef.objects.create(
            user=user,
            name=chef_name,
            specialty=chef_specialty,
            avatar=chef_avatar
        )

        return user
