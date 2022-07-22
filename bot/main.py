import discord
from inferconvo import Conversation, Message

with open("bot_token.txt", "r") as file:
    BOT_TOKEN = file.read()

with open("inferkit_token.txt", "r") as file:
    INFERKIT_TOKEN = file.read().replace("\n", "")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents = intents)

bot.conversations = {}

@bot.event
async def on_message(message):
    if not message.reference: # If this is not a reply
        return

    if message.author.id == bot.user.id: # If the bot is replying to itself, we dont want it to do anything
        return

    if message.reference.resolved.author.id != bot.user.id: # If the reply isnt to the bot
        return

    if message.author.id not in bot.conversations: # If there is not an existing conversation with this user
        await message.reply(f"<@!{message.author.id}> does not have an existing conversation.")
        return

    await message.channel.trigger_typing()

    conversation = bot.conversations[message.author.id]

    # Add the reply to the conversation
    user_reply = Message(message.author.name, message.content)

    conversation.add_message(user_reply)

    bot_message = conversation.generate_message(author_to_generate = bot.user.display_name)

    await message.reply(bot_message.text)

    return

@bot.event
async def on_reaction_add(reaction, user): # Force the bot to send the next message
    if reaction.message.author.id != bot.user.id:
        return

    if reaction.emoji != "▶️":
        return

    print("hello")

    if user.id not in bot.conversations: # If there is not an existing conversation with this user
        await reaction.message.channel.send(f"<@!{message.author.id}> does not have an existing conversation.")

        return

    conversation = bot.conversations[user.id]

    await reaction.message.channel.trigger_typing()

    bot_message = conversation.generate_message(author_to_generate = bot.user.display_name)

    await reaction.message.reply(bot_message.text)

@bot.slash_command(description = "Begin a conversation with the bot")
async def talk(ctx, relationship:str = "friend"):

    # Create a new conversation for this user
    new_conversation = Conversation(token = INFERKIT_TOKEN)

    new_conversation.heading = f"A text conversation between {bot.user.display_name} and their {relationship} {ctx.user.name}"

    bot.conversations[ctx.author.id] = new_conversation

    await ctx.respond(f"Started a new conversation between <@!{ctx.author.id}> and their {relationship} {bot.user.display_name}.\n\nReply to this message to begin conversation. ")

@bot.slash_command(description="Infer what the user would say in this context", guild_ids=[761789274512425001])
async def infer(ctx, user = None) -> None:
    await ctx.channel.trigger_typing()

    # Fetch the user we are trying to generate a fake message from
    user_id = int(
        user.replace("<@!", "").replace(">", "")
    )

    author_to_generate = await bot.fetch_user(user_id)

    author_to_generate = author_to_generate.name

    # Retrieve messages
    messages = await ctx.channel.history(limit=75).flatten()

    # Convert discord message objects and add them to context
    for message in messages:
        infer_message = Message(message.author.name, message.content)

        conversation.add_message(infer_message)

    boing = conversation._generate_prompt_string(author_to_generate)

    print(boing)

    #generated_message = conversation.generate_message(author_to_generate)

    #rint(generated_message.text)

    #await ctx.defer()

    #await ctx.respond(f"{generated_message.author} said {generated_message.text}")



bot.run(BOT_TOKEN)
