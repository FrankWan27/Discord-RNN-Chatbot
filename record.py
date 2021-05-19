import discord
import re
import util
import os

class MyClient(discord.Client):
    async def on_ready(self):
        print('Recording Ready! ', self.user, flush=True)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        
        if re.match(r'^!train', message.clean_content):
            size = util.formatBytes(os.path.getsize('./traindata.txt'))
            await message.channel.send('Training data is currently at ' + size)
        elif re.match(r'^!help', message.clean_content):
            return
        elif re.match(r'^!shakespeare', message.clean_content):
            return
        elif re.match(r'^!say', message.clean_content):
            return
        elif re.match(r'^-rate', message.clean_content):
            return
        elif re.match(r'^!check', message.clean_content):
            return
        elif re.match(r'^\.', message.clean_content):
        	return
        elif re.match(r'^>', message.clean_content):
            return
        elif self.user in message.mentions:
            return
        elif not util.checkBot(message.channel.name):
            #add message to training data
            #remove urls
            content = util.removeURLs(message.clean_content)
            #remove emotes
            content = util.removeEmotes(content)            
            #remove non ascii 
            content = util.removeNonAscii(content)

            if content != '':
                traindata = open("traindata.txt", "a")
                traindata.write(content)
                traindata.write('\n')
                traindata.close()

client = MyClient()
client.run(util.token)