import requests

from .errors import NoTokenError, CharacterLimitExceeded
from .message import Message

class Conversation:
    def __init__(self, token = None, relationship = "friend", url = "https://api.inferkit.com/v1/models/standard/generate"):

        self.url = url

        if not token:
            raise NoTokenError("No token has been supplied")

        self.token = token

        # A list of message objects
        self.context = []

        # Attached to the top to tell the AI that this is a text conversation
        self.heading = "A text conversation: "

    # Add a message to history, giving the AI more context
    def add_message(self, message):

        self.context.append(message) # This whole function might be kinda useless, but it makes it so you dont need to interact with context at all


    # Request the AI to generate a message object from the specified sender
    def generate_message(self, author_to_generate, add_to_context = True):

        prompt_string = self._generate_prompt_string(author_to_generate)
        raw_generated_text = self._request_new_text(prompt_string)
        generated_text = self._parse_response(raw_generated_text)

        generated_message = Message(author = author_to_generate, text = generated_text)

        if add_to_context:
            self.context.append(generated_message)

        return generated_message

    # Construct prompt string from context
    def _generate_prompt_string(self, author_to_generate):
        prompt_string = ""

        # Add the heading
        prompt_string += f"{self.heading}\n"

        # For every message in context, we add it to the string
        for message in self.context:

            prompt_string += f"{message.author}: {message.text}\n"

        # Encourage the AI to generate a message from that author
        prompt_string += f"{author_to_generate}: "

        if len(prompt_string) > 3000:
            raise CharacterLimitExceeded(f"Your context generates too many characters ({len(prompt_string)})")

        return prompt_string

    # Send the request to the AI
    def _request_new_text(self, prompt_string):

        # Prompt json object
        prompt = {
            "text": prompt_string
        }

        response = requests.post(

            url = self.url,

            json = {
                "prompt": prompt,
                "length": 100 # This is the minimum number of characters the API will charge you for
            },

            headers = {
                "Authorization" : f"Bearer {self.token}"
            }
        )

        raw_generated_text = response.json()["data"]["text"]

        return raw_generated_text

    # Parse the generated text and return only a single line of text representing the generated message for one user
    def _parse_response(self, raw_generated_text):

        # This could be cleaned up and clarified
        generated_text = raw_generated_text.split("\n")[0] # Chop off any of the extra lines the AI generates.

        return generated_text
