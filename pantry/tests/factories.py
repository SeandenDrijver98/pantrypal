from random import randint

from faker import Faker
from factory import LazyAttribute, SubFactory, post_generation
from factory.django import DjangoModelFactory
from faker_food import FoodProvider

from pantry.models import Ingredient, User, Recipe, Food, FoodInventory

fake = Faker()

fake.add_provider(FoodProvider)
# >>> fake.dish()
# >>> fake.dish_description()
# >>> fake.ethnic_category()
# >>> fake.fruit()
# >>> fake.ingredient()
# >>> fake.measurement()
# >>> fake.metric_measurement()
# >>> fake.measurement_size()
# >>> fake.spice()
# >>> fake.sushi()
# >>> fake.vegetable()


class IngredientFactory(DjangoModelFactory):
    """A factory class used for creating Ingredients, only for testing purposes."""

    title = LazyAttribute(lambda obj: fake.text.title())
    quantity = LazyAttribute(lambda _: randint(20, 120))

    class Meta:
        model = Ingredient

class UserFactory(DjangoModelFactory):
    """A factory class used for creating Users, only for testing purposes."""

    email = LazyAttribute(lambda obj: fake.email())
    first_name = LazyAttribute(lambda obj: fake.first_name())
    last_name = LazyAttribute(lambda obj: fake.last_name())

    class Meta:
        model = User

class RecipeFactory(DjangoModelFactory):
    """A factory class used for creating Recipes, only for testing purposes."""

    name = LazyAttribute(lambda obj: fake.dish())
    directions = LazyAttribute(lambda obj: fake.dish_description())
    calories = LazyAttribute(lambda obj: randint(20, 120))
    protein = LazyAttribute(lambda obj: randint(20, 120))
    url = LazyAttribute(lambda obj: fake.url())
    created_by = SubFactory(UserFactory)


    class Meta:
        model = Recipe


class FoodFactory(DjangoModelFactory):
    """A factory class used for creating Food, only for testing purposes."""

    name = LazyAttribute(lambda obj: fake.vegetable())

    class Meta:
        model = Food

class FoodInventoryFactory(DjangoModelFactory):
    """A factory class used for creating Food Inventories, only for testing purposes."""

    user = SubFactory(UserFactory)
    food = SubFactory(IngredientFactory)
    quantity = LazyAttribute(lambda _: randint(10, 300))
    quantity_uom = LazyAttribute(lambda obj: fake.measurement())
    expiration_date = LazyAttribute(lambda obj: fake.fake.date_time_this_month().date())
    class Meta:
        model = FoodInventory