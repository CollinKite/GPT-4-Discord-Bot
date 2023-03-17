import os
import discord
import openai
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

class ChatBot(discord.Client):
    async def on_ready(self):
        print(f'We have logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # If a message mentions the bot, then reply
        if self.user.mentioned_in(message):
            # Get previous messages
            messages = []

            #loop through previous 20 messages between the bot and the user, and add them to the messages list only if the message is from the user mentioning the bot or if the message is from the bot replying to the user
            async for msg in message.channel.history(limit=20):
                if msg.author == self.user and message.author.mentioned_in(msg):
                    messages.insert(0, {"role": "assistant", "content": msg.content})
                elif self.user.mentioned_in(msg):
                    messages.insert(0, {"role": "user", "content": msg.content})

            #Add Bot Instructions
            messages.insert(0, {"role": "system", "content": "You are talking to a GPT-4 chatbot. The chatbot is very friendly and helpful"})


            # Send the messages to OpenAI to get a response
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )

            assistant_response = response["choices"][0]["message"]['content']
            await message.reply(assistant_response)

client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)