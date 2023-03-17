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
            messages = [{"role": "user", "content": message.content}]

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=messages
            )

            assistant_response = response["choices"][0]["message"]['content']
            await message.reply(assistant_response)

client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)