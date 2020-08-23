import discord
import os
import sys

from six.moves import cPickle
import tensorflow as tf
import argparse
from six import text_type
import re

sys.path.append('./char-rnn/')
from model import Model



parser = argparse.ArgumentParser(
                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--save_dir', type=str, default='save',
                    help='model directory to store checkpointed models')
parser.add_argument('-n', type=int, default=200,
                    help='number of characters to sample')
parser.add_argument('--prime', type=text_type, default=u'',
                    help='prime text')
parser.add_argument('--sample', type=int, default=1,
                    help='0 to use max at each timestep, 1 to sample at '
                         'each timestep, 2 to sample on spaces')
args = parser.parse_args()
args.save_dir = os.path.join('char-rnn/', args.save_dir)

with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
    saved_args = cPickle.load(f)
with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
    chars, vocab = cPickle.load(f)

model = Model(saved_args, training=False)

def sample(args, content):

    #Use most frequent char if no prime is given
    args.prime = content

    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            data = model.sample(sess, chars, vocab, args.n, args.prime,
                               args.sample).encode('utf-8')
            return data.decode("utf-8")

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user, flush=True)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if len(message.clean_content) >= 4 and message.clean_content[0:4] == '!say':
            start = 5
            if len(message.clean_content) >= 5 and message.clean_content[5] == ' ':
                start = 6
            content = message.clean_content[start:]
            if(content == ''):
                content = chars[0]
            async with message.channel.typing():
                output = sample(args, content)
            lines = output.split('\n')

            length = len(lines[0])
            end = 1
            while(length < 20):
                length += len(lines[end])
                end += 1

            print(lines[0:end], flush=True)

            for i in range(0, end):
                await message.channel.send(lines[i])
        elif self.user in message.mentions:
            content = message.content.replace('<@!746867040224149555>', '')
            async with message.channel.typing():
                output = sample(args, content)
            lines = output.split('\n')
            print(output, flush=True)
            await message.channel.send(output)
        else:
            #add message to training data
            traindata = open("traindata.txt", "a")
            #remove urls
            content = re.sub(r'^https?:\/\/.*[\r\n]*', '', message.clean_content)
            traindata.write(content)
            traindata.write('\n')
            traindata.close()

client = MyClient()
client.run('NzQ2ODY3MDQwMjI0MTQ5NTU1.X0GkIg.tBNjbSH7QQl63mrVMAs8g1jTgsY')