import discord
import re
import sys
sys.path.append('./chatbot-rnn/')
import chatbot
import util

class MyClient(discord.Client):
    async def on_ready(self):
        print('@Mention ready! ', self.user, flush=True)


    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if self.user in message.mentions:
            content = message.content.replace('<@!746867040224149555>', '')
            print("input: " + content, flush=true)
            async with message.channel.typing():
                chatbot.sendline(content)
                chatbot.expect('>')
                print(chatbot.before, flush=True)
            lines = chatbot.before.split('\n')
            print(lines, flush=True)
            await message.channel.send(lines[1])

rnn = chatbot.main()
client = MyClient()
client.run(util.token)