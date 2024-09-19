# 🍽️ RecipeIQ Chatbot

**RecipeIQ** is an intelligent chatbot that helps users find recipes based on ingredients they have on hand. Powered by **Dialogflow** for natural language understanding, **Flask** for webhook fulfillment, and **Spoonacular API** for fetching recipe data, this project demonstrates an end-to-end solution integrating AI, APIs, and databases (MongoDB) for personalized recipe recommendations.

---

## 🌟 Features

- **Natural Language Understanding**: The chatbot uses **Dialogflow** to interpret users' intent and extract relevant information like ingredients and meal types.
- **Ingredient-Based Recipe Search**: Users can input a list of ingredients (e.g., "Find a recipe with salmon, garlic, and lemon for lunch"), and the bot will return relevant recipes.
- **Detailed Recipe Information**: For each recipe, the chatbot provides detailed information including preparation time, servings, ingredients, and cooking instructions.
- **Persistent Storage with MongoDB**: Recipes are cached in a **MongoDB** database to optimize subsequent queries, reducing API calls and improving performance.
- **Spoonacular API Integration**: Real-time integration with the **Spoonacular API** ensures fresh and varied recipe suggestions.

---

## 🛠️ Tech Stack

- **Natural Language Processing**: [Dialogflow](https://dialogflow.cloud.google.com/)
- **Backend Framework**: [Flask](https://flask.palletsprojects.com/)
- **Database**: [MongoDB](https://www.mongodb.com/)
- **External API**: [Spoonacular API](https://spoonacular.com/food-api)
- **Hosting**: [Heroku](https://www.heroku.com/) or any cloud provider

---

## 🎯 Project Goals

This project was built to demonstrate the following core skills:

1. **AI & Natural Language Understanding**: Building chatbots using Dialogflow, understanding intents and entities, and creating meaningful, conversational user interactions.
2. **API Integration**: Fetching and managing external data (e.g., recipes) using the Spoonacular API, handling multiple requests efficiently.
3. **Database Design & Optimization**: Using MongoDB for data caching and querying to improve performance and reduce redundant API calls.
4. **Full-Stack Development**: Building a full-stack AI-powered application, from the chatbot interface to API integration and database storage.
5. **Python Programming**: Utilizing Python to handle server-side logic, API requests, and data processing in Flask.

---

## ⚙️ Installation & Setup

To get the project up and running locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Ronney221/RecipeIQ
   cd recipe-finder-ai-chatbot
    ```
2. **Create and Activate a Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. **Install the Dependencies**:
    
    ```bash
    pip install -r requirements.txt
    ```
4. **Set Up Environment Variables:**
    
    Create a .env file in the root directory and add the following:
    
    ```bash
    SPOONACULAR_API_KEY=your_spoonacular_api_key
    MONGODB_URI=your_mongodb_connection_string
    ```
5. **Start the Flask Server:**
    
   ```bash
   flask run
   ```
6. **Connect to Dialogflow:**
    
   - Create a Dialogflow agent and link it to your local Flask server via a webhook (using ngrok or a cloud service like Heroku).
   - Ensure your agent’s intents are configured to call the webhook for fulfillment.
   
    
7. **Test the Bot:**

    - Use the Dialogflow test console or a platform integration (e.g., Google Assistant or Facebook Messenger) to interact with the bot.

## 📚 API Documentation

This project uses the **Spoonacular API** to fetch recipes based on the user's ingredients and meal preferences. Here's how the integration works:

- **Recipe Search**: The bot calls the `/recipes/complexSearch` endpoint to search for recipes based on ingredients provided by the user.
- **Detailed Recipe Info**: After getting basic recipe results, the bot uses `/recipes/{id}/information` to retrieve detailed information about each recipe, such as ingredients, instructions, and nutrition.

---

## 🗃️ MongoDB Integration

The project uses **MongoDB** to cache recipes and reduce redundant API calls. When a user searches for a recipe, the bot:

1. First checks the MongoDB database to see if there are any matching recipes.
2. If not, it fetches fresh data from the Spoonacular API and stores it in MongoDB for future use.

MongoDB is a key part of optimizing this system, reducing API costs, and improving response times for users.

---

## 🌍 Deployment

You can deploy this project on cloud platforms like **Heroku**, **AWS**, or **Google Cloud**.

**Example Deployment on Heroku**:

1. **Set up a Heroku app and push the code:**

   ```bash
   git push heroku main
    ```
2. **Configure environment variables (`SPOONACULAR_API_KEY`, `MONGODB_URI`) using:**

    ```bash
    heroku config:set SPOONACULAR_API_KEY=your_spoonacular_api_key
    heroku config:set MONGODB_URI=your_mongodb_connection_string
   ```
3. **Ensure your Flask server is running and connected to your Dialogflow agent’s webhook.**
    
---

## 🚀 Features to Add Next

- **User Authentication**: Implement user authentication (e.g., OAuth) to save favorite recipes and personalize recommendations.
- **Nutritional Filters**: Allow users to filter recipes based on dietary preferences (e.g., vegan, gluten-free, keto).
- **Voice Integration**: Integrate the chatbot with voice assistants like **Google Assistant** for hands-free cooking assistance.
- **Enhanced Caching Strategy**: Implement cache expiration policies in MongoDB to refresh older recipes automatically.

---

## 🧑‍💻 Why This Project Stands Out

- **Full-Stack AI Integration**: Combines natural language understanding, third-party APIs, and databases to deliver a seamless, personalized experience.
- **Efficient Data Handling**: Shows optimization techniques using MongoDB for caching and reducing API usage.
- **Scalable Architecture**: Built with scalability in mind, making it easy to expand and add new features as the product evolves.

---

## 📧 Contact

Interested in collaborating or learning more about this project? Feel free to reach out!

- **Email**: [ronney@cs.washington.edu](mailto:ronney@cs.washington.edu)
- **LinkedIn**: [Ronney Do](https://www.linkedin.com/in/ronneydo/)
- **GitHub**: [github.com/ronney221](https://github.com/ronney221)

---

## 👏 Contributions

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/recipe-finder-ai-chatbot/issues) or submit a pull request.

---

## Project Screenshots

![avocados1](https://github.com/user-attachments/assets/fb54e197-b039-4f85-8a67-cda65b0afaf0)![avocados2](https://github.com/user-attachments/assets/b79cada3-3807-4fca-b414-e79b67db0bb3)![avocados3](https://github.com/user-attachments/assets/ad292f22-de02-4f8a-a7e0-442f9286d1ff)


![breakfast1](https://github.com/user-attachments/assets/3e27b71c-e73a-4cb8-90f4-079c73428ffc)![breakfast2](https://github.com/user-attachments/assets/3ce51e6b-e654-4206-a480-38a1619221bc)![breakfast3](https://github.com/user-attachments/assets/c9056eaf-c641-40ed-b576-e32f5c73bf0f)



