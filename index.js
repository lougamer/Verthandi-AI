import dotenv from 'dotenv';
// FORCES THE CONTAINER TO INJECT RENDER'S ENVIRONMENT CARDS ON STEP ONE
dotenv.config();

import { Client, GatewayIntentBits, ActivityType } from 'discord.js';
import http from 'http';
import { askVerthandi } from './services/gemini.js';

// --- 1. OPTIMIZED FIXED RENDER WEB SERVER ROUTING ---
const server = http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('⚡ Verthandi Core Logic Matrix: Online and Stable.\n');
});

// FIXED: Adjusted to 10000 to match Render's network requirements exactly
const PORT = process.env.PORT || 10000;
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

// --- FREE COOLDOWN TRACKER ---
const userCooldowns = new Map();

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

  if (isReplyOrMention && !message.content.startsWith(COMMAND_PREFIX)) {
    let cleanPrompt = message.content.replace(new RegExp(`<@!?${client.user.id}>`, 'g'), '').trim();
    
    if (!cleanPrompt) {
      return message.reply("✨ I'm here! What's on your mind? 🌸");
    }

    // ========================================================
    // 🛡️ FREE TIER PROTECTION FILTER
    // Blocks users from spamming requests and freezing your free API key
    // ========================================================
    const userId = message.author.id;
    const currentTime = Date.now();
    const cooldownAmount = 5000; // 5 seconds in milliseconds

    if (userCooldowns.has(userId)) {
      const expirationTime = userCooldowns.get(userId) + cooldownAmount;
      if (currentTime < expirationTime) {
        const timeLeft = ((expirationTime - currentTime) / 1000).toFixed(1);
        return message.reply(`Slow down a bit! 🌸 Give me ${timeLeft} more seconds to clear my thoughts before messaging again! ✨`);
      }
    }

    // Set the cooldown timestamp for the user
    userCooldowns.set(userId, currentTime);

    try {
      await message.channel.sendTyping();
      const verthandiReply = await askVerthandi(message.author.id, cleanPrompt);
      return message.reply(verthandiReply);
    } catch (err) {
      console.error(`[Message Event Exception Handler]: ${err.message}`);
    }
  }

  // Handle prefix execution triggers
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

