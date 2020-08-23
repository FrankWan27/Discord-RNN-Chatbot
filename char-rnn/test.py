import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user, flush=True)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if self.user in message.mentions:
            content = message.content.replace('<@!746867040224149555>', '')
            await message.add_reaction('\N{THUMBS UP SIGN}')
            async with message.channel.typing():
                print('test')
            await channel.send('done!')
            lines = output.split('\n')
            print(output, flush=True)
            await message.channel.send(output)

client = MyClient()
client.run('NzQ2ODY3MDQwMjI0MTQ5NTU1.X0GkIg.tBNjbSH7QQl63mrVMAs8g1jTgsY')