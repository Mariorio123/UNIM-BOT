import discord
import os

TOKEN = os.environ['DISCORD_TOKEN']
SALON_BIENVENUE_ID = 1501257698300268554
SALON_TWITTER_ID = 1540447152050933820
SALON_THREADS_ID = 1540447072501633105
SALON_INSTAGRAM_ID = 1540447221516869793
SALON_PAIEMENT_ID = 1501257450496458894  # ID du salon "infos paiement"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

MESSAGE_PAIEMENT = """# 🎯 Bienvenue dans l'équipe UNIM Agency

## 💰 NOUVELLE STRUCTURE DE RÉMUNÉRATION

*(Remplace intégralement l'ancienne grille)*

La rémunération est calculée **par jour**, en fonction :

* du **nombre d'abonnements générés**
OU
* du **nombre de clics générés**
* de la **plateforme utilisée** (Instagram)

---

## 🔹 RÉMUNÉRATION PAR ABONNEMENTS (SUBS) – **PAR JOUR**

### **Instagram**

Jusqu'à 15 subs : 0,50 USD par sub
Plus de 15 et jusqu'à 30 subs : 0,60 USD par sub
Plus de 30 et jusqu'à 50 subs : 0,70 USD par sub
Plus de 50 et jusqu'à 80 subs : 0,80 USD par sub
Plus de 80 subs : 0,90 USD par sub

---

## 🔹 RÉMUNÉRATION PAR CLICS – PAR JOUR

### **Instagram**

* Jusqu'à 150 clics : 0,040 USD par clic
* Plus de 150 et jusqu'à 300 clics : 0,047 USD par clic
* Plus de 300 et jusqu'à 500 clics : 0,053 USD par clic
* Plus de 500 et jusqu'à 800 clics : 0,060 USD par clic
* Plus de 800 clics : 0,067 USD par clic
---

## 📅 MODALITÉS DE PAIEMENT

* Paiements effectués **toutes les 2 semaines**
* Périodes de calcul :

Le 1er de chaque mois : pour la période du 08 au 23
Le 16 de chaque mois pour la période du 23 au 08
* Paiement prioritaire en **USDC (ERC-20 – réseau Ethereum)**

⚠️ Les performances sont **calculées quotidiennement**, puis consolidées sur la période de paiement.

---
@everyone"""


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")

    salon = bot.get_channel(SALON_PAIEMENT_ID)
    if salon:
        await salon.send(
            MESSAGE_PAIEMENT,
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
