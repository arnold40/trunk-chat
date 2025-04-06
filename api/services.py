import os
import json
import uuid
import logging
from dotenv import load_dotenv
from openai import OpenAI
from .models import User, UserFavFood

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class GPTClient:
    """Handles communication with OpenAI GPT models."""

    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key)

    def ask_question(self, system_prompt, user_content, response_format=None):
        """Sends a prompt to OpenAI and returns the response."""
        try:
            response = self.client.responses.create(
                model="gpt-4o",
                input=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                text=response_format
            )
            return response.output_text
        except Exception as e:
            logger.error(f"Error in OpenAI request: {e}")
            return None


class FoodSimulationService:
    """Simulates user favorite food preferences using GPT-generated responses."""

    def __init__(self):
        logger.info("Initializing GPT clients...")
        self.gpt_asker = GPTClient()
        self.gpt_responder = GPTClient()

    def generate_fav_foods(self):
        """Generates a simulated favorite food list from AI interaction."""

        # First AI asks the question
        asker_prompt = "You are ChatGPT A. Your only task is to ask a question. Do not answer. Ask: What are your top 3 favorite foods?"
        asker_content = ""
        question = self.gpt_asker.ask_question(asker_prompt, asker_content)

        if not question:
            logger.error("Failed to generate question for food simulation.")
            return None

        logger.info(f"Generated question: {question}")

        # Second AI responds dynamically with three random foods
        responder_prompt = "You are ChatGPT B. Respond with three random food items. Also indicate if they are vegetarian or not."
        json_format = {
            "format": {
                "type": "json_schema",
                "name": "user_fav_food",
                "schema": {
                    "type": "object",
                    "properties": {
                        "foods": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string"
                                    },
                                    "is_veggie": {
                                        "type": "boolean"
                                    }
                                },
                                "additionalProperties": False,
                                "required": ["name", "is_veggie"]
                            }
                        }
                    },
                    "required": ["foods"],
                    "additionalProperties": False
                }
            }
        }
        response = self.gpt_responder.ask_question(responder_prompt, question, json_format)

        if not response:
            logger.error("Failed to generate favorite foods response.")
            return None

        logger.info(f"Received favorite foods: {response}")

        try:
            food_data = json.loads(response)
            return food_data.get("foods", [])
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON response from GPT.")
            return None

    def simulate_user_fav_food(self):
        """Creates a simulated user with their favorite foods in the database."""
        favorite_foods = self.generate_fav_foods()

        if not favorite_foods:
            logger.warning("No favorite foods generated. Skipping database entry.")
            return None

        user_id = uuid.uuid4()
        user_name = f"User {user_id}"

        try:
            user = User.objects.create(name=user_name, is_vegetarian=False)
            for food in favorite_foods:
                UserFavFood.objects.create(
                    user=user,
                    food_name=food["name"],
                    is_veggie=food["is_veggie"]
                )

            logger.info(f"Created user {user_name} with favorite foods: {favorite_foods}")
            return user

        except Exception as e:
            logger.error(f"Failed to create User and their favorite foods: {e}")
            return None
