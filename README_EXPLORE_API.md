# Explore API Endpoint

## Overview

The `ExploreDataView` endpoint provides all the necessary data for the frontend explore page in a single API call.

## Endpoint

```
GET /api/explore/
```

## Response Structure

The endpoint returns a JSON response with the following structure:

```json
{
  "floating_recipes": [
    // 2 random recipe cards
  ],
  "popular_recipes": [
    // Top 5 most popular recipes (by user saves + meal plan additions)
  ],
  "quick_easy_recipes": [
    // 5 recipes tagged as quick and easy (prep + cook time <= 30 min)
  ],
  "vegetarian_recipes": [
    // 5 recipes tagged as vegetarian
  ],
  "browse_recipes": [
    // 10 additional recipes for the browse section
  ],
  "top_chefs": [
    // Top 5 most active chefs
  ]
}
```

## Recipe Data Fields

Each recipe object includes:

- `id`: Recipe ID
- `name`: Recipe name
- `description`: Recipe description
- `prep_time`: Preparation time in minutes
- `cook_time`: Cooking time in minutes
- `servings`: Number of servings
- `difficulty`: Easy, Medium, or Hard
- `image`: Recipe image URL
- `rating`: Recipe rating (0.0 - 5.0)
- `likes`: Number of likes
- `tags`: Array of recipe tags
- `chef`: Chef information
- `created_at`: Creation timestamp

## Chef Data Fields

Each chef object includes:

- `id`: Chef ID
- `name`: Chef name
- `avatar`: Chef avatar URL
- `specialty`: Chef's specialty cuisine
- `verified`: Whether the chef is verified
- `followers`: Number of followers
- `recipes_count`: Number of recipes
- `rating`: Chef rating (0.0 - 5.0)

## Popularity Calculation

Popular recipes are determined by:

1. Number of user saves (`UserSave` model)
2. Number of meal plan additions (`MealPlan` model)
3. Recipe likes (as a tiebreaker)

## Quick & Easy Filtering

Recipes are considered "quick and easy" if:

- `prep_time` ≤ 15 minutes AND
- `cook_time` ≤ 15 minutes

## Vegetarian Filtering

Recipes are considered vegetarian if they have a tag containing "vegetarian" (case-insensitive).

## Browse Recipes

The browse section shows up to 10 recipes that are not already included in other sections, ordered by creation date and rating.

## Fake Chef Data

If no chefs exist in the database, the endpoint will return 5 fake chef profiles with realistic data for demonstration purposes.

## Usage Example

```javascript
// Frontend API call
fetch("/api/explore/")
  .then((response) => response.json())
  .then((data) => {
    console.log("Floating recipes:", data.floating_recipes);
    console.log("Popular recipes:", data.popular_recipes);
    console.log("Quick & easy recipes:", data.quick_easy_recipes);
    console.log("Vegetarian recipes:", data.vegetarian_recipes);
    console.log("Browse recipes:", data.browse_recipes);
    console.log("Top chefs:", data.top_chefs);
  });
```

## Dependencies

- Django REST Framework
- Django models: Recipe, Chef, Tag, UserSave, MealPlan
- User authentication (for tracking saves and meal plans)

## Notes

- The endpoint is publicly accessible (no authentication required)
- Random floating recipes are selected using Python's `random.sample()`
- All recipe counts are limited to prevent performance issues
- The endpoint handles cases where insufficient data exists gracefully
