import requests
from bs4 import BeautifulSoup
import discord
import re
import util
from charrnn import Rnn
import sched, time
from discord.ext import tasks

#bypass captcha
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,'referer':'https://www.google.com/'}
giantURL = 'https://giantfoodsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory'
cvsURL = 'https://www.cvs.com/immunizations/covid-19-vaccine?icid=coronavirus-lp-nav-vaccine'

def getGiant():
    response = requests.get(giantURL, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    apptInfo = soup.find(id='divApptTypeInfo0')
    if apptInfo is not None:
        return apptInfo.text
    return 'Text not found error'

def getCVS():
    response = requests.get(cvsURL, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    apptInfo = soup.findAll(class_='text aem-GridColumn aem-GridColumn--default--12')
    found = False
    for appt in apptInfo:
        if 'At this time, all appointments in Massachusetts are booked. We’ll add more as they become available. Please check back later.' in appt.text:
            found = True
    if found:
        return 'Massachusetts vaccines are NOT available from CVS'
    
    return 'Text changed somehow, vaccines might be available!'

class MyClient(discord.Client):
    @tasks.loop(seconds=30)
    async def checkGiant(self): 
        text = getGiant()
        if text != '\nThere are currently no COVID-19 vaccine appointments available. Please check back later. We appreciate your patience as we open as many appointments as possible. Thank you.\n':
            await self.get_channel(415398356613857283).send('There was a change at https://giantfoodsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory\n' + text)   
        else:
            await self.get_channel(415398356613857283).send('No change at https://giantfoodsched.rxtouch.com/rbssched/program/covid19/Patient/Advisory\n' + text)
  
    @tasks.loop(seconds=30)
    async def checkCVS(self): 
        text = getCVS()
        if text != 'Massachusetts vaccines are NOT available from CVS':
            await self.get_channel(826174048215498772).send('There was a change at https://www.cvs.com/immunizations/covid-19-vaccine?icid=coronavirus-lp-nav-vaccine\n' + text)   
        # else:
        #     await self.get_channel(826174048215498772).send('No change at https://www.cvs.com/immunizations/covid-19-vaccine?icid=coronavirus-lp-nav-vaccine\n' + text)

    async def on_ready(self):
        print('!check Ready! ', self.user, flush=True)
        #self.checkGiant.start()
        self.checkCVS.start()

    async def on_message(self, message):
        # don't respond to ourselves

        if message.author == self.user:
            return

        if re.match(r'^!check', message.clean_content):
            content = util.removeNonAscii(message.clean_content[6:])
            content = util.removeLeadSpaces(content)
            content = content.lower()
            async with message.channel.typing():
                if 'giant' in content:
                    output = getGiant()
                elif 'cvs' in content:
                    output = getCVS()
                else:
                    output = 'Unknown website, currently only supporting `!check cvs` and `!check giant`'

            await message.channel.send(output)

client = MyClient()
client.run(util.token)




