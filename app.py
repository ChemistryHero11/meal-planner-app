"""
Meal Planner App - Flask Application

This is the main application file for the Meal Planner app which uses TheMealDB API
to display and manage recipes. The app consists of two main sections: Menu and Plan.
The Menu section allows users to browse recipes and add custom ones, while the Plan
section helps users generate a weekly meal plan with a grocery list.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import random
import uuid

app = Flask(__name__)
app.secret_key = 'mealplanner_secret_key'  # Required for flash messages and sessions

# In-memory storage for custom recipes
custom_recipes = []

# Base URL for TheMealDB API
MEALDB_API_BASE_URL = "https://www.themealdb.com/api/json/v1/1"

# Predefined meal categories
MEAL_CATEGORIES = [
    "Breakfast", "Lunch", "Dinner", "Snacks", "Desserts", "Drinks"
]

# Predefined grocery categories
GROCERY_CATEGORIES = [
    "Produce", "Dairy", "Meat", "Grains", "Canned Goods", "Frozen Foods", 
    "Condiments", "Spices", "Baking Supplies", "Others"
]

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/menu')
def menu():
    """
    Display recipe categories from TheMealDB API and custom recipes.
    """
    try:
        # Fetch categories from TheMealDB API
        response = requests.get(f"{MEALDB_API_BASE_URL}/categories.php")
        categories_data = response.json()
        
        if 'categories' in categories_data:
            api_categories = categories_data['categories']
        else:
            api_categories = []
            flash("Could not fetch categories from API, showing default categories")
            
        # Custom recipes disabled in serverless environment
        user_recipes = []
        
        return render_template(
            'menu.html', 
            api_categories=api_categories,
            custom_recipes=user_recipes
        )
    except Exception as e:
        flash(f"Error fetching categories: {str(e)}")
        return render_template('menu.html', api_categories=[], custom_recipes=[])

@app.route('/menu/<category>')
def menu_category(category):
    """
    Display meals for a specific category from TheMealDB API.
    """
    try:
        # Fetch meals for the given category
        response = requests.get(f"{MEALDB_API_BASE_URL}/filter.php?c={category}")
        meals_data = response.json()
        
        if 'meals' in meals_data and meals_data['meals']:
            meals = meals_data['meals']
        else:
            meals = []
            flash(f"No meals found for category: {category}")
            
        return render_template('menu.html', category=category, meals=meals)
    except Exception as e:
        flash(f"Error fetching meals: {str(e)}")
        return render_template('menu.html', category=category, meals=[])

@app.route('/meal/<meal_id>')
def meal_detail(meal_id):
    """
    Display detailed information for a specific meal.
    """
    try:
        # Check if this is a custom recipe
        for recipe in custom_recipes:
            if str(recipe['id']) == meal_id:
                return render_template('meal_detail.html', meal=recipe, is_custom=True)
        
        # Otherwise fetch from the API
        response = requests.get(f"{MEALDB_API_BASE_URL}/lookup.php?i={meal_id}")
        meal_data = response.json()
        
        if 'meals' in meal_data and meal_data['meals']:
            meal = meal_data['meals'][0]
            
            # Extract ingredients and measurements
            ingredients = []
            for i in range(1, 21):  # TheMealDB provides up to 20 ingredients
                ingredient = meal.get(f'strIngredient{i}')
                measure = meal.get(f'strMeasure{i}')
                
                if ingredient and ingredient.strip():
                    ingredients.append({
                        'name': ingredient,
                        'measure': measure
                    })
            
            return render_template('meal_detail.html', meal=meal, ingredients=ingredients, is_custom=False)
        else:
            flash(f"Meal with ID {meal_id} not found")
            return redirect(url_for('menu'))
    except Exception as e:
        flash(f"Error fetching meal details: {str(e)}")
        return redirect(url_for('menu'))

@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    """
    Handle custom recipe form submission.
    Note: Custom recipes are disabled in production due to serverless limitations.
    """
    if request.method == 'POST':
        # In serverless environments, we can't persist data without a database
        flash("Custom recipes are currently disabled in the live version. This feature requires a database to store recipes permanently. You can still browse recipes from TheMealDB!", "info")
        return redirect(url_for('menu'))
    
    # Show info message for GET requests too
    flash("Custom recipes are currently disabled in the live version. This feature requires a database to store recipes permanently.", "info")
    return redirect(url_for('menu'))

@app.route('/custom_recipes')
def custom_recipes_list():
    """
    Display all user-added custom recipes.
    Note: Custom recipes are disabled in production due to serverless limitations.
    """
    flash("Custom recipes are currently disabled in the live version. This feature requires a database to store recipes permanently.", "info")
    return redirect(url_for('menu'))

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    """
    Handle meal plan generation based on user survey.
    """
    if request.method == 'POST':
        # Process survey form
        cravings = request.form.get('cravings', '')
        dietary_goals = request.form.get('dietary_goals', '')
        budget = request.form.get('budget', '')
        
        # Generate meal plan and grocery list
        meal_plan = generate_meal_plan(cravings, dietary_goals, budget)
        grocery_list = generate_grocery_list(meal_plan)
        
        return render_template(
            'plan.html', 
            meal_plan=meal_plan, 
            grocery_list=grocery_list,
            cravings=cravings,
            dietary_goals=dietary_goals,
            budget=budget,
            submitted=True
        )
    
    # For GET requests, render the form
    return render_template('plan.html', submitted=False)

def generate_meal_plan(cravings, dietary_goals, budget):
    """
    Generate a 7-day meal plan based on user preferences.
    
    Args:
        cravings (str): User's food cravings
        dietary_goals (str): User's dietary restrictions or goals
        budget (str): User's budget preference
        
    Returns:
        dict: A 7-day meal plan with meals for each day
    """
    # For MVP, we'll generate a placeholder meal plan
    # In a real implementation, we would use the API to fetch meals
    # that match the user's preferences
    
    meal_categories = {
        "breakfast": ["Pancakes", "Oatmeal", "Eggs Benedict", "Fruit Bowl", "Yogurt Parfait", "Avocado Toast", "Breakfast Burrito"],
        "snack1": ["Apple", "Banana", "Protein Bar", "Mixed Nuts", "Greek Yogurt", "Carrots & Hummus", "Granola"],
        "lunch": ["Caesar Salad", "Turkey Sandwich", "Chicken Wrap", "Quinoa Bowl", "Tuna Salad", "Vegetable Soup", "Buddha Bowl"],
        "snack2": ["Popcorn", "Cucumber Slices", "Cheese Stick", "Rice Cakes", "Edamame", "Smoothie", "Trail Mix"],
        "dinner": ["Spaghetti", "Grilled Chicken", "Salmon", "Stir Fry", "Tacos", "Pizza", "Roast Beef"],
        "dessert": ["Ice Cream", "Brownie", "Fruit Salad", "Cheesecake", "Pudding", "Cookies", "Apple Pie"]
    }
    
    # Create a 7-day meal plan
    meal_plan = {}
    for day in range(1, 8):
        day_key = f"day{day}"
        meal_plan[day_key] = {}
        
        for meal_type, options in meal_categories.items():
            # Randomly select a meal from the options
            meal_plan[day_key][meal_type] = random.choice(options)
    
    return meal_plan

def generate_grocery_list(meal_plan):
    """
    Generate a grocery list based on the given meal plan.
    
    Args:
        meal_plan (dict): The meal plan to generate a grocery list for
        
    Returns:
        dict: A categorized grocery list
    """
    # For MVP, we'll generate a placeholder grocery list
    # In a real implementation, we would extract ingredients from the
    # meals in the meal plan and categorize them
    
    # Placeholder grocery items by category
    grocery_items = {
        "Produce": ["Apples", "Bananas", "Lettuce", "Tomatoes", "Cucumbers", "Carrots", "Avocados"],
        "Dairy": ["Milk", "Eggs", "Cheese", "Yogurt", "Butter"],
        "Meat": ["Chicken Breast", "Ground Beef", "Salmon", "Turkey"],
        "Grains": ["Bread", "Pasta", "Rice", "Oats", "Quinoa"],
        "Canned Goods": ["Beans", "Tuna", "Soup", "Tomato Sauce"],
        "Frozen Foods": ["Frozen Vegetables", "Ice Cream", "Frozen Berries"],
        "Condiments": ["Ketchup", "Mustard", "Mayonnaise", "Olive Oil", "Vinegar"],
        "Spices": ["Salt", "Pepper", "Basil", "Oregano", "Cinnamon"],
        "Baking Supplies": ["Flour", "Sugar", "Baking Powder", "Vanilla Extract"],
        "Others": ["Coffee", "Tea", "Chips", "Crackers", "Nuts"]
    }
    
    # Create a grocery list with random items from each category
    grocery_list = {}
    for category, items in grocery_items.items():
        # Select a random number of items from each category
        num_items = random.randint(2, len(items))
        selected_items = random.sample(items, num_items)
        grocery_list[category] = selected_items
    
    return grocery_list

if __name__ == '__main__':
    app.run(debug=True)
