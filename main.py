import discord
import os

TOKEN = os.environ['DISCORD_TOKEN']
SALON_BIENVENUE_ID = 1501257698300268554
SALON_TWITTER_ID = 1540447152050933820
SALON_THREADS_ID = 1540447072501633105
SALON_INSTAGRAM_ID = 1540447221516869793
SALON_QUI_TA_INVITE_ID = 1538731348255047720  # remplace par ton vrai ID si différent
SALON_PARRAINAGE_ID = 1538731299500589117     # remplace par ton vrai ID
SALON_EXPLICATION_ID = 1501257521321480446    # remplace par ton vrai ID du salon #explication

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

points = {}  # pseudo -> nombre de points

MESSAGE_PARRAINAGE = f"""🎁 Programme de parrainage UNIM AGENCY

Invite tes amis à rejoindre UNIM AGENCY en tant que VA ! 🚀

Comment ça marche :
1️⃣ Tu fais venir tes amis → ils rejoignent et deviennent VA.
2️⃣ Quand un ami arrive, il va dans <#1538731348255047720> et indique que c'est toi qui l'as invité.
3️⃣ Chaque invitation validée = 1 point pour toi.

🏆 Chaque fin de semaine (dimanche), le top 3 gagne :
🥇 1er → $5
🥈 2e → $3
🥉 3e → $2

⚠️ Minimum 5 invitations dans la semaine pour être éligible à une récompense.

Plus tu invites, plus tu gagnes. 💰
@everyone"""

MESSAGE_EXPLICATION = """📌 **Organisation du Discord — UNIM AGENCY**

Une fois arrivé sur le **Discord officiel**, vous pouvez commencer le travail.
Voici les différentes sections 👇

🎓 **Partie Formation**
Vous y trouverez toutes les réponses à vos questions :
• Formations écrites
• Vidéos explicatives
• Méthodes pour éviter les **bannissements**

💼 **Partie Travail**
C'est ici que tout se passe :
• Vous récupérez les **identités** à utiliser sur Instagram
• ⚠️ **1 compte = 1 identité** (très important à respecter)

💬 **Partie Général**
• Annonces importantes
• Tips, etc...

🎁 **Partie Autres**
• Système d'affiliation
• Jeux pour gagner de l'argent 💸
• Preuves de paiement

📌 Rendez-vous dans le salon pour passer l'entretien. : https://ptb.discord.com/channels/1500885983250350080/1500885984072437803"""


class FormulaireInvite(discord.ui.Modal, title="Qui t'a invité ?"):
    pseudo_parrain = discord.ui.TextInput(
        label="Pseudo de la personne qui t'a invité",
        placeholder="Ex: Mario",
        required=True,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):
        parrain = self.pseudo_parrain.value.strip()
        points[parrain] = points.get(parrain, 0) + 1
        await interaction.response.send_message(
            f"✅ Merci ! **{parrain}** vient de gagner 1 point.",
            ephemeral=True
        )


class BoutonInvite(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Indiquer qui m'a invité",
        emoji="🤝",
        style=discord.ButtonStyle.success,
        custom_id="bouton_qui_ta_invite"
    )
    async def indiquer_invite(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FormulaireInvite())


@bot.event
async def on_ready():
    print(f"Connecté en tant que {bot.user}")
    bot.add_view(BoutonInvite())

    salon_explication = bot.get_channel(SALON_EXPLICATION_ID)
    if salon_explication:
        await salon_explication.send(MESSAGE_EXPLICATION)


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


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.strip() == "!classement":
        if not points:
            await message.channel.send("Aucun point enregistré pour le moment.")
            return
        classement_trie = sorted(points.items(), key=lambda x: x[1], reverse=True)
        texte = "🏆 **Classement parrainage**\n\n"
        medailles = ["🥇", "🥈", "🥉"]
        for i, (pseudo, pts) in enumerate(classement_trie[:10]):
            medaille = medailles[i] if i < 3 else f"{i+1}."
            texte += f"{medaille} **{pseudo}** — {pts} point(s)\n"
        await message.channel.send(texte)


bot.run(TOKEN)
