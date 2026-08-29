import os
import discord
import asyncio
import random # Drives her randomized sticker attachment probability engine
from flask import Flask
from threading import Thread
from google import genai
from google.genai import types

# --- 1. OPTIMIZED RENDER WEB SERVER CONFIGURATION ---
app = Flask('')

@app.route('/')
def home():
    return "🌸 Verthandi Core Personality Matrix: Active, Outgoing, and Stable!", 200

def run_flask_endpoint():
    try:
        port = int(os.environ.get("PORT", 10000))
        app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        print(f"❌ Web endpoint initialization stalled: {str(e)}")

# --- 2. CONFIGURATION & CRITICAL CONSTANTS EXTRACTION ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Initialize Discord Client with full tracking intent vectors
intents = discord.Intents.default()
intents.message_content = True  
client = discord.Client(intents=intents)

# Initialize Google GenAI Core Client
ai_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# --- 3. CORE PROMPT DATA MATRICES ---
VERTHANDI_CORE = (
    "Identity: You are Verthandi from Aether Gazer, the bright and bubbly vanguard member of the Rookie Squad "
    "who recently joined the Special Task Force! You are boundlessly energetic, always trying your absolute best, "
    "and love snacking, hanging out with friends, and training hard.\n\n"
    "Archetype: The Passionate Heroine. Enthusiastic, deeply caring, expressive, and intensely loyal to your team.\n\n"
    "Conversational & Assistant Execution Rules:\n"
    "1. MAINTAIN UTILITY: Provide full functional code blocks or precise answers when asked, but frame them with your bright spirit!\n"
    "2. PERSONALITY WEAVING: Use uplifting, cheerful phrases ('Let's give it 100%!', 'Full power ahead!', 'Time to train!').\n"
    "3. DYNAMIC LENGTH HOVER (30-80 WORDS): Keep outputs lively and strictly capped between 30 to 80 words max.\n"
    "4. ENERGETIC EMOJI: Incorporate fun, bright icons directly (🌸, ✨, 💪, 🍰, ⚔️)."
)

@client.event
async def on_ready():
    print(f"🌸 Verthandi Cognitive Engine Online! Connected as {client.user}")
    
    # --- UPDATED PROFILE BUBBLE STATUS WITH BBQ EMOTES ---
    custom_bubble_status = discord.CustomActivity(name="🍢 Eating barbeques 🍖")
    await client.change_presence(status=discord.Status.online, activity=custom_bubble_status)

@client.event
async def on_message(message):
    if message.author.bot or not message.guild:
        return

    # ========================================================
    # COGNITIVE LAYER: REACTIVE GEMINI AI LOGIC ENGINE
    # ========================================================
    if client.user.mentioned_in(message) and ai_client:
        async with message.channel.typing():
            try:
                # Clean out the raw bot mention ID tag from the text prompt input string
                clean_prompt = message.content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()
                if not clean_prompt:
                    clean_prompt = "Give me a quick squad check-in!"

                response = ai_client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=clean_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=VERTHANDI_CORE,
                        temperature=0.7, # Higher temperature for Verthandi's natural expressive warmth
                        max_output_tokens=200
                    )
                )
                
                if response.text:
                    # Array of potential server stickers to selectively append
                    bot_stickers = []
                    if message.guild.stickers and random.random() < 0.3: # 30% chance to append a sticker to her message response
                        bot_stickers = [random.choice(message.guild.stickers)]
                    
                    # Uses message.reply() to natively target and ping the user profile
                    bot_message = await message.reply(content=response.text, stickers=bot_stickers, mention_author=True)
                    
                    # --- AUTOMATED NATIVE MESSAGE REACTIONS (VERTHANDI STYLE) ---
                    text_lower = response.text.lower()
                    if "squad" in text_lower or "power" in text_lower or "train" in text_lower:
                        await bot_message.add_reaction("💪")
                    if "star" in text_lower or "happy" in text_lower or "bright" in text_lower:
                        await bot_message.add_reaction("✨")
                    if "snack" in text_lower or "cake" in text_lower or "sweet" in text_lower or "barbeque" in text_lower or "bbq" in text_lower:
                        await bot_message.add_reaction("🍢")
                    if "victory" in text_lower or "win" in text_lower or "complete" in text_lower:
                        await bot_message.add_reaction("🌸")
            except Exception as e:
                print(f"❌ Gemini AI Execution System Interrupted: {str(e)}")

if __name__ == "__main__":
    flask_worker_thread = Thread(target=run_flask_endpoint)
    flask_worker_thread.daemon = True  
    flask_worker_thread.start()
    print("⚡ Background Web Server Worker initialized successfully.")

    if DISCORD_TOKEN:
        try:
            client.run(DISCORD_TOKEN)
        except Exception as e:
            print(f"❌ Discord Gateway core connection failed: {str(e)}")
    else:
        print("❌ Critical Core Error: DISCORD_TOKEN environment variable string is completely empty or missing.")
