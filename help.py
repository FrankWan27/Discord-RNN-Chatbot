import discord
import re
import util

class MyClient(discord.Client):
    async def on_ready(self):
        print('!help Ready! ', self.user, flush=True)


    async def on_message(self, message):
        # don't respond to ourselves
        
        if message.author == self.user:
            return

        if re.match(r'^!help', message.clean_content):
            output = "```Current supported commands: \n\n!shakespeare [# of lines (optional, default = 10)] [seed (optional)]\n!say [seed (optional)]\n!train (returns current size of training data)```"

            await message.channel.send(output)

client = MyClient()
client.run(util.token)