import discord
import re
import util
import os
import openai

openai.api_key = 'sk-RE5GV2cF8sx3zbdOWq1' + 't5eW9cfPGDRAL6Ey2Q6xs'

promptBase = "The following is a conversation with an AI assistant. The assistant is "

def createPrompt(prompt, personality):
    return promptBase + personality + ".\nHuman: " + prompt + "\nAI: "

def getResponse(prompt, personality): 
    response = openai.Completion.create(
        engine="curie",
        prompt= createPrompt(prompt, personality),   
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    print(createPrompt(prompt, personality), flush=True)
    return response.choices[0].text


class MyClient(discord.Client):

    async def on_ready(self):
        print('!say openai Ready! ', self.user, flush=True)
        self.personality = "clever and friendly"


    async def on_message(self, message):
        # don't respond to ourselves

        if message.author == self.user:
            return

        if re.match(r'^!personality', message.clean_content):
            content = util.removeNonAscii(message.clean_content[12:])
            content = util.removeLeadSpaces(content)
            if content != "":
                self.personality = content
            await message.channel.send("I am " + self.personality)

        elif re.match(r'^!say', message.clean_content):
            content = util.removeNonAscii(message.clean_content[4:])
            content = util.removeLeadSpaces(content)
            async with message.channel.typing():
                output = getResponse(content, self.personality)
            await message.channel.send(output)


client = MyClient()
client.run(util.token)