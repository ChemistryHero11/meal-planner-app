# Meal Planner App

A Flask web application that leverages TheMealDB API to display and manage recipes. The app allows users to browse recipes, add custom recipes, and generate weekly meal plans with grocery lists.

## Features

- **Menu Section**
  - Browse recipe categories from TheMealDB API
  - View meals within each category
  - View detailed information about individual meals
  - Add and manage custom recipes

- **Plan Section**
  - Generate personalized 7-day meal plans based on preferences
  - Create grocery lists organized by food categories
  - Interactive checklist for grocery items

## Project Structure

```
meal-planner-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Project dependencies
├── static/                # Static files
│   └── css/
│       └── styles.css     # Custom CSS styles
└── templates/             # HTML templates
    ├── base.html          # Base template with navigation
    ├── index.html         # Home page
    ├── menu.html          # Recipe categories and meals
    ├── meal_detail.html   # Detailed meal information
    ├── add_recipe.html    # Form to add custom recipes
    ├── custom_recipes.html # List of user's custom recipes
    └── plan.html          # Meal plan and grocery list
```

## Installation

1. Clone the repository or download the source code
2. Create and activate a virtual environment (recommended)

   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # macOS/Linux
   ```

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application

   ```
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`

3. Use the navigation menu to explore the app's features:
   - Browse recipes in the Menu section
   - Add your own recipes using the Add Recipe form
   - Generate a meal plan in the Plan section

## API Integration

This application uses TheMealDB API (https://www.themealdb.com/api.php) to fetch recipe data. The free tier of the API is used, which provides access to a limited set of recipes.

## Notes

- This is an MVP (Minimum Viable Product) implementation
- Custom recipes are stored in-memory and will be lost when the server restarts
- For a production version, a database should be implemented for persistent storage
