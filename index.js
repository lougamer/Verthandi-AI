import { Client, GatewayIntentBits } from 'discord.js';
import dotenv from 'dotenv';
import http from 'http';
import { askVerthandi } from './services/gemini.js';

dotenv.config();

// --- 1. OPTIMIZED RENDER PROXY WEB SERVER ROUTING ---
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('⚡ Verthandi Core Logic Matrix: Online and Stable.\n');
});

const PORT = process.env.PORT || 10000;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`⚡ Async Web Endpoint bound successfully to port ${PORT}`);
});

// --- 2. CONFIGURATION EXTRACTION & CHAT MANAGERS ---
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildVoiceStates
  ]
});

const COMMAND_PREFIX = "?";

client.once('ready', () => {
  console.log(`✅ Success! Verthandi logged in as ${client.user.tag}`);
  // Establishes a customized active presence display status on startup
  client.user.setActivity('Chatting with the Server ✨', { type: 3 }); // Listening type
});

client.on('messageCreate', async (message) => {
  if (message.author.bot || !message.guild) return;

  const mentionString = `<@${client.user.id}>`;
  const isReplyOrMention = message.content.includes(mentionString) || message.mentions.has(client.user);

  // Trigger conversational AI logic on direct pings or inline replies
  if (isReplyOrMention && !message.content.startsWith(COMMAND_PREFIX)) {
    let cleanPrompt = message.content.replace(new RegExp(`<@!?${client.user.id}>`, 'g'), '').trim();
    
    if (!cleanPrompt) {
      return message.reply("✨ I'm here! What's on your mind? 🌸");
    }

    try {
      await message.channel.sendTyping();
      const verthandiReply = await askVerthandi(message.author.id, cleanPrompt);
      return message.reply(verthandiReply);
    } catch (err) {
      console.error(`[Message Event Exception Handler]: ${err.message}`);
    }
  }

  // Handle music prefix execution triggers or dedicated slash routing channels
  if (message.content.startsWith(COMMAND_PREFIX)) {
    const args = message.content.slice(COMMAND_PREFIX.length).trim().split(/ +/);
    const commandName = args.shift().toLowerCase();

    if (commandName === 'askverthandi') {
      const queryPayload = args.join(' ');
      if (!queryPayload) return message.reply("Prompt data required.");
      
      await message.channel.sendTyping();
      const reply = await askVerthandi(message.author.id, queryPayload);
      return message.reply(reply);
    }

    // Music Command placeholders (Ready for your customized player.js bindings)
    if (commandName === 'playsong') {
      return message.reply("🎵 Parsing stream parameters... (Connect your custom player.js file here)");
    }
    if (commandName === 'stopsong') {
      return message.reply("🛑 Audio streaming terminated cleanly.");
    }
  }
});

// --- 3. HARDEST ERROR LOGGER MATRIX ---
// This forces Render's console output window to explicitly print out connection faults
client.login(process.env.DISCORD_TOKEN).catch(error => {
  console.error(`❌ CRITICAL GATEWAY LOGIN FAILURE: ${error.message}`);
  console.error(error);
});

