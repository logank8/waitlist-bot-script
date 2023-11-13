from discord.ext import tasks

import discord

from selenium import webdriver
from selenium.webdriver.common.by import By


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        self.counter = 0

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.my_background_task.start()

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def my_background_task(self):
        print('looping...')
        channel_debug = self.get_channel(1095410811045945435)  # channel ID goes here
        channel_main = self.get_channel(1094315067064991825)
        if (self.counter == 100):
            self.counter = 0
        else:
            self.counter += 1
        print(self.counter)
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(f'user-agent={user_agent}')
        driver = webdriver.Chrome(options=options)

        # check MATH 441

        driver.get("https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=MATH&course=441&section=201")
        element = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/table[3]/tbody/tr[2]/td[2]/strong")
        if (element.text == "60"):
            await channel_debug.send('MATH 441 still full')
            await channel_debug.send(self.counter)
        else:
            await channel_main.send("MATH 441 available!")

        # check CPSC 440
        
        driver.get("https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=CPSC&course=440&section=201")
        element = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/table[4]/tbody/tr[2]/td[2]/strong")
        if (element.text == "114"):
            await channel_debug.send('CPSC 440 still full')
            await channel_debug.send(self.counter)
        else:
            await channel_main.send("CPSC 440 available!")

        # check CPSC 404

        driver.get("https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-section&dept=CPSC&course=404&section=201")
        element = driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/table[4]/tbody/tr[2]/td[2]/strong")
        if (element.text == "90"):
            await channel_debug.send('CPSC 404 still full')
            await channel_debug.send(self.counter)
        else:
            await channel_main.send("CPSC 404 available!")

    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


client = MyClient(intents=discord.Intents.default())
client.run(#discord key goes here. not including mine, no thieves allowed!)