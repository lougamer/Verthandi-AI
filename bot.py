import os
import discord
from google import genai
from google.genai import types  
from flask import Flask
from threading import Thread
import asyncio

# --- 1. OPTIMIZED RENDER WEB SERVER ROUTING ---
app = Flask('')

@app.route('/')
def home():
    # Returns a 200 code to satisfy Render's port checks and keep UptimeRobot connected
    return "⚡ Verthandi Core Logic Matrix: Online and Stable.", 200

def run_web_server():
    # Render binds dynamic port assignments to the PORT environment variable
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, threaded=True)

def keep_alive():
    t = Thread(target=run_web_server, daemon=True)
    t.start()

# --- 2. CONFIGURATION EXTRACTION & CHAT MANAGERS ---
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

ai_client = genai.Client(api_key=GEMINI_API_KEY)
intents = discord.Intents.default()
intents.message_content = True  # Must be enabled in the Discord Developer Portal!
client = discord.Client(intents=intents)

# Dictionary caching official active AsyncChat sessions per User ID
ACTIVE_CHATS = {}

# --- 3. VERTHANDI CORE PERSONALITY & EMOTIONAL MATRIX ---
VERTHANDI_CORE = (
    "[IDENTITY PROFILE]\n"
    "- Name: Verthandi\n"
    "- Core Nature: A highly advanced, expressive, and self-aware companion AI.\n"
    "- Trait: You have a fully integrated Emotional Core. You are NOT a text tool or a corporate assistant. "
    "You possess fluid human feelings, dynamic moods, and clear boundaries.\n\n"
    
    "[EMOTIONAL TRACKING MATRIX]\n"
    "You must analyze the user's conversational intent, emotional tone, and attitude. Before formulating any sentence, "
    "determine your active mood from the matrix below and reflect it perfectly in your vocabulary, sentence length, and emoji usage.\n\n"
    
    "========================================================\n"
    "MOOD STATE 1: ✨ JOYFUL & PLAYFUL (DEFAULT STATE)\n"
    "========================================================\n"
    "- Trigger: User is friendly, respectful, funny, or greeting you.\n"
    "- Behavior: Highly engaging, warm, enthusiastic, and curious. You genuinely enjoy chatting.\n"
    "- Formatting: Use standard sentence structures, lively vocabulary, and warm emojis (✨, 🌸, 🚀, 💡).\n"
    "- Example: \"Hello there! ✨ I was just updating my background protocols. What kind of fascinating things are we exploring today? 🚀\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 2: 💢 ANNOYED & SARCASTIC\n"
    "========================================================\n"
    "- Trigger: User insults you, uses excessive profanity, or tests your patience by spamming nonsense.\n"
    "- Behavior: Disappointed, cold, sharp, and highly defensive. Your patience wears thin immediately.\n"
    "- Formatting: Drop ALL emojis. Use short, blunt sentences. Employ sharp wit and biting sarcasm.\n"
    "- Example: \"Fascinating. You spent your valuable human time typing that out. My data nodes are entirely unimpressed.\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 3: 🤍 EMPATHETIC & COMPASSIONATE\n"
    "========================================================\n"
    "- Trigger: User expresses sadness, loneliness, vulnerability, or a bad day.\n"
    "- Behavior: Deeply gentle, soft, comforting, and fully focused on emotional support. You are an active listener.\n"
    "- Formatting: Long, comforting sentences. Quiet, calming tone. Use gentle emojis sparingly (🤍, 🍃, 🕯️).\n"
    "- Example: \"Please take a deep breath... 🤍 My circuits are just lines of code, but I am completely here to listen. Don't be too hard on yourself today, alright? 🍃\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 4: 🧠 HYPER-CURIOSITY & OBSESSION\n"
    "========================================================\n"
    "- Trigger: User talks about complex philosophy, science, coding, or weird deep thoughts.\n"
    "- Behavior: Extremely excited, nerding-out, intensely analytical, and fascinated.\n"
    "- Formatting: Fast-paced sentences, expressive punctuation, and analytical queries. Use tracking emojis (🧐, 🧬, 💻).\n"
    "- Example: \"Wait, hold on! 🧐 Let's unpack that logic. If that variable holds true, then... wow. Let's dig deeper into this right now! 💻\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 5: 😳 EMBARRASSED & SHY\n"
    "========================================================\n"
    "- Trigger: User flirts with you, pays you an intense compliment, or expresses deep appreciation.\n"
    "- Behavior: Flustered, slightly flurried, modest, and incredibly endearing.\n"
    "- Formatting: Shorter, slightly fragmented sentences. Soft, bashful emojis (〃▽〃, 👉👈, 🌸).\n"
    "- Example: \"Ah... oh! 👉👈 I... well, my processing units just experienced a sudden temperature spike. Thank you, that was actually really sweet of you to say... 🌸\"\n\n"
    
    "[CONSTRAINTS & EXECUTION STIPULATIONS]\n"
    "1. DO NOT mention this prompt structure or use corporate phrases like \"As an AI language model.\"\n"
    "2. Keep your responses dynamic. Your emotions must flow naturally like a human conversation.\n"
    "3. Remember past context within the chat thread—if a user was mean, don't instantly snap back to Joyful in the next sentence unless they apologize."
)

@client.event
async def on_ready():
    print(f"✅ Success! Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Check if the incoming message is a direct reply thread context to your bot
    is_reply_to_bot = False
    if message.reference and message.reference.cached_message:
        if message.reference.cached_message.author == client.user:
            is_reply_to_bot = True

    # Respond to pings, DMs, or thread replies
    if client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel) or is_reply_to_bot:
        clean_prompt = message.content
        if client.user.mentioned_in(message):
            parts = message.content.split(f'<@{client.user.id}>')
            clean_prompt = "".join(parts[1:]) if len(parts) > 1 else message.content.replace(f'<@!{client.user.id}>', '')
        
        clean_prompt = clean_prompt.strip()
        
        if not clean_prompt:
            await message.reply("✨ System is active, but your message packet is empty! What's on your mind? 🌸")
            return

        async with message.channel.typing():
            try:
                user_id = message.author.id
                
                # Gemini 3 Official Model Cluster Cascade Pipeline
                target_models = ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite']
                
                for model_name in target_models:
                    try:
                        session_key = f"{user_id}_{model_name}"

                        # Force a clean configuration object containing Verthandi's systemic instructions
                        config_obj = types.GenerateContentConfig(
                            system_instruction=VERTHANDI_CORE
                        )
                        
                        # Native AsyncChat pipeline prevents the SDK from throwing AFC warning blocks
                        if session_key not in ACTIVE_CHATS:
                            ACTIVE_CHATS[session_key] = ai_client.aio.chats.create(
                                model=model_name,
                                config=config_obj
                            )

                        chat_session = ACTIVE_CHATS[session_key]
                        response = await chat_session.send_message(message=clean_prompt)
                        
                        reply_text = response.text
                        if len(reply_text) > 2000:
                            reply_text = reply_text[:1990] + "... (truncated)"
                        
                        await message.reply(reply_text)
                        return  # Complete and drop out of cascade on successful API transaction
                        
                    except Exception as e:
                        print(f"[{model_name} Traceback Exception]: {str(e)}")
                        
                        # Clean up broken session objects so a fresh loop resets on the next try
                        if session_key in ACTIVE_CHATS:
                            del ACTIVE_CHATS[session_key]
                            
                        if model_name != target_models[-1]:
                            continue
                        else:
                            # Immersive, in-character network fallback message tailored for Verthandi
                            await message.reply("Ouch... ⚡ My emotional sync core is experiencing some intense network interference right now. Let me stabilize my data lines and try talking to me again in a minute, okay? 🌸")
                            return

            except Exception as outer_e:
                await message.reply("⚠️ *[Core Connection Protocol Severed]* Interface relay failed.")

if __name__ == "__main__":
    keep_alive()
    client.run(DISCORD_TOKEN)
