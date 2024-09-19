from flask import Flask, request, jsonify
import pymongo
import requests
import os

app = Flask(__name__)

# MongoDB Connection (for MongoDB Atlas, replace with your connection string)

# MongoDB Atlas connection string
# Replace <username> and <password> with your actual MongoDB credentials
#MONGO_URI = 'mongodb+srv://<username>:<password>@cluster0.mongodb.net/recipeDB?retryWrites=true&w=majority'

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("No MONGO_URI set for Flask application. Did you forget to set it?")

print(MONGO_URI)

# Connect to MongoDB Atlas
client = pymongo.MongoClient(MONGO_URI)
db = client['recipeDB']
recipes_collection = db['recipes'] #saved recipes on mongodb so we save an api call to spoonacular

# Spoonacular API Key
#SPOONACULAR_API_KEY = 'your_spoonacular_api_key'
SPOONACULAR_API_KEY = os.getenv('SPOONACULAR_API_KEY')
print(SPOONACULAR_API_KEY)
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Received request: ", req)  # Debugging - Check the entire request body

    # Get intent name to verify it's the correct intent
    intent = req.get("queryResult").get("intent").get("displayName")
    print("Intent: ", intent)  # Debugging - Print the detected intent

    if intent == "Find Recipe Intent":
        # Extract parameters from the request
        ingredients = req.get("queryResult").get("parameters").get("ingredients", [])
        meal_type = req.get("queryResult").get("parameters").get("meal_type", "")

        print("Ingredients: ", ingredients)  # Debugging - Print the ingredients
        print("Meal Type: ", meal_type)  # Debugging - Print the meal type

        # Fetch recipes from Spoonacular API based on meal type and ingredients
        recipes = fetch_recipes_with_details(ingredients, meal_type)

        # If we get any recipes, return them to Dialogflow
        if recipes:
            response_text = format_recipe_details(recipes, ingredients)
            #print("Sending response: ", response_text)  # Debugging - Print the response sent to Dialogflow
            return response_text
        else:
            return jsonify({"fulfillmentText": "Sorry, I couldn't find any recipes with those ingredients."})

    return jsonify({"fulfillmentText": "Sorry, I couldn't understand your request."})

# Function to fetch recipes from Spoonacular API, including details for each recipe
def fetch_recipes_with_details(ingredients, meal_type):
    # First, check MongoDB for existing recipes
    query = {
        "ingredients": {"$all": ingredients},  # Ensure all ingredients match
        "meal_type": meal_type
    }
    stored_recipes = list(recipes_collection.find(query))

    if stored_recipes:
        print("Found recipes in MongoDB")
        return stored_recipes

    print("No recipes in MongoDB, fetching from Spoonacular API")
    # If no recipes in MongoDB, fetch from Spoonacular API
    ingredients_str = ",".join(ingredients)
    url = f"https://api.spoonacular.com/recipes/complexSearch?apiKey={SPOONACULAR_API_KEY}&includeIngredients={ingredients_str}&number=1"

    if meal_type:
        url += f"&type={meal_type}"

    print("Spoonacular API URL: ", url)  # Debugging - Print the API URL
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            # Store the recipes in MongoDB
            for recipe in data['results']:
                recipe['ingredients'] = ingredients  # Add ingredients for MongoDB searchability
                recipe['meal_type'] = meal_type
                recipes_collection.insert_one(recipe)  # Store the recipe in MongoDB

            return data['results']
    else:
        print("Error fetching recipes from Spoonacular.")
        return None

def fetch_detailed_recipe_info(recipe_id):
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={SPOONACULAR_API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch recipe details")


def format_recipe_details(recipes, ingredients):
    if not recipes:
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["I couldn't find any recipes with those ingredients."]
                    }
                }
            ]
        }


    ingredients_str = ", ".join(ingredients)

    # Initialize the response array with multiple messages
    fulfillment_messages = []

    # Add a text message first, including the list of ingredients
    fulfillment_messages.append({
        "text": {
            "text": [f"Here are some recipes you can make with:\n {ingredients_str}"]
        }
    })

    # Iterate through each recipe and format the response
    for recipe in recipes:
        title = recipe.get('title', 'No title available')
        image_url = recipe.get('image', '')
        recipe_id = recipe.get('id', 'No ID available')
        recipe_details = fetch_detailed_recipe_info(recipe_id)

        servings = recipe_details.get('servings', 'N/A')
        ready_in_minutes = recipe_details.get('readyInMinutes', 'N/A')
        summary = recipe_details.get('summary', '').replace('<b>', '').replace('</b>', '')
        allIngredients = recipe_details.get('extendedIngredients', [])
        instructions = recipe_details.get('instructions', 'No instructions available')

        # Nutrition info
        nutrition = recipe_details.get('nutrition', {}).get('nutrients', [])
        calories = next((item for item in nutrition if item["title"] == "Calories"), {}).get('amount', 'N/A')
        protein = next((item for item in nutrition if item["title"] == "Protein"), {}).get('amount', 'N/A')
        fat = next((item for item in nutrition if item["title"] == "Fat"), {}).get('amount', 'N/A')
        carbs = next((item for item in nutrition if item["title"] == "Carbohydrates"), {}).get('amount', 'N/A')

        # Dietary restrictions
        vegetarian = recipe_details.get('vegetarian', False)
        vegan = recipe_details.get('vegan', False)
        gluten_free = recipe_details.get('glutenFree', False)
        dairy_free = recipe_details.get('dairyFree', False)

        # Additional details
        cuisines = ', '.join(recipe_details.get('cuisines', 'N/A'))
        dish_types = ', '.join(recipe_details.get('dishTypes', 'N/A'))
        likes = recipe_details.get('aggregateLikes', 0)
        health_score = recipe_details.get('healthScore', 'Not available')
        price_per_serving = recipe_details.get('pricePerServing', 0) / 100

        # Create an image block for the recipe
        image_block = {
            "type": "image",
            "rawUrl": image_url,
            "accessibilityText": f"Image of {title}"
        }

        # Fetch detailed information about the recipe
        recipe_details = fetch_detailed_recipe_info(recipe_id)

        if recipe_details:
            servings = recipe_details.get('servings', 'N/A')
            ready_in_minutes = recipe_details.get('readyInMinutes', 'N/A')
            summary = recipe_details.get('summary', '').replace('<b>', '').replace('</b>', '')

            # Create the info block for the recipe
            recipe_block = {
                "type": "info",
                "title": title,
                "subtitle": f"🌍 Cuisine: {cuisines}\n 🍽️ Dish Type: {dish_types}\n 👍 Popularity: {likes} likes\n 💪 Health Score: {health_score}/100\n 💰 Price per serving: ${price_per_serving:.2f}\n 🔥 Calories: {calories} kcal\n 💪 Protein: {protein} g\n 🧈 Fat: {fat} g\n 🥔 Carbohydrates: {carbs} g",
                "image": {
                    "src": image_url,
                    "alt": f"Image of {title}"
                },
                "actionLink": recipe_details.get('sourceUrl', 'N/A')
            }

            # Add the rich content for the recipe (image + info)
            fulfillment_messages.append({
                "payload": {
                    "richContent": [
                        [image_block, recipe_block]
                    ]
                }
            })

            # Add the ingredients section
            ingredient_list = "\nIngredients:\n" + "\n".join([f"- {ingredient.get('original', 'N/A')}" for ingredient in allIngredients])

            # Create a simple text response with more details
            fulfillment_messages.append({
                "text": {

                    "text": [
                        f"{ingredient_list} \n\nInstructions:\n{instructions}\n"
                    ]
                }
            })

    # Return the response with multiple fulfillment messages
    return {"fulfillmentMessages": fulfillment_messages}

# Function to format the detailed recipe information for multiple recipes
def format_recipe_details2(recipes):
    if not recipes:
        return {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": ["I couldn't find any recipes with those ingredients."]
                    }
                }
            ]
        }

    # Initialize the rich response array
    rich_response = []

    # Iterate through each recipe and format the response
    for recipe in recipes:
        title = recipe.get('title', 'No title available')
        image_url = recipe.get('image', '')
        recipe_id = recipe.get('id', 'No ID available')

        # Create the image block for the recipe (using image_url)
        rich_response.append({
            "type": "image",
            "rawUrl": image_url,
            "accessibilityText": f"Image of {title}"  # Image description for accessibility
        })

        # Fetch detailed information about the recipe
        recipe_details = fetch_detailed_recipe_info(recipe_id)

        if recipe_details:
            # Extract relevant recipe details
            servings = recipe_details.get('servings', 'N/A')
            ready_in_minutes = recipe_details.get('readyInMinutes', 'N/A')
            summary = recipe_details.get('summary', '').replace('<b>', '').replace('</b>', '')
            ingredients = recipe_details.get('extendedIngredients', [])
            instructions = recipe_details.get('instructions', 'No instructions available')

            # Nutrition info
            nutrition = recipe_details.get('nutrition', {}).get('nutrients', [])
            calories = next((item for item in nutrition if item["title"] == "Calories"), {}).get('amount', 'N/A')
            protein = next((item for item in nutrition if item["title"] == "Protein"), {}).get('amount', 'N/A')
            fat = next((item for item in nutrition if item["title"] == "Fat"), {}).get('amount', 'N/A')
            carbs = next((item for item in nutrition if item["title"] == "Carbohydrates"), {}).get('amount', 'N/A')

            # Dietary restrictions
            vegetarian = recipe_details.get('vegetarian', False)
            vegan = recipe_details.get('vegan', False)
            gluten_free = recipe_details.get('glutenFree', False)
            dairy_free = recipe_details.get('dairyFree', False)

            # Additional details
            cuisines = ', '.join(recipe_details.get('cuisines', 'N/A'))
            dish_types = ', '.join(recipe_details.get('dishTypes', 'N/A'))
            likes = recipe_details.get('aggregateLikes', 0)
            health_score = recipe_details.get('healthScore', 'Not available')
            price_per_serving = recipe_details.get('pricePerServing', 0) / 100

            # Create the info block for the recipe
            recipe_block = {
                "type": "info",
                "title": title,
                "subtitle": f"⏱️ Ready in: {ready_in_minutes} minutes\n🍽️ Servings: {servings}",
                "image": {
                    "src": image_url,  # Image URL for the recipe
                    "alt": f"Image of {title}"  # Alt text for accessibility
                },
                "description": summary[:150] + "...",  # A brief summary
                "actionLink": recipe_details.get('sourceUrl', 'N/A'),
                "info": f"""
                    🌍 Cuisine: {cuisines}
                    🍽️ Dish Type: {dish_types}
                    👍 Popularity: {likes} likes
                    💪 Health Score: {health_score}/100
                    💰 Price per serving: ${price_per_serving:.2f}
                    - Calories: {calories} kcal
                    - Protein: {protein} g
                    - Fat: {fat} g
                    - Carbohydrates: {carbs} g
                """
            }

            # Add the ingredients section
            ingredient_list = "\nIngredients:\n" + "\n".join([f"- {ingredient.get('original', 'N/A')}" for ingredient in ingredients])
            recipe_block['info'] += ingredient_list

            # Add the instructions section
            recipe_block['info'] += f"\n\nInstructions:\n{instructions}\n"

            # Add dietary restrictions
            recipe_block['info'] += "\nDietary Restrictions:\n"
            recipe_block['info'] += f"- Vegetarian: {'Yes' if vegetarian else 'No'}\n"
            recipe_block['info'] += f"- Vegan: {'Yes' if vegan else 'No'}\n"
            recipe_block['info'] += f"- Gluten Free: {'Yes' if gluten_free else 'No'}\n"
            recipe_block['info'] += f"- Dairy Free: {'Yes' if dairy_free else 'No'}\n"

            # Append the recipe block to the rich response
            rich_response.append(recipe_block)

    # Return the response with the rich content structure
    return {"fulfillmentMessages": [{"payload": {"richContent": [rich_response]}}]}

if __name__ == '__main__':
    app.run(port=5000, debug=True)