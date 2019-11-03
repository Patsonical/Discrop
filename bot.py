import os, sys, traceback, discord
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from crop import cropImage

load_dotenv()
token     = os.getenv('DISCORD_TOKEN')
master_id = os.getenv('DISCORD_MASTER')

client = discord.Client()

@client.event
async def on_ready():
    # print(f'{client.user} connected!')
    pass

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    for att in message.attachments:
        if att.width != None:
            imgbytes = await att.read()
            img = Image.open(BytesIO(imgbytes))
            cropped = cropImage(img)
            if cropped != None:
                outbytes = BytesIO()
                cropped.save(outbytes, format='PNG')
                outbytes.seek(0)
                out = discord.File(outbytes, filename=att.filename)
                await message.channel.send(content="Let me crop that for you " + message.author.mention, file=out)
                # print(f'Cropped image sent!')
            # else:
                # print('Image doesn\'t need cropping!')

@client.event
async def on_error(event, *args, **kwargs):
    master = await client.fetch_user(master_id)
    errorInfo = sys.exc_info()
    errorMessage = "".join(traceback.format_tb(errorInfo[2])) + f'{errorInfo[1].__class__.__name__}: {str(errorInfo[1])}'
    await master.send(content=f'**ERROR LOG**\nEvent: `{event}`\n```{args}```\nTraceback:\n```{errorMessage}```')

client.run(token)

