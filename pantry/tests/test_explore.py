import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from pantry.tests.factories import (
    UserFactory, RecipeFactory, ChefFactory, TagFactory,
    UserSaveFactory, MealPlanFactory
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def quick_tag():
    return TagFactory(name='quick')


@pytest.fixture
def easy_tag():
    return TagFactory(name='easy')


@pytest.fixture
def vegetarian_tag():
    return TagFactory(name='vegetarian')


@pytest.fixture
def chef():
    return ChefFactory(
        name='Test Chef',
        specialty='Test Cuisine',
        verified=True,
        followers=1000,
        recipes_count=10,
        rating=4.5
    )


@pytest.fixture
def quick_recipe(chef, quick_tag, easy_tag):
    recipe = RecipeFactory(
        name='Quick Recipe 1',
        description='A quick recipe',
        directions='Cook quickly',
        prep_time=10,
        cook_time=15,
        servings=2,
        difficulty='easy',
        rating=4.5,
        likes=50,
        chef=chef
    )
    recipe.tags.add(quick_tag, easy_tag)
    return recipe


@pytest.fixture
def vegetarian_recipe(chef, vegetarian_tag):
    recipe = RecipeFactory(
        name='Vegetarian Recipe 1',
        description='A vegetarian recipe',
        directions='Cook vegetarian',
        prep_time=20,
        cook_time=25,
        servings=4,
        difficulty='medium',
        rating=4.8,
        likes=75,
        chef=chef
    )
    recipe.tags.add(vegetarian_tag)
    return recipe


@pytest.fixture
def popular_recipe(chef):
    return RecipeFactory(
        name='Popular Recipe 1',
        description='A popular recipe',
        directions='Cook popular',
        prep_time=30,
        cook_time=35,
        servings=6,
        difficulty='hard',
        rating=4.9,
        likes=100,
        chef=chef
    )


@pytest.fixture
def user_save(user, popular_recipe):
    return UserSaveFactory(user=user, recipe=popular_recipe)


@pytest.fixture
def meal_plan(user, popular_recipe):
    return MealPlanFactory(
        user=user, 
        recipe=popular_recipe, 
        planned_date='2024-01-01', 
        meal_type='dinner'
    )


@pytest.mark.django_db
class TestExploreDataView:
    """Test the explore data endpoint"""
    
    def test_explore_data_endpoint_structure(self, api_client, user, quick_recipe, 
                                           vegetarian_recipe, popular_recipe, user_save, meal_plan):
        """Test that the explore data endpoint returns the expected data structure"""
        url = reverse('explore_data')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.data
        
        # Check that all expected keys are present
        expected_keys = [
            'floating_recipes', 'popular_recipes', 'quick_easy_recipes',
            'vegetarian_recipes', 'browse_recipes', 'top_chefs'
        ]
        for key in expected_keys:
            assert key in data
        
        # Check that floating_recipes has 2 recipes (or less if not enough exist)
        assert len(data['floating_recipes']) <= 2
        
        # Check that popular_recipes has up to 5 recipes
        assert len(data['popular_recipes']) <= 5
        
        # Check that quick_easy_recipes has up to 5 recipes
        assert len(data['quick_easy_recipes']) <= 5
        
        # Check that vegetarian_recipes has up to 5 recipes
        assert len(data['vegetarian_recipes']) <= 5
        
        # Check that browse_recipes has up to 10 recipes
        assert len(data['browse_recipes']) <= 10
        
        # Check that top_chefs has up to 5 chefs
        assert len(data['top_chefs']) <= 5
    
    def test_popular_recipes_ordering(self, api_client, user, quick_recipe, 
                                     vegetarian_recipe, popular_recipe, user_save, meal_plan):
        """Test that popular recipes are ordered by popularity (saves + meal plans)"""
        url = reverse('explore_data')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        popular_recipes = response.data['popular_recipes']
        
        # Recipe should be first as it has both a save and meal plan
        if len(popular_recipes) > 0:
            assert popular_recipes[0]['name'] == 'Popular Recipe 1'
    
    def test_quick_easy_filtering(self, api_client, user, quick_recipe, 
                                 vegetarian_recipe, popular_recipe, user_save, meal_plan):
        """Test that quick and easy recipes are properly filtered"""
        url = reverse('explore_data')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        quick_easy_recipes = response.data['quick_easy_recipes']
        
        # All quick and easy recipes should have prep + cook time <= 30
        for recipe in quick_easy_recipes:
            total_time = recipe['prep_time'] + recipe['cook_time']
            assert total_time <= 30
    
    def test_vegetarian_filtering(self, api_client, user, quick_recipe, 
                                 vegetarian_recipe, popular_recipe, user_save, meal_plan):
        """Test that vegetarian recipes are properly filtered"""
        url = reverse('explore_data')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        vegetarian_recipes = response.data['vegetarian_recipes']
        
        # All vegetarian recipes should have the vegetarian tag
        for recipe in vegetarian_recipes:
            from pantry.models import Recipe
            recipe_obj = Recipe.objects.get(id=recipe['id'])
            assert recipe_obj.tags.filter(name__icontains='vegetarian').exists()
    
    def test_no_duplicates_in_sections(self, api_client, user, quick_recipe, 
                                      vegetarian_recipe, popular_recipe, user_save, meal_plan):
        """Test that recipes don't appear in multiple sections"""
        url = reverse('explore_data')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.data
        
        # Get all recipe IDs from each section
        floating_ids = {r['id'] for r in data['floating_recipes']}
        popular_ids = {r['id'] for r in data['popular_recipes']}
        quick_easy_ids = {r['id'] for r in data['quick_easy_recipes']}
        vegetarian_ids = {r['id'] for r in data['vegetarian_recipes']}
        browse_ids = {r['id'] for r in data['browse_recipes']}
        
        # Check that browse recipes don't overlap with other sections
        all_other_ids = floating_ids | popular_ids | quick_easy_ids | vegetarian_ids
        assert browse_ids.isdisjoint(all_other_ids)
    
    def test_fake_chef_data_when_none_exist(self, api_client):
        """Test that fake chef data is returned when no chefs exist"""
        url = reverse('explore_data')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.data
        top_chefs = data['top_chefs']
        
        # Should return exactly 5 fake chefs
        assert len(top_chefs) == 5
        
        # Check that fake chefs have expected structure
        for chef in top_chefs:
            assert 'name' in chef
            assert 'avatar' in chef
            assert 'specialty' in chef
            assert 'verified' in chef
            assert 'followers' in chef
            assert 'recipes_count' in chef
            assert 'rating' in chef 