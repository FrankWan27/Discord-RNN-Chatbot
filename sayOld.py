import discord
import re
import util
from charrnn import Rnn

class MyClient(discord.Client):
    async def on_ready(self):
        print('!say Ready! ', self.user, flush=True)

    async def on_message(self, message):
        # don't respond to ourselves

        if message.author == self.user:
            return

        if re.match(r'^!say', message.clean_content):
            content = util.removeNonAscii(message.clean_content[4:])
            content = util.removeLeadSpaces(content)
            async with message.channel.typing():
                output = alphabet.predict(content)

            await message.channel.send(output)

alphabet = Rnn('newdata')
client = MyClient()
client.run(util.token)