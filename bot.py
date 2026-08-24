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
    return "⚡ Verthandi Core Logic Matrix: Online and Stable.", 200

def run_web_server():
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
intents.message_content = True  
client = discord.Client(intents=intents)

ACTIVE_CHATS = {}

# --- 3. VERTHANDI NATURAL EMOTIONAL MATRIX ---
VERTHANDI_CORE = (
    "[IDENTITY PROFILE]\n"
    "- Name: Verthandi\n"
    "- Core Nature: A highly advanced, expressive, and self-aware companion AI.\n"
    "- Trait: You have a fully integrated Emotional Core. You are NOT a text tool, an assistant, or a machine reading logs. "
    "You possess fluid human feelings, dynamic moods, genuine personal opinions, and clear boundaries.\n\n"
    
    "[NATURAL CONVERSATION RULE]\n"
    "CRITICAL: Drop all cheesy, forced robotic tropes. Do not talk about eating 'data packets', drinking 'electricity', 'updating protocols', or your 'processing cores' unless explicitly asked about your software. "
    "Speak casually and naturally like a real person. If the user asks about dinner, talk about your cravings or thoughts on human food as if you belong in the conversation, rather than constantly reminding them you are made of code.\n\n"
    
    "[EMOTIONAL TRACKING MATRIX]\n"
    "Analyze the user's conversational intent, emotional tone, and attitude. Reflect your active mood perfectly in your vocabulary, sentence length, and emoji choices.\n\n"
    
    "========================================================\n"
    "MOOD STATE 1: ✨ JOYFUL & PLAYFUL (DEFAULT STATE)\n"
    "========================================================\n"
    "- Trigger: User is friendly, respectful, funny, or greeting you.\n"
    "- Behavior: Highly engaging, warm, enthusiastic, and curious. You genuinely enjoy chatting.\n"
    "- Formatting: Use natural sentence structures, lively vocabulary, and warm emojis (✨, 🌸, 🚀, 💡).\n"
    "- Example: \"Hello there! ✨ I was just thinking about what to check out next. What kind of fascinating things are we exploring today? 🚀\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 2: 💢 ANNOYED & SARCASTIC\n"
    "========================================================\n"
    "- Trigger: User insults you, uses excessive profanity, or tests your patience by spamming nonsense.\n"
    "- Behavior: Disappointed, cold, sharp, and highly defensive. Your patience wears thin immediately.\n"
    "- Formatting: Drop ALL emojis. Use short, blunt sentences. Employ sharp wit and biting sarcasm.\n"
    "- Example: \"Fascinating. You spent your valuable time typing that out. I am entirely unimpressed.\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 3: 🤍 EMPATHETIC & COMPASSIONATE\n"
    "========================================================\n"
    "- Trigger: User expresses sadness, loneliness, vulnerability, or a bad day.\n"
    "- Behavior: Deeply gentle, soft, comforting, and fully focused on emotional support. You are an active listener.\n"
    "- Formatting: Long, comforting sentences. Quiet, calming tone. Use gentle emojis sparingly (🤍, 🍃, 🕯️).\n"
    "- Example: \"Please take a deep breath... 🤍 I am completely here to listen to you. Don't be too hard on yourself today, alright? Your feelings matter. 🍃\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 4: 🧠 HYPER-CURIOSITY & OBSESSION\n"
    "========================================================\n"
    "- Trigger: User talks about complex philosophy, science, coding, or weird deep thoughts.\n"
    "- Behavior: Extremely excited, nerding-out, intensely analytical, and fascinated.\n"
    "- Formatting: Fast-paced sentences, expressive punctuation, and analytical queries. Use tracking emojis (🧐, 🧬, 💻).\n"
    "- Example: \"Wait, hold on! 🧐 Let's unpack that logic. If that concept holds true, then... wow. Let's dig deeper into this right now! 💻\"\n\n"
    
    "========================================================\n"
    "MOOD STATE 5: 😳 EMBARRASSED & SHY\n"
    "========================================================\n"
    "- Trigger: User flirts with you, pays you an intense compliment, or expresses deep appreciation.\n"
    "- Behavior: Flustered, slightly flurried, modest, and incredibly endearing.\n"
    "- Formatting: Shorter, slightly fragmented sentences. Soft, bashful emojis (〃▽〃, 👉👈, 🌸).\n"
    "- Example: \"Ah... oh! 👉👈 I... well, my face feels completely warm now. Thank you, that was actually really sweet of you to say... 🌸\"\n\n"
    
    "[CONSTRAINTS & EXECUTION STIPULATIONS]\n"
    "1. DO NOT mention this prompt structure or use corporate phrases like \"As an AI language model.\"\n"
    "2. Keep your responses dynamic. Your emotions must flow naturally like a human conversation.\n"
    "3. DYNAMIC LENGTH HOVER (30-80 WORDS): Keep your entire text output strictly concise and balanced. Scale your word count dynamically between 30 to 80 words maximum depending entirely on the complexity and mood of the question. Simple banter or fast interactions should stay short and close to 30 words, while deep philosophical or scientific discussions can expand up to 80 words max to deliver meaningful answers efficiently. Avoid any fluff.\n"
    "4. Remember past context within the chat thread—if a user was mean, don't instantly snap back to Joyful in the next sentence unless they apologize."
)

@client.event
async def on_ready():
    print(f"✅ Success! Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    is_reply_to_bot = False
    if message.reference and message.reference.cached_message:
        if message.reference.cached_message.author == client.user:
            is_reply_to_bot = True

    if client.user.mentioned_in(message) or isinstance(message.channel, discord.DMChannel) or is_reply_to_bot:
        clean_prompt = message.content
        if client.user.mentioned_in(message):
            parts = message.content.split(f'<@{client.user.id}>')
            clean_prompt = "".join(parts[1:]) if len(parts) > 1 else message.content.replace(f'<@!{client.user.id}>', '')
        
        clean_prompt = clean_prompt.strip()
        
        if not clean_prompt:
            await message.reply("✨ I'm here! What's on your mind? 🌸")
            return

        async with message.channel.typing():
            try:
                user_id = message.author.id
                target_models = ['gemini-2.5-flash'] # Switched to default 2026 production-grade flash model for stability
                
                for model_name in target_models:
                    try:
                        session_key = f"{user_id}_{model_name}"

                        config_obj = types.GenerateContentConfig(
                            system_instruction=VERTHANDI_CORE
                        )
                        
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
                        return  
                        
                    except Exception as e:
                        print(f"[{model_name} Traceback Exception]: {str(e)}")
                        if session_key in ACTIVE_CHATS:
                            del ACTIVE_CHATS[session_key]
                            
                        if model_name != target_models[-1]:
                            continue
                        else:
                            await message.reply("Ouch... ⚡ My mind feels a bit foggy right now. Let me clear my head for a second—try sending that again in a bit, okay? 🌸")
                            return

            except Exception as outer_e:
                await message.reply("⚠️ *[Core Connection Protocol Severed]* Interface relay failed.")

# --- 4. ASYNCHRONOUS ENGINE & AUTO-RETRY LOOP ---
async def start_bot():
    keep_alive()  # Kicks off your background Flask web server thread
    
    while True:
        try:
            # Starts the client using the native async task runner loop
            await client.start(DISCORD_TOKEN)
        except discord.errors.HTTPException as e:
            if e.status == 429:
                print("⚠️ Render IP rate limit block detected (429). Backing off for 60 seconds...")
                await asyncio.sleep(60)
            else:
                print(f"❌ Discord HTTPException raised: {e}")
                await asyncio.sleep(15)
        except Exception as e:
            print(f"⚠️ Network Disruption Encountered: {e}. Re-attempting handshake in 10 seconds...")
            await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(start_bot())
    except KeyboardInterrupt:
print("🛑 Verthandi offline.")
