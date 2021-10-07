
import os
import discord
import requests
import json
import random
import asyncio
import re
from replit import db
from keep_alive import keep_alive
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pickle
import pandas as pd
from google.auth.transport.requests import Request
import ast
import google.oauth2.credentials
#import discord_slash
from discord.ext import commands
from discord import ActionRow, Button, ButtonStyle
from datetime import datetime, timedelta
import time
import calendar
#import flair
#from flair.models import TextClassifier
#from flair.data import Sentence
#from discord_slash.utils import manage_components
#from discord_slash.model import ButtonStyle
#from discord_buttons import DiscordButton, Button, ButtonStyle, InteractionType
#from tkinter import *
#Creating a win
#win = Tk()
#Creating The Button

#db["who was Albert Einstein?"] = "Albert Einstein was #a great scientist"
#db["who was Abraham Lincoln?"] = "Abraham Lincoln was #the 16th President of Unites States of America"



client = discord.Client()
#client = commands.Bot(command_prefix='!')
embed = discord.Embed()
embed2 = discord.Embed()
embed_fb = discord.Embed()
embed_ok = discord.Embed()
#db1 = DiscordButton(client)

ext=0

#channel: ComponentContext=await manage_components.wait_for_component(client, components=action_row)

def get_quote():
  quote_response = requests.get('https://zenquotes.io/api/random')
  response_data = json.loads(quote_response.text)
  quote = response_data[0]['q'] + " - " + response_data[0]['a']
  return(quote)

def get_voyager(voyager_question):
  payload_json = {"text" : voyager_question};
  voyager_response = requests.post('http://dev.api.merlyn.org/api/getinformation/', json=payload_json)
  return voyager_response

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def get_jokes():
  joke_response = requests.get('https://icanhazdadjoke.com/', headers = {"Accept": "text/plain"})
  return joke_response.text

def is_command (msg): # Checking if the message is a command call
  if len(msg.content) == 0:
    return False
  elif msg.content.split()[0] == 'scan':
    return True
  else:
    return False

def predict(sentence):
    """ Predict the sentiment of a sentence """
    classifier = TextClassifier.load('en-sentiment')
    if sentence == "":
        return 0
    text = Sentence(sentence)
    # stacked_embeddings.embed(text)
    classifier.predict(text)
    value = text.labels[0].to_dict()['value'] 
    if value == 'POSITIVE':
        result = text.to_dict()['labels'][0]['confidence']
    else:
        result = -(text.to_dict()['labels'][0]['confidence'])
    return round(result, 3)

'''def process_response(voyager_resp,left,message):
  if voyager_resp.status_code == 500:
    await message.channel.send("That is NOT acceptable!")
  elif voyager_resp.status_code == 200:
    voyager_answer = voyager_resp.json()
    failed_answers=['No short answer available','?','Wolfram|Alpha did not understand your input','No response']
    sources=voyager_answer['source']
    answers=voyager_answer['text']
    source_answer_map={}
    for i in range(0,len(sources)):
      if answers[i] not in failed_answers:
        source_answer_map[sources[i]]=answers[i]
    voyager_para = '\n'.join(["Answer from "+str(k)+" : "+str(source_answer_map[k]) for k in source_answer_map.keys()])

    await message.channel.send(voyager_para)

    voyager_faq = '\n'.join([str(elem) for elem in voyager_answer["FAQs"]])

    request = youtube.search().list(part="snippet", q=left)
    response = request.execute()

    await message.channel.send("Check out this youtube video: %s"%("https://www.youtube.com/watch?v="+response['items'][0]['id']['videoId']))

    await message.channel.send('Did you know you could also ask about these:')

    faq=voyager_answer["FAQs"]
    for q in range(0,len(faq[:2])):
      await message.channel.send(faq[q])

  else:
        await message.channel.send("Sorry I cannot help you now, can we try later?")'''





@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

'''@client.command(name='buttons', description='sends you some nice Buttons')
async def buttons(ctx: commands.Context,s):
  components = [ActionRow(Button(label=s,custom_id='option1',style=ButtonStyle.green))]
  an_embed = discord.Embed()
  msg = await ctx.send(embed=an_embed, components=components)

  def _check(i: discord.Interaction, b):
    return i.message == msg and i.member == ctx.author
  interaction, button = await client.wait_for('button_click', check=_check)
  button_id = button.custom_id
  await interaction.defer()
  await interaction.edit(embed=an_embed.add_field(name='Choose', value=f'Your Choose was `{button_id}`'),
  components=[components[0].disable_all_buttons(), components[1].disable_all_buttons()])'''

'''@client.command(pass_context=True)
async def test(ctx):
    #await client.wait_until_ready()
    channel = client.get_channel(876753113070043166)
    await channel.send('Hi @RKbotman, the sentiment seems to be negative in the student room. You may want to have a look')
    #await member.create_dm()
    #await member.channel.send('Hi @RKbotman, the sentiment seems to be negative in the student room. You may want to have a look')'''


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  #print(tmp)
  teacher_id = 877816065718116352
  student_id = 887920154984448010
  general_id = 877816065718116352
  #msg = discord.utils.get(await channel.history(limit=2).flatten(), author=client.user)
  #msg = await channel.fetch_message(channel.last_message_id)
  #msg = await client.get_channel(general_id).history(limit=2).flatten()
  #channel=client.get_channel(general_id)
  #msg1 = await channel.fetch_message(msg[1].id)
  #text=msg1.content
  #print(text)
  #logs = client.logs_from(message.channel, limit=2)
  #tmp = yield from client.send_message(message.channel, 'Collecting messages...')
  #for msg in logs:
    #print(msg.content)
  #yield from client.edit_message(tmp, 'messages successfully collected')

  norm_message = re.sub(r'[^\w\s]', '', message.content)
  norm_message = norm_message.lower()

  if norm_message.split()[0]=='scan':
    data = pd.DataFrame(columns=['content', 'time', 'author'])
    async for msg in message.channel.history(limit=10000): # As an example, I've set the limit to 10000
      if msg.author != "XXX":
        if not is_command(msg):  
          print(msg.content,msg.created_at,msg.author.name)
          data = data.append({'content': msg.content,'time': msg.created_at,'author': msg.author.name},ignore_index=True)
          if len(data) == 100:
            break
    file_location = "data.csv" # Set the string to where you want the file to be saved to
    data.to_csv(file_location)

  elif re.search('you should have allowed me to ask', norm_message) or re.search("i do not care", norm_message) or re.search('this is not done', norm_message):

    #member="general"
    #valid_ids=["general","Merlyn_Bot"]
    #for channel in member.server.channels:
      #if str(channel)=="Ayan_Bhowmick":
        #await client.send_message("Hi @RKbotman, the sentiment seems to be negative in the student room. You may want to have a look")
      #for guild in client.guilds:
       # print(f'{client.user} is connected to the following guild:\n'
      #f'{guild.name}(id: {guild.id})\n')

      #members = '\n - '.join([member.name for member in guild.members])
      #print(f'Guild Members:\n - {members}')
      #for member in guild.members:
       # if str(member.name)=="Ayan_Bhowmick":
      #client.loop.create_task(test(message))
      #channel = client.channels.cache.find("Ayan_Bhowmick")
      #channel.send("Hi @RKbotman, the sentiment seems to be negative in the student room. You may want to have a look")
      #await client.channels.cache.get("876753113070043166").send("Hi @RKbotman, the sentiment seems to be negative in the student room. You may want to have a look")
      #print("Sentiment=",predict(norm_message))
      channel=client.get_channel(teacher_id)
      time.sleep(3)
      await channel.send("Hi @"+channel.name+", the sentiment seems to be negative in the student room. You may want to have a look")
      #break
  
  elif norm_message.startswith('hm') or norm_message.startswith('hey merlyn'):
    
    if norm_message.startswith('hm'):
      left_message = remove_prefix(norm_message, 'hm ')
    else:
      left_message = remove_prefix(norm_message, 'hey merlyn ')
      
    options=["Liquid to Gas","Solid to Gas","Liquid to Solid","Gas to Liquid"]

    if left_message.startswith('inspire me') or re.search('feeling low', left_message) or re.search('feeling very low', left_message):
      quote = get_quote()
      await message.channel.send("Let me try to inspire you with a quote:\n"+quote)
      #if re.search('feeling low', left_message) or re.search('feeling very low', left_message):
      channel=client.get_channel(teacher_id)
      time.sleep(3)
      await channel.send("Hi @"+channel.name+", you may want to keep an eye on "+str(message.author)+". He said the following: "+str(message.content))
    elif message.channel.id==teacher_id and left_message.startswith('please run through this for preparation of lesson'):
      time.sleep(4)
      channel=client.get_channel(teacher_id)
      await channel.send("Worksheet ingested for preparation tonight")
      channel=client.get_channel(student_id)
      time.sleep(3)
      await channel.send("Hi @"+channel.name+", you have a preparation worksheet for the lesson on water cycle. Let us go through it together")
    elif left_message.startswith('evaporation is liquid to gas') or left_message.startswith('condensation is gas to liquid'):
      #for msg in message.channel.history(limit=2):
      time.sleep(2)
      await message.channel.send("Excellent! You know your stuff.")
      time.sleep(3)
      if left_message.startswith('evaporation'):
        text='What is condensation?'+'\n\n(a) '+options[0]+'      (b) '+options[1]+'\n\n(c) '+options[2]+'\t\t\t\t\t\t\t\t(d) '+options[3]
        embed2.description=text
        time.sleep(3)
        await message.channel.send(embed=embed2)
      else:
        channel=client.get_channel(teacher_id)
        await channel.send("Here is the statistics for the preparation worksheet attempts from last night")
        time.sleep(1)
        await channel.send(file=discord.File('prep_stats.png'))
    elif left_message.startswith('i understood what is condensation'):
      text='What is condensation?'+'\n\n(a) '+options[0]+'      (b) '+options[1]+'\n\n(c) '+options[2]+'\t\t\t\t\t\t\t\t(d) '+options[3]
      embed2.description=text
      time.sleep(2)
      await message.channel.send(embed=embed2)
    elif left_message.startswith('evaporation is'):
      #for msg in message.channel.history(limit=2):
      request = youtube.search().list(part="snippet", q="evaporation")
      response = request.execute()
      #await message.channel.send("Not really. Evaporation is liquid to gas. You may want to look at the material linked below. Tell me when you are ready: %s"%("https://www.youtube.com/watch?v="))
      time.sleep(2)
      await message.channel.send("Not really. Evaporation is liquid to gas. You may want to look at the material linked below. Tell me when you are ready: %s"%("https://www.youtube.com/watch?v="+response['items'][0]['id']['videoId']))
    elif left_message.startswith('condensation is'):
      #for msg in message.channel.history(limit=2):
      request = youtube.search().list(part="snippet", q="condensation")
      response = request.execute()
      time.sleep(2)
      await message.channel.send("Not really. Condensation is gas to liquid. You may want to look at the material linked below. Tell me when you are ready: %s"%("https://www.youtube.com/watch?v="+response['items'][0]['id']['videoId']))
      channel=client.get_channel(teacher_id)
      time.sleep(3)
      await channel.send("Here is the statistics for the preparation worksheet attempts from last night")
      await channel.send(file=discord.File('prep_stats.png'))
      #await message.channel.send("Not really. Condensation is gas to liquid. You may want to look at the material linked below. Tell me when you are ready: %s"%("https://www.youtube.com/watch?v=SfzUBe7lp44"))
    elif left_message.startswith('okay let us start the preparation for the lesson') or left_message.startswith('i understood what is evaporation'):
      #questions=["What is condensation?","What is evaporation?"]
      #ans={}
      #ans[questions[0]]="liquid to gas"
      #ans[questions[1]]="gas to liquid"
      text='What is evaporation?'+'\n\n(a) '+options[0]+'      (b) '+options[1]+'\n\n(c) '+options[2]+'\t\t\t\t\t\t\t\t(d) '+options[3]
      embed2.description=text
      time.sleep(2)
      await message.channel.send(embed=embed2)

    
    elif left_message.startswith('i am bored') or left_message.startswith('tell me a joke'):
      joke = get_jokes()
      time.sleep(1)
      await message.channel.send("Let me tell you a joke:\n"+joke)
    #elif left_message.startswith('when is our social studies assignment due') or :
    elif re.search('when is', left_message) and re.search('assignment due', left_message):
      due_date=datetime.now() + timedelta(1)
      #day=calendar.day_name[due_date]
      time.sleep(1)
      #await message.channel.send("Your social studies assignment is due on "+due_date.strftime('%A, %dth %B %Y'))
      await message.channel.send("This assignment is due on "+due_date.strftime('%A, %dst %B %Y'))
    #elif left_message.startswith('let us start the preparation for the lesson on Water Cycle'):
      #questions=["What is condensation?","What is evaporation?"]
      #options=["Liquid to Gas","Solid to Gas","Liquid to Solid","Gas to Liquid"]
      #ans={}
      #ans[questions[0]]="liquid to gas"
      #ans[questions[1]]="gas to liquid"
      #text=questions[0]+'\n'+options[0]+'\t'+options[1]+'\n'+options[2]+'\t'+options[3]
      #embed.description=text
      #await message.channel.send("What is "+text)
      #await message.channel.send("What is evaporation")
    else:
      failed_answers=['No short answer available','?','Wolfram|Alpha did not understand your input','No response']
      voyager_response = get_voyager(left_message)
      print(voyager_response)
      curr_msg=left_message
      history=[]
      while(True):
        if curr_msg not in history:
          history.append(curr_msg)
        if voyager_response.status_code == 500:
          await message.channel.send("That is NOT acceptable!")
          break
        elif voyager_response.status_code == 200:
          voyager_answer = voyager_response.json()
          if 'index' in voyager_answer.keys():
            index_curr=voyager_answer['index']
          sources=voyager_answer['source']
          answers=voyager_answer['text']
          source_answer_map={}
          #print("Fail")
          fail=0
          arithmetic_words=['sum','added','by','plus','add','product','multiplied','multiply','divide','divided','square','minus','difference','subtract','subtracted','+','-','*','**','/']
          for i in range(0,len(sources)):
            #print("Here:")
            if answers[i] not in failed_answers:
              source_answer_map[sources[i]]=answers[i]
            elif answers[i] in failed_answers:
              fail=1
          if len(source_answer_map)==0:
            await message.channel.send("I cannot confidently answer this question. Let me refer this to your teacher. They will help you")
            #await client.wait_until_ready()
            #new_channel=client.get_channel(id=876313807851515967)
            #await new_channel.send("Hi @RKbotman, I could not respond to this question: "+curr_msg)
            #user=await client.get_user_info(876753113070043166)
            new_channel=client.get_channel(teacher_id)
            #client.loop.create_task(test())
            time.sleep(2)
            await new_channel.send("Hi @"+new_channel.name+", I could not respond to this question: "+curr_msg)
            #await client.send_message(user, "Hi @RKbotman, I could not respond to this question: "+curr_msg)
            break
                
          words=left_message.split()
          ov=list(set(words) & set(arithmetic_words))
          if len(ov)>0:
            voyager_para = '\n'.join(["Answer from "+str(k)+" : "+str(source_answer_map[k]) for k in ['Wolfram Alpha']])

          else:
            voyager_para = '\n'.join(["Answer from "+str(k)+" : "+str(source_answer_map[k]) for k in source_answer_map.keys()])
          #voyager_para = ' '.join([str(elem) for elem in voyager_answer["text"]]) 
          await message.channel.send(voyager_para)

          voyager_faq = '\n'.join([str(elem) for elem in voyager_answer["FAQs"]])

          request = youtube.search().list(part="snippet", q=curr_msg)
          response = request.execute()

          await message.channel.send("Check out this youtube video: %s"%("https://www.youtube.com/watch?v="+response['items'][0]['id']['videoId']))
          #voyager_faq = ' '.join([str(elem) for elem in voyager_answer["FAQs"]])
          #await message.channel.send('Did you know you could also ask about these: \n'+ voyager_faq)
          #await message.channel.send('Did you know you could also ask about these:')
          #for elem in voyager_answer["FAQs"][:2]:
          #embed.description = "["+elem+"](https://discord.com/channels/876313807851515964/876313807851515967)"
          #embed.title = "HM "+elem
          #buttons = [
           #   manage_components.create_button(
            #      style=ButtonStyle.blue,
             #     label="HM "+str(elem)  
              #),
            #]
          #button1 =  Button(win, text=elem, command=btn1("HM "+str(elem)))
          #put on screen
          #button1.pack()
          #win.mainloop()
          #action_row = #manage_components.create_actionrow(*buttons)
          #embed.description = elem
          #embed.add_field(name="undefined", value="undefined", inline=False)
          #await message.add_reaction("hm "+elem)
          if fail==1:
            await message.channel.send("This is the response we got but we are not sure about this.")
            embed2.description="Do you want us to contact your teacher?"
            components1 = [ActionRow(Button(label="Yes",custom_id='3',style=ButtonStyle.green)),(Button(label="No",custom_id='4',style=ButtonStyle.green))]
            msg = await message.channel.send(embed=embed2,components=components1)
            def _check(i: discord.Interaction, b):
              return i.message == msg and i.member == message.author
            interaction, button = await client.wait_for('button_click', check=_check)
            #button_id = button.custom_id
            await interaction.defer()
            if interaction.component.custom_id==3:
              new_channel=client.get_channel(teacher_id)
              stud=client.get_channel(message.channel.id)
              #client.loop.create_task(test())
              time.sleep(2)
              await new_channel.send("Hi @"+new_channel.name+", I am not sure about the response we got to this question: "+curr_msg+" asked by "+stud.name+". You may like to check the response and verify it.")

          faq=voyager_answer["FAQs"]
          #components = [ActionRow(Button(label=faq[0],custom_id='option1',emoji="🆗",style=ButtonStyle.green),Button(label=faq[1],custom_id='option2',emoji="🆗",style=ButtonStyle.green))]
          #for q in range(0,len(faq[:2])):
          #curr_msg=faq[0]
          '''if curr_msg in history:
            if faq[1] in history:
              curr_msg=faq[2]
            else:
              curr_msg=faq[1]'''
          time.sleep(1)
          embed.description="Do you want to leave a feedback to the response?"
          components2 = [ActionRow(Button(label="Yes",custom_id='33',style=ButtonStyle.green)),(Button(label="No",custom_id='44',style=ButtonStyle.green))]
          msg = await message.channel.send(embed=embed,components=components2)
          def _check(i: discord.Interaction, b):
            return i.message == msg and i.member == message.author
          interaction, button = await client.wait_for('button_click', check=_check)
          #button_id = button.custom_id
          await interaction.defer()
          if interaction.component.custom_id==33:
            await message.channel.send("You pressed Yes.")
            embed_fb.description="Is the answer correct?"
            components3 = [ActionRow(Button(label="Yes",custom_id='55',style=ButtonStyle.green)),(Button(label="No",custom_id='66',style=ButtonStyle.green))]
            msg = await message.channel.send(embed=embed_fb,components=components3)
            def _check(i: discord.Interaction, b):
              return i.message == msg and i.member == message.author
            interaction, button = await client.wait_for('button_click', check=_check)
            #button_id = button.custom_id
            await interaction.defer()
            time.sleep(4)
            if interaction.component.custom_id==55:
              await message.channel.send("Thank you for acknowledging that the response is correct.")
              if 'index' in voyager_answer.keys():
                url = "http://dev.api.merlyn.org/api/updatedatabase/"
                payload = {"index": voyager_answer['index'], "isCorrect": "true"}
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(url, data=json.dumps(payload), headers=headers)
                print(r)
            else:
              await message.channel.send("Please let us know your feedback to the question: "+curr_msg)
              embed_ok.description="Press the OK button below when you have entered the feedback:"
              components4 = [ActionRow(Button(label="OK",custom_id='100',style=ButtonStyle.green))]
              msg = await message.channel.send(embed=embed_ok,components=components4)
              def _check(i: discord.Interaction, b):
                return i.message == msg and i.member == message.author
              interaction, button = await client.wait_for('button_click', check=_check)
              #button_id = button.custom_id
              await interaction.defer()
              #time.sleep(4)
              if interaction.component.custom_id==100:
                #time.sleep(10)
                coun=0
                async for msg in message.channel.history(limit=5): 
                  coun+=1  
                  hist=msg.content
                  if hist.startswith("Did you know") or hist.startswith("Please let us know") or msg.author==client.user:
                    print(msg.author.name)
                    continue
                  print(hist,msg.author.name)
                  if 'index' in voyager_answer.keys():
                    url = "http://dev.api.merlyn.org/api/updatedatabase/"
                    payload = {"index": voyager_answer['index'], "isCorrect": "false", "comments": hist}
                    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                    r = requests.post(url, data=json.dumps(payload), headers=headers)
                    print(r.json())
                  if coun == 5:
                    break
          time.sleep(3)
          embed.description="Did you know you could also ask about these:"
          #components = [ActionRow(Button(label=faq[q],custom_id='option1',emoji="🆗",style=ButtonStyle.green),Button(label=faq[q],custom_id='option2',emoji="🆗",style=ButtonStyle.green))]
          components = [ActionRow(Button(label=faq[0][:80],custom_id='1',style=ButtonStyle.green)),(Button(label=faq[1][:80],custom_id='2',style=ButtonStyle.green))]
          msg = await message.channel.send(embed=embed,components=components)
          def _check(i: discord.Interaction, b):
            return i.message == msg and i.member == message.author
          interaction, button = await client.wait_for('button_click', check=_check)
          #button_id = button.custom_id
          await interaction.defer()
          if interaction.component.custom_id==1:
            voyager_response = get_voyager(faq[0])
            curr_msg=faq[0]
            await message.channel.send("You clicked the question: "+curr_msg+"\nPlease find the answer below:")
            time.sleep(1)
          if interaction.component.custom_id==2:
            voyager_response = get_voyager(faq[1])
            curr_msg=faq[1]
            await message.channel.send("You clicked the question: "+curr_msg+"\nPlease find the answer below:")
            time.sleep(1)
          #process_response(voyager_response,faq[q],"hm "+faq[q])
          #await interaction.edit(embed=embed.add_field(name='Choose', value=f'HM `{faq[q]}`'))
          #await message.channel.send("hm "+faq[q])

          #await message.channel.send(embed=embed)
          #await message.channel.send(components=[action_row],embed=embed)        #await message.channel.send(embed=embed)
          #await message.add_reaction("HM")
          #message = await message.channel.send(embed = embed)
          #await message.edit(embed = embed1)
          #if left_message in db.keys():
          #  await message.channel.send(db[left_message])
          #else:
          #  await message.channel.send('I do not know the #answer to this question but maybe you can ask #me ' + random.choice(list(db.keys())))
        else:
          await message.channel.send("Sorry I cannot help you now, can we try later?")
          break

  #elif re.search('you should have allowed me to ask', norm_message) or re.search('i don''t care', norm_message) or re.search('this is not done', norm_message):
    #client.loop.create_task(test())
    #channel=client.get_channel(876753113070043166)
    #await channel.send("Hi @prasenjit_dey, the sentiment seems to be negative in the student room. You may want to have a look​")
    #user = client.get_user(876753113070043166)
    #await message.user.send("Hi @prasenjit_dey, the sentiment seems to be negative in the student room. You may want to have a look")
      
      
my_secret = os.environ['TOKEN']
GOAuth = {}
GOAuth['token']= os.environ['G-OAuth_token']
GOAuth['refresh_token']= os.environ['G-OAuth_refresh_token']
GOAuth['token_uri']= os.environ['G-OAuth_token_uri']
GOAuth['client_id']= os.environ['G-OAuth_client_id']
GOAuth['client_secret']= os.environ['G-OAuth_client_secret']
GOAuth['scopes']= ["https://www.googleapis.com/auth/youtube.force-ssl"]

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"

credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(GOAuth)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

keep_alive()
client.run(my_secret)