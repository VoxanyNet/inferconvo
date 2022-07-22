from .inferconvo import Conversation, Message

with open("inferkit_key.txt", "r") as file:
	key = file.read().replace("\n","")

conversation = Conversation(key)

user_name = input("Enter your name: ")
bot_name = input("Enter bot's name: ")

while True:
	user_input = input(f"{user_name}: ")

	print("\n")

	user_message = Message(user_name, user_input)

	conversation.add_message(user_message)

	bot_message = conversation.generate_message(bot_name)

	print(f"{bot_message.author}: {bot_message.text}")

	print("\n")
