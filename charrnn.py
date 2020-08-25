
import os
import sys
from six.moves import cPickle


from six import text_type

import tensorflow as tf
sys.path.append('./char-rnn/')
from rnnmodel import RNNModel
import util
class Rnn:

    def __init__(self, dataset, length=500):
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
        self.datadir = 'char-rnn/save/' + dataset
        self.n = length
        self.sample = 2   
                            #help='0 to use max at each timestep, 1 to sample at '
                            #     'each timestep, 2 to sample on spaces')
        with open(os.path.join(self.datadir, 'config.pkl'), 'rb') as f:
            self.saved_args = cPickle.load(f)
        with open(os.path.join(self.datadir, 'chars_vocab.pkl'), 'rb') as f:
            self.chars, self.vocab = cPickle.load(f)

        self.model = RNNModel(self.saved_args, training=False)

    def predict(self, content, lines=3):
        #Use most frequent char if no prime is given
        print("input: " + content, flush=True)
        if content == '':
            content = self.chars[0]
        with tf.Session() as sess:
            tf.global_variables_initializer().run()
            saver = tf.train.Saver(tf.global_variables())
            ckpt = tf.train.get_checkpoint_state(self.datadir)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
                data = self.model.sample(sess, self.chars, self.vocab, self.n, content,
                                   self.sample).encode('utf-8')
                return self.formatText(data.decode("utf-8"), lines)

    def formatText(self, text, lines):
        text = util.removeNonAscii(text)
        print(text, flush=True)
        splitlines = text.split('\n')
        joined = '\n'.join(splitlines[0:lines])

        return self.sanitize(self.vocab, joined)

    def sanitize(self, vocab, text): # Strip out characters that are not part of the net's vocab.
        return ''.join(i for i in text if i in vocab)