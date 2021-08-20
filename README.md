# MerlynVoyagerBot
How to create a Bot stub in Discord before writing the actual code for the Bot which can be hosted anywhere.

Go to: https://discord.com/developers/applications

Click on "New Application"

<img width="500" alt="Screen Shot 2021-08-19 at 6 50 36 PM" src="https://user-images.githubusercontent.com/88387668/130077063-b415b3b3-7760-43c7-9096-bf1214835ab8.png">

Give the Bot a name and click "Create"

<img width="500" alt="Screen Shot 2021-08-19 at 6 51 23 PM" src="https://user-images.githubusercontent.com/88387668/130077522-0ddc9212-81a0-48c4-8e23-575ff4d55dff.png">

Got to "Bot" option on the left and Click "Add Bot"

<img width="500" alt="Screen Shot 2021-08-19 at 6 55 42 PM" src="https://user-images.githubusercontent.com/88387668/130078914-547536fd-5531-4336-9930-b4d4b9ccd182.png">

<img width="500" alt="Screen Shot 2021-08-19 at 6 55 52 PM" src="https://user-images.githubusercontent.com/88387668/130080730-939362aa-7f04-4bff-b481-87e0c8695907.png">

This is what you see after adding the Bot

<img width="500" alt="Screen Shot 2021-08-19 at 6 58 13 PM" src="https://user-images.githubusercontent.com/88387668/130079288-90354df8-1717-48ab-b1b3-ae819f1959c4.png">

Go to OAuth2 option on the left and select Bot, all the Text Options and View Channels as shown

<img width="500" alt="Screen Shot 2021-08-19 at 6 57 03 PM" src="https://user-images.githubusercontent.com/88387668/130079663-82a403ea-f4d5-4f93-b2ab-5948f176d0b7.png">

Copy the Bot URL from the box as shown using the "Copy" button. This allows the Bot to be added to a server.

<img width="500" alt="Screen Shot 2021-08-19 at 6 57 03 PM" src="https://user-images.githubusercontent.com/88387668/130079663-82a403ea-f4d5-4f93-b2ab-5948f176d0b7.png">

Paste the URL copied above to a browser and if you are logged in, it will show all the servers you own. Select the server and click "Continue". The Bot is now added to your server. You can now invite the Bot to any channel you want.

<img width="500" alt="Screen Shot 2021-08-19 at 6 57 45 PM" src="https://user-images.githubusercontent.com/88387668/130080479-8fc254c6-1693-4e9b-9c14-3f94e3552a13.png">

You will see the Bot as offline in the channel since there is no code running inside it yet

<img width="500" alt="Screen Shot 2021-08-20 at 11 49 39 AM" src="https://user-images.githubusercontent.com/88387668/130189248-9ff95d5e-f396-4943-897a-f17e001c60be.png">

In the next step we need to Copy the authorization TOKEN (as shown below) to be used in the actual Bot code (could be hosted elsewhere) to be able to access the Bot stub that is now in the channel.

<img width="500" alt="Screen Shot 2021-08-19 at 6 58 13 PM" src="https://user-images.githubusercontent.com/88387668/130189537-d933e684-6b11-499a-a8a5-9ad068e8a8cd.png">

This TOKEN is used with client.run(TOKEN) in the code to run the code in the Bot (see the main.py code).

ABOUT THE CODE

The code was written to run on Replit and hence the following are specific to Replit and are not needed when hosting on our own server:
* keep_alive.py is used to keep the Replit code running as Replit shuts down the code after a period of non-activity
* In main.py: my_secret = os.environ['TOKEN'] is used to keep the TOKEN secret in Replit as its code is all public and only enviroment variables are kept secret.
* In main.py: keep_alive() is not required to run it as discussed above.
