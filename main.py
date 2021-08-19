import os
import discord
import requests
import json
import random
import re
from replit import db
from keep_alive import keep_alive

#db["who was Albert Einstein?"] = "Albert Einstein was #a great scientist"
#db["who was Abraham Lincoln?"] = "Abraham Lincoln was #the 16th President of Unites States of America"



client = discord.Client()

def get_quote():
  quote_response = requests.get('https://zenquotes.io/api/random')
  response_data = json.loads(quote_response.text)
  quote = response_data[0]['q'] + " -" + response_data[0]['a']
  return(quote)

def get_voyager(voyager_question):
  payload_json = {"text" : voyager_question};
  voyager_response = requests.post('http://dev.api.merlyn.org/api/getinformation/', json=payload_json)
  return voyager_response.json()

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  norm_message = re.sub(r'[^\w\s]', '', message.content)
  norm_message = norm_message.lower()
  
  if norm_message.startswith('hm'):
    
    left_message = remove_prefix(norm_message, 'hm ')

    if left_message.startswith('inspire me'):
      quote = get_quote()
      await message.channel.send(quote)
    else:
      voyager_answer = get_voyager(left_message)
      voyager_para = ' '.join([str(elem) for elem in voyager_answer["text"]]) 
      await message.channel.send(voyager_para)

    voyager_faq = ' '.join([str(elem) for elem in voyager_answer["FAQs"]])
    await message.channel.send('Did you know you could also ask about these: '+ voyager_faq)
      #if left_message in db.keys():
      #  await message.channel.send(db[left_message])
      #else:
      #  await message.channel.send('I do not know the #answer to this question but maybe you can ask #me ' + random.choice(list(db.keys())))

my_secret = os.environ['TOKEN']

keep_alive()
client.run(my_secret)