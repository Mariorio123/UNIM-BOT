import discord
import os

TOKEN = os.environ['DISCORD_TOKEN']
SALON_BIENVENUE_ID = 1501257698300268554
SALON_TWITTER_ID = 1540447152050933820
SALON_THREADS_ID = 1540447072501633105
SALON_INSTAGRAM_ID = 1540447221516869793
SALON_PAIEMENT_ID = 1501257450496458894  # ID du salon "infos paiement"
SALON_PARRAINAGE_ID = 1538731299500589117  # ID du salon #parrainage

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

MESSAGE_PARRAINAGE = """🎁 Programme de parrainage UNIM AGENCY

Invite tes amis à rejoindre UNIM AGENCY en tant que VA ! 🚀

Comment ça marche :
1️⃣ Tu fais venir tes amis → ils rejoignent et deviennent VA.
2️⃣ Quand un ami arrive, il va dans #qui-t-a-invité et indique que c'est toi qui l'as invité.
3️⃣ Chaque invitation validée = 1 point pour toi.

🏆 Chaque fin de semaine (dimanche), le top 3 gagne :
🥇 1er → $5
🥈 2e → $3
🥉 3e → $2

⚠️ Minimum 5 invitations dans la semaine pour être éligible à une récompense.

Plus tu invites, plus tu gagnes. 💰
@everyone"""


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

    salon = bot.get_channel(SALON_PARRAINAGE_ID)
    if salon:
        await salon.send(
            MESSAGE_PARRAINAGE,
            allowed_mentions=discord.AllowedMentions(everyone=True)
        )


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
