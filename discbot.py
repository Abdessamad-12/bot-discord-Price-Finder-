import discord
from scraping import scrape_amazon


def read_token():
    with open("token.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


intents = discord.Intents.default()
intents.members = True
intents.presences = True

token = read_token()
client = discord.Client(intents=intents)


@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if str(channel) == "général":
            await client.send_message(f"""Welcome to the server {member.mention}""")


@client.event
async def on_message(message):
    if message.author == client.user:  # Ignore messages sent by the bot itself
        return

    if message.content.startswith("hello"):
        await message.channel.send("Hello!")
    else:
        product_name, product_price, product_rating, product_prices, product_link = scrape_amazon(message.content)  # Pass the message content to the scraping function
        await message.channel.send("Nom du produit: " + product_name)
        await message.channel.send("Prix du produit: " + str(product_price) + "$")
        await message.channel.send("Évaluation du produit: " + str(product_rating))
        await message.channel.send("list des prix : " + str(product_prices))
        await message.channel.send("lien de produit: " + str(product_link))


client.run(token)
