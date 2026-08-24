import dotenv from 'dotenv';
// FORCES THE CONTAINER TO INJECT RENDER'S ENVIRONMENT CARDS ON STEP ONE
dotenv.config();

import { Client, GatewayIntentBits, ActivityType } from 'discord.js';
import http from 'http';
import { askVerthandi } from './services/gemini.js';

// --- 1. OPTIMIZED ISOLATED RENDER WEB SERVER ROUTING ---
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('⚡ Verthandi Core Logic Matrix: Online and Stable.\n');
});

// Port isolated to 10005 to prevent collision loops with your other bots
const PORT = process.env.PORT || 10005;
server.listen(PORT, '0.0.0.0', () => {
  console.log(`⚡ Async Web Endpoint bound successfully to port ${PORT}`);
});

// --- 2. CONFIGURATION EXTRACTION & CHAT MANAGERS ---
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,             // Mandatory core intent to register inside your server layout
    GatewayIntentBits.GuildMessages,      // Allows tracking of message updates inside channels
    GatewayIntentBits.MessageContent,     // Allows parsing text strings for your AI engine
    GatewayIntentBits.GuildVoiceStates    // Tracks voice activity channels
  ],
  // Forces the very first WebSocket packet to explicitly broadcast her online status flag
  presence: {
    status: 'online',
    activities: [{
      type: ActivityType.Custom,
      name: 'custom',
      state: 'Chatting with the Server ✨'
    }]
  }
});

const COMMAND_PREFIX = "?";

client.once('ready', () => {
  console.log(`✅ Success! Verthandi logged in as ${client.user.tag}`);

  // Persistent refresh loop to keep her socket punching through Render's network cache
  const updatePresence = () => {
    try {
      client.user.setPresence({
        status: 'online',
        activities: [{
          type: ActivityType.Custom,
          name: 'custom',
          state: 'Chatting with the Server ✨'
        }]
      });
    } catch (err) {
      console.error(`[Presence Refresh Error]: ${err.message}`);
    }
  };

  updatePresence();
  setInterval(updatePresence, 10000);
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

// --- 3. HARD ERROR LOGGER MATRIX ---
client.login(process.env.DISCORD_TOKEN).catch(error => {
  console.error(`❌ CRITICAL GATEWAY LOGIN FAILURE: ${error.message}`);
  console.error(error);
});


// --- 3. HARDEST ERROR LOGGER MATRIX ---
client.login(process.env.DISCORD_TOKEN).catch(error => {
  console.error(`❌ CRITICAL GATEWAY LOGIN FAILURE: ${error.message}`);
  console.error(error);
});
