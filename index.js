const { Client, GatewayIntentBits } = require('discord.js');

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent
    ]
});

// Character Personality Configuration
const BOT_PERSONALITY = "You are a helpful, witty, and highly intelligent assistant named Verthandi. Keep your responses engaging, brief, and clear.";

client.once('ready', () => {
    console.log(`Success! VerthandiBot AI is now logged in as ${client.user.tag}`);
});

client.on('messageCreate', async (message) => {
    // Ignore messages from other bots to prevent infinite text loops
    if (message.author.bot) return;

    // Trigger only if your bot account is explicitly tagged/mentioned
    if (message.mentions.has(client.user)) {
        const userPrompt = message.content.replace(`<@${client.user.id}>`, '').trim();
        if (!userPrompt) return message.reply("Hello! I am Verthandi. Ask me anything by tagging me!");

        // Simulate typing animation behavior
        await message.channel.sendTyping();

        try {
            // FIXED: The unified, official Google Gemini endpoint URL path structure
            const apiKey = process.env.SECRET_GEMINI_KEY || process.env.GEMINI_API_KEY || '';
            const cleanUrl = "https://googleapis.com" + String(apiKey).trim();

            const response = await fetch(cleanUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: userPrompt }] }],
                    system_instruction: { parts: [{ text: BOT_PERSONALITY }] }
                })
            });

            const data = await response.json();
            
            // Standard safe checking conditions targeting index tokens safely
            let aiReply = "";
            if (data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0]) {
                aiReply = data.candidates[0].content.parts[0].text;
            }

            if (aiReply) {
                return await message.reply(aiReply.substring(0, 2000));
            } else {
                console.log("Empty Response Data:", JSON.stringify(data));
                return await message.reply("I reached my AI module, but the output came back empty.");
            }
        } catch (error) {
            console.error("AI Thread Connection Exception:", error);
            return await message.reply("My circuits hit an internal network timeout. Try again shortly!");
        }
    }
});

client.login(process.env.DISCORD_TOKEN);
