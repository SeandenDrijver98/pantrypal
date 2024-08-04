from random import randint

from faker import Faker
from factory import LazyAttribute, SubFactory, post_generation
from factory.django import DjangoModelFactory

from pantry.models import Ingredient

fake = Faker()


class IngredientFactory(DjangoModelFactory):
    """A factory class used for creating Ingredients, only for testing purposes."""

    title = LazyAttribute(lambda obj: fake.text.title())
    quantity = LazyAttribute(lambda _: randint(20, 120))


    class Meta:
        model = Ingredient