import pytest
from _pytest.fixtures import fixture
from faker import Faker
from faker_food import FoodProvider

from pantry.tests.factories import RecipeFactory, UserFactory

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

@pytest.mark.django_db
class TestRecipeViewSet():
    @fixture(autouse=True)
    def setup(self, client):
        self.user = UserFactory()
        self.other_user = UserFactory()

        self.my_recipe = RecipeFactory(created_by=self.user)
        self.other_recipe = RecipeFactory(created_by=self.other_user)

        self.client = client
        self.client.force_login(self.user)

    def test_get_queryset(self):
        response = self.client.get("/api/recipes/")
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == self.my_recipe.id

        self.user.following.add(self.other_user)

        response = self.client.get("/api/recipes/")
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]["id"] == self.other_recipe.id
        assert response.json()[1]["id"] == self.my_recipe.id

    def test_create(self):
        pass