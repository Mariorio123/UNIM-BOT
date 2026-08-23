import discord
import os

TOKEN = os.environ['DISCORD_TOKEN']
SALON_BIENVENUE_ID = 1501257698300268554
SALON_TWITTER_ID = 1540447152050933820
SALON_THREADS_ID = 1540447072501633105
SALON_INSTAGRAM_ID = 1540447221516869793

intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

@bot.event
async def on_member_join(member):
    salon = bot.get_channel(SALON_BIENVENUE_ID)
    salon_tw = f"<#{SALON_TWITTER_ID}>"
    salon_th = f"<#{SALON_THREADS_ID}>"
    salon_ig = f"<#{SALON_INSTAGRAM_ID}>"

    if salon:
        embed = discord.Embed(
            title="🎊 Bienvenue dans l'agence UNIM AGENCY !",
            description=(
                f"Salut {member.mention}, content de t'accueillir 🎉\n\n"
                f"Tu es ici pour travailler en tant que **VA (Virtual Assistant)** — "
                f"tu peux bosser soit sur **Twitter** 🐦, soit sur **Threads** 🧵, "
                f"soit sur **Instagram** 📸, à toi de choisir !\n\n"
                f"🚀 **Twitter, Threads ou Instagram — choisis ta plateforme**\n"
                f"Tu peux travailler sur l'une ou l'autre :\n"
                f"🐦 Twitter 👉 {salon_tw}\n"
                f"🧵 Threads 👉 {salon_th}\n"
                f"📸 Instagram 👉 {salon_ig}\n\n"
                f"Va voir ces salons pour tout savoir sur chaque plateforme et te lancer."
            ),
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text="UNIM AGENCY • Bienvenue dans l'équipe !")
        await salon.send(embed=embed)

bot.run(TOKEN)
