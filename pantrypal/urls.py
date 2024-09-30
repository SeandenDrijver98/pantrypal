"""
URL configuration for pantrypal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from pantry.views import NeededIngredientsView, CreatableRecipes, InventoryViewSet, UserViewSet, RecipeViewSet

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/users', UserViewSet)
router.register(r"api/inventory", InventoryViewSet)
router.register(r"api/recipes", RecipeViewSet)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/needed_ingredients/', NeededIngredientsView.as_view(), name='needed_ingredients'),
    path('api/creatable_recipes/', CreatableRecipes.as_view(), name='creatable_recipes'),
] + router.urls
