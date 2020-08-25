import discord
import re
from charrnn import Rnn
import util

class MyClient(discord.Client):
    async def on_ready(self):
        print('!shakespeare Ready! ', self.user, flush=True)


    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if re.match(r'^!shakespeare', message.clean_content):
            lines = 10
            content =  message.clean_content[12:]
            z = re.match(r'^ *[0-9]+', content)
            if z:
                lines = z.group(0)
                content = content[len(lines):]
            content = util.removeNonAscii(content)
            content = util.removeLeadSpaces(content)
            #content = re.sub(r'[^a-zA-Z \']*', '', content)
            async with message.channel.typing():
                output = shakespeare.predict(content, int(lines))

            await message.channel.send(output)

shakespeare = Rnn('shakespeare')
client = MyClient()
client.run(util.token)