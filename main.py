import discord
import discord
import discord.opus
import ctypes.util

if not discord.opus.is_loaded():
    chemin_opus = ctypes.util.find_library('opus')
    noms_a_tester = [chemin_opus, 'libopus.so.0', 'libopus.so', 'opus']
    for nom in noms_a_tester:
        if nom is None:
            continue
        try:
            discord.opus.load_opus(nom)
            print(f"✅ Opus chargé : {nom}")
            break
        except OSError:
            continue
    if not discord.opus.is_loaded():
        print("⚠️ Impossible de charger Opus, tous les essais ont échoué")
import os
import asyncio
import yt_dlp
import imageio_ffmpeg

TOKEN = os.environ['DISCORD_TOKEN']
SALON_BIENVENUE_ID = 1501257698300268554
SALON_TWITTER_ID = 1540447152050933820
SALON_THREADS_ID = 1540447072501633105
SALON_INSTAGRAM_ID = 1540447221516869793
SALON_QUI_TA_INVITE_ID = 1538731348255047720
SALON_PARRAINAGE_ID = 1538731299500589117
SALON_EXPLICATION_ID = 1501257521321480446
SALON_COMMENCEMENT_ID = 1532334459934736455
SALON_ENTRETIEN_ID = 1500885984072437803

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = discord.Client(intents=intents)

points = {}  # pseudo -> nombre de points

file_attente = {}  # id_serveur -> liste de (url, titre)
en_lecture = {}     # id_serveur -> titre actuel

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'quiet': True,
    'default_search': 'ytsearch',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


async def recherche_audio(requete):
    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        infos = await loop.run_in_executor(None, lambda: ydl.extract_info(requete, download=False))
        if 'entries' in infos:
            infos = infos['entries'][0]
        return infos['url'], infos['title']


class ControlesMusique(discord.ui.View):
    def __init__(self, id_serveur):
        super().__init__(timeout=None)
        self.id_serveur = id_serveur

    @discord.ui.button(emoji="⏸️", style=discord.ButtonStyle.secondary, custom_id="musique_pause")
    async def pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸️ En pause.", ephemeral=True)
        else:
            await interaction.response.send_message("Rien à mettre en pause.", ephemeral=True)

    @discord.ui.button(emoji="▶️", style=discord.ButtonStyle.secondary, custom_id="musique_resume")
    async def reprendre(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ Reprise.", ephemeral=True)
        else:
            await interaction.response.send_message("Rien à reprendre.", ephemeral=True)

    @discord.ui.button(emoji="⏭️", style=discord.ButtonStyle.secondary, custom_id="musique_skip")
    async def suivant(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        if vc and (vc.is_playing() or vc.is_paused()):
            vc.stop()
            await interaction.response.send_message("⏭️ Musique suivante.", ephemeral=True)
        else:
            await interaction.response.send_message("Rien à passer.", ephemeral=True)

    @discord.ui.button(emoji="⏹️", style=discord.ButtonStyle.danger, custom_id="musique_stop")
    async def stop_musique(self, interaction: discord.Interaction, button: discord.ui.Button):
        vc = interaction.guild.voice_client
        file_attente[self.id_serveur] = []
        if vc:
            vc.stop()
            await vc.disconnect()
        await interaction.response.send_message("⏹️ Arrêté, file vidée.", ephemeral=True)


def jouer_suivant(id_serveur, voice_client, channel):
    if file_attente.get(id_serveur):
        url, titre = file_attente[id_serveur].pop(0)
        chemin_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
        source = discord.FFmpegPCMAudio(url, executable=chemin_ffmpeg, **FFMPEG_OPTIONS)

        def apres(erreur):
            asyncio.run_coroutine_threadsafe(
                envoyer_et_continuer(channel, id_serveur, voice_client),
                bot.loop
            )

        voice_client.play(source, after=apres)
        en_lecture[id_serveur] = titre
    else:
        en_lecture[id_serveur] = None


async def envoyer_et_continuer(channel, id_serveur, voice_client):
    jouer_suivant(id_serveur, voice_client, channel)
    if en_lecture.get(id_serveur):
        await channel.send(
            f"🎶 En train de jouer : **{en_lecture[id_serveur]}**",
            view=ControlesMusique(id_serveur)
        )


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
            "✅ C'est enregistré, merci !",
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

    id_serveur = message.guild.id if message.guild else None

    if message.content.startswith("!play "):
        requete = message.content[6:].strip()
        if not message.author.voice:
            await message.channel.send("Connecte-toi d'abord à un salon vocal.")
            return

        salon_vocal = message.author.voice.channel
        voice_client = message.guild.voice_client
        if not voice_client:
            voice_client = await salon_vocal.connect()

        await message.channel.send(f"🔎 Recherche : {requete}...")
        url, titre = await recherche_audio(requete)

        if id_serveur not in file_attente:
            file_attente[id_serveur] = []
        file_attente[id_serveur].append((url, titre))

        if not voice_client.is_playing() and not voice_client.is_paused():
            jouer_suivant(id_serveur, voice_client, message.channel)
            await message.channel.send(
                f"🎶 En train de jouer : **{en_lecture[id_serveur]}**",
                view=ControlesMusique(id_serveur)
            )
        else:
            await message.channel.send(f"➕ Ajouté à la file : **{titre}**")
        return

    if message.content.strip() == "!queue":
        liste = file_attente.get(id_serveur, [])
        if not liste:
            await message.channel.send("File d'attente vide.")
        else:
            texte = "\n".join(f"{i+1}. {titre}" for i, (_, titre) in enumerate(liste))
            await message.channel.send(f"📋 **File d'attente :**\n{texte}")
        return

    if message.content.strip() == "!leave":
        voice_client = message.guild.voice_client
        if voice_client:
            file_attente[id_serveur] = []
            await voice_client.disconnect()
            await message.channel.send("👋 Déconnecté.")
        return

    if message.content.strip() == "!classement":
        if not message.author.guild_permissions.administrator:
            return

        try:
            await message.delete()
        except discord.Forbidden:
            pass

        if not points:
            try:
                await message.author.send("Aucun point enregistré pour le moment.")
            except discord.Forbidden:
                pass
            return

        classement_trie = sorted(points.items(), key=lambda x: x[1], reverse=True)
        texte = "🏆 **Classement parrainage**\n\n"
        medailles = ["🥇", "🥈", "🥉"]
        for i, (pseudo, pts) in enumerate(classement_trie[:10]):
            medaille = medailles[i] if i < 3 else f"{i+1}."
            texte += f"{medaille} **{pseudo}** — {pts} point(s)\n"

        try:
            await message.author.send(texte)
        except discord.Forbidden:
            pass


bot.run(TOKEN)
