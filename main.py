import discord
import os

TOKEN = os.environ['DISCORD_TOKEN']
SALON_BIENVENUE_ID = 1501257698300268554
SALON_TWITTER_ID = 1540447152050933820
SALON_THREADS_ID = 1540447072501633105
SALON_INSTAGRAM_ID = 1540447221516869793
SALON_QUI_TA_INVITE_ID = 1538731348255047720  # ID du salon #qui-t-a-invité

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

points = {}  # pseudo -> nombre de points


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

    salon = bot.get_channel(SALON_QUI_TA_INVITE_ID)
    if salon:
        embed = discord.Embed(
            title="🤝 Qui t'a invité ?",
            description=(
                "Bienvenue ! 👋\n\n"
                "Si un VA t'a fait venir sur UNIM AGENCY, clique le bouton ci-dessous "
                "et indique **son pseudo**.\n"
                "Ça lui permet de gagner des points pour le classement de la semaine "
                "(et une récompense 💰).\n\n"
                "👉 Clique sur « Indiquer qui m'a invité » juste en dessous."
            ),
            color=discord.Color.gold()
        )
        await salon.send(embed=embed, view=BoutonInvite())


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
