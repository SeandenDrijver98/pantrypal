from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pantry.models import FoodInventory, Recipe, Ingredient
from pantry.serializers import FoodInventorySerializer


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

        missing_ingredients = []

        for ingredient in ingredients_to_create:
            food_inventory = FoodInventory.objects.filter(food__name=ingredient["food__name"])
            if not food_inventory.exists():
                missing_ingredients.append(ingredient)
            else:
                food_inventory = food_inventory.first()
                if food_inventory.quantity < ingredient["quantity"]:
                    missing_ingredients.append({"food": ingredient["food__name"], "quantity":ingredient["quantity"] - food_inventory.quantity, "quantity_uom":ingredient["quantity_uom"]})
        # TODO if An ingredient is listed as needed twice in the response, combine the quantities



        return Response({"uses": ingredients_to_create, "missing": missing_ingredients})



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