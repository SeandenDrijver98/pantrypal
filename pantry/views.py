import random

from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from pantry.models import FoodInventory, Recipe, Ingredient, Chef, ShoppingList
from pantry.serializers import FoodInventorySerializer, RecipeSerializer, ChefSerializer, ShoppingListSerializer, \
    UserSignupSerializer


class SignupView(APIView):
    """
    Creates a new user and chef profile.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = FoodInventory.objects.all()
    serializer_class = FoodInventorySerializer

    def get_queryset(self):
        return FoodInventory.objects.filter(user=self.request.user)


class NeededIngredientsView(APIView):
    permission_classes = [IsAuthenticated]
    """ Returns the ingredients needed to create the supplied list of recipes """
    def post(self, request):
        recipes_to_create = Recipe.objects.filter(id__in=request.data["recipe_ids"])
        ingredients_to_create = Ingredient.objects.filter(recipe__in=recipes_to_create).values("food__name", "quantity", "quantity_uom")

        # missing_ingredients = []
        #
        # for ingredient in ingredients_to_create:
        #     food_inventory = FoodInventory.objects.filter(food__name=ingredient["food__name"])
        #     if not food_inventory.exists():
        #         missing_ingredients.append(ingredient)
        #     else:
        #         food_inventory = food_inventory.first()
        #         if food_inventory.quantity < ingredient["quantity"]:
        #             missing_ingredients.append({"food": ingredient["food__name"], "quantity":ingredient["quantity"] - food_inventory.quantity, "quantity_uom":ingredient["quantity_uom"]})
        # TODO if An ingredient is listed as needed twice in the response, combine the quantities



        return Response({"uses": ingredients_to_create})


class CreatableRecipes(APIView):
    permission_classes = [IsAuthenticated]

    """ Returns the recipes that can be created with the current inventory """
    def get(self, request):
        food_inventory = FoodInventory.objects.filter(user=request.user)
        recipes = Recipe.objects.all()

        creatable_recipes = []
        missing_ingredient_threshold = 2

        for recipe in recipes:
            ingredients = Ingredient.objects.filter(recipe=recipe)
            missing_ingredients = 0

            for ingredient in ingredients:
                food_inventory = food_inventory.filter(food=ingredient.food)
                if not food_inventory.exists() or food_inventory.first().quantity < ingredient.quantity:
                    missing_ingredients += 1

            if missing_ingredients <= missing_ingredient_threshold:
                creatable_recipes.append(recipe)

        return Response(creatable_recipes)


class ExploreDataView(APIView):
    """Returns all the data needed for the 'explore recipes' page"""
    
    def get(self, request):
        # Get 2 random floating recipe cards
        random_recipes = list(Recipe.objects.all())
        if len(random_recipes) >= 2:
            floating_recipes = random.sample(random_recipes, 2)
        else:
            floating_recipes = random_recipes
        
        # Get top 5 most popular recipes (by user saves and meal plan adds)
        # Calculate popularity score based on saves and meal plan additions
        recipes_with_popularity = Recipe.objects.annotate(
            save_count=Count('usersave'),
            mealplan_count=Count('mealplan'),
            total_popularity=Count('usersave') + Count('mealplan')
        ).order_by('-total_popularity', '-likes')[:5]
        
        # Get 5 recipes tagged as quick and easy (prep + cook time <= 30 min)
        quick_easy_recipes = Recipe.objects.filter(
            Q(prep_time__lte=15) & Q(cook_time__lte=15)
        ).order_by('prep_time', 'cook_time')[:5]
        
        # Get 5 recipes tagged as vegetarian
        vegetarian_recipes = Recipe.objects.filter(
            tags__name__icontains='vegetarian'
        ).distinct()[:5]
        
        # Get 10 recipes for browse a section (excluding already selected ones)
        selected_recipe_ids = set()
        selected_recipe_ids.update([r.id for r in floating_recipes])
        selected_recipe_ids.update([r.id for r in recipes_with_popularity])
        selected_recipe_ids.update([r.id for r in quick_easy_recipes])
        selected_recipe_ids.update([r.id for r in vegetarian_recipes])
        
        browse_recipes = Recipe.objects.exclude(
            id__in=selected_recipe_ids
        ).order_by('-created_at', '-rating')[:10]
        
        # Get top 5 most active chefs (fake data for now)
        # In a real app, this would be based on actual chef activity
        top_chefs = Chef.objects.annotate(
            recipe_count=Count('recipe')
        ).order_by('-recipe_count', '-rating')[:5]
        
        # If no chefs exist, create some fake ones
        if not top_chefs.exists():
            fake_chefs = [
                {
                    'name': 'Chef Antonio Rossi',
                    'avatar': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
                    'specialty': 'Italian Cuisine',
                    'verified': True,
                    'followers': 15400,
                    'recipes_count': 89,
                    'rating': 4.9
                },
                {
                    'name': 'Chef Sarah Kim',
                    'avatar': 'https://images.unsplash.com/photo-1494790108755-2616b612b786?w=150&h=150&fit=crop&crop=face',
                    'specialty': 'Korean Fusion',
                    'verified': True,
                    'followers': 12800,
                    'recipes_count': 67,
                    'rating': 4.8
                },
                {
                    'name': 'Chef Marcus Johnson',
                    'avatar': 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face',
                    'specialty': 'Plant-Based',
                    'verified': False,
                    'followers': 9600,
                    'recipes_count': 45,
                    'rating': 4.7
                },
                {
                    'name': 'Chef Elena Rodriguez',
                    'avatar': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face',
                    'specialty': 'Mediterranean',
                    'verified': True,
                    'followers': 11200,
                    'recipes_count': 78,
                    'rating': 4.9
                },
                {
                    'name': 'Chef Pierre Dubois',
                    'avatar': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face',
                    'specialty': 'French Pastry',
                    'verified': True,
                    'followers': 8900,
                    'recipes_count': 56,
                    'rating': 4.8
                }
            ]
            
            # Create fake chef objects
            fake_chef_objects = []
            for chef_data in fake_chefs:
                chef = Chef(
                    name=chef_data['name'],
                    avatar=chef_data['avatar'],
                    specialty=chef_data['specialty'],
                    verified=chef_data['verified'],
                    followers=chef_data['followers'],
                    recipes_count=chef_data['recipes_count'],
                    rating=chef_data['rating']
                )
                fake_chef_objects.append(chef)
            
            top_chefs = fake_chef_objects
        
        # Serialize the data
        data = {
            'floating_recipes': RecipeSerializer(floating_recipes, many=True).data,
            'popular_recipes': RecipeSerializer(recipes_with_popularity, many=True).data,
            'quick_easy_recipes': RecipeSerializer(quick_easy_recipes, many=True).data,
            'vegetarian_recipes': RecipeSerializer(vegetarian_recipes, many=True).data,
            'browse_recipes': RecipeSerializer(browse_recipes, many=True).data,
            'top_chefs': ChefSerializer(top_chefs, many=True).data if hasattr(top_chefs, 'model') else top_chefs
        }
        
        return Response(data)