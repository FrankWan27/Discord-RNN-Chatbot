import discord
import os
import sys

from six.moves import cPickle
import tensorflow as tf
import argparse
from six import text_type
import re
import wexpect

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user, flush=True)
        chatbot.expect('>')
        print('chatbot ready', flush=True)
        rnn.expect('>')
        print('rnn ready', flush=True)


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
        else:
            #add message to training data
            traindata = open("traindata.txt", "a")
            #remove urls
            content = re.sub(r'^https?:\/\/.*[\r\n]*', '', message.clean_content)
            traindata.write(content)
            traindata.write('\n')
            traindata.close()

chatbot = wexpect.spawn('python ./chatbot-rnn/chatbot.py')
rnn = wexpect.spawn('python ./char-rnn/sample.py')
client = MyClient()
client.run('NzQ2ODY3MDQwMjI0MTQ5NTU1.X0GkIg.tBNjbSH7QQl63mrVMAs8g1jTgsY')