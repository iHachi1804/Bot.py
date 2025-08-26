import os
import discord
from discord.ext import commands
import asyncio
from mcrcon import MCRcon

# --- Configuración del bot ---
intents = discord.Intents.all()  # Necesitas SERVER MEMBERS INTENT activado en Discord Developer Portal
bot = commands.Bot(command_prefix="!", intents=intents)

# --- Eventos ---
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# --- Moderación ---
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"🚫 {member} fue baneado. Motivo: {reason}")

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} fue expulsado. Motivo: {reason}")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, tiempo: int = None):
    if tiempo:
        duration = discord.utils.utcnow() + discord.timedelta(minutes=tiempo)
        await member.edit(timeout=duration)
        await ctx.send(f"🔇 {member} muteado por {tiempo} minutos.")
    else:
        await member.edit(timeout=None)
        await ctx.send(f"🔇 {member} muteado permanentemente.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def isolate(ctx, member: discord.Member, tiempo: int):
    role = discord.utils.get(ctx.guild.roles, name="Aislado")
    if not role:
        role = await ctx.guild.create_role(name="Aislado")
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False, read_messages=True)

    await member.add_roles(role)
    await ctx.send(f"🚷 {member} aislado por {tiempo} minutos.")
    await asyncio.sleep(tiempo * 60)
    await member.remove_roles(role)
    await ctx.send(f"✅ {member} ya no está aislado.")

# --- Anuncios ---
@bot.command()
async def anuncio(ctx, canal: discord.TextChannel, *, mensaje):
    embed = discord.Embed(title="📢 Anuncio", description=mensaje, color=discord.Color.gold())
    await canal.send(embed=embed)
    await ctx.send("✅ Anuncio enviado.")

# --- Conexión con Minecraft usando mcrcon ---
MCRCON_HOST = "127.0.0.1"
MCRCON_PORT = 25575
MCRCON_PASS = "raulmejialozanoplzegabro5"

@bot.command()
async def mcchat(ctx, *, mensaje):
    try:
        with MCRcon(MCRCON_HOST, MCRCON_PASS, port=MCRCON_PORT) as mcr:
            response = mcr.command(f"say [Discord] {mensaje}")
        await ctx.send("✅ Mensaje enviado al chat de Minecraft.")
    except Exception as e:
        await ctx.send(f"❌ No se pudo enviar el mensaje al chat de Minecraft.\nError: {e}")

# --- Mostrar IP del servidor Minecraft ---
@bot.command()
async def ip(ctx):
    embed = discord.Embed(title="🌐 IP del Servidor Minecraft", color=discord.Color.green())
    
    # Java
    embed.add_field(name="Java", value="・🌐➜𝙄𝙋: onlypvp.falixsrv.me", inline=False)
    
    # Bedrock
    embed.add_field(name="Bedrock", value="・📱➜𝘿𝙞𝙧𝙚𝙘𝙘𝙞𝙤́𝙣: onlypvp.falixsrv.me\n・🎯➜𝙋𝙪𝙚𝙧𝙩𝙤: 29954", inline=False)
    
    await ctx.send(embed=embed)

# --- Ejecutar bot ---
TOKEN = os.getenv("TOKEN")  # Leemos el token desde variable de entorno
if TOKEN is None:
    print("❌ ERROR: No se encontró la variable de entorno TOKEN.")
else:
    bot.run(TOKEN)
