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
    // Ignore messages from other bots to prevent loops
    if (message.author.bot) return;

    // Trigger only if someone tags/mentions this bot profile directly
    if (message.mentions.has(client.user)) {
        // Strip the bot mention from the prompt string
        const userPrompt = message.content.replace(`<@${client.user.id}>`, '').trim();
        
        // If someone just tags the bot with an empty text line
        if (!userPrompt) {
            return message.reply("Hello! I am Verthandi. Ask me anything by tagging me!");
        }

        // Show visual typing animation status indicator
        await message.channel.sendTyping();

        try {
            // Secure connection to Google's API using standard native Web Queries
            const response = await fetch(
                `https://googleapis.com{process.env.GEMINI_API_KEY}`,
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                   body: JSON.stringify({
    contents: [{ parts: [{ text: userPrompt }] }],
    system_instruction: { parts: [{ text: BOT_PERSONALITY }] }
})
                }
            );

            const data = await response.json();
            
            let aiReply = "";
if (data && data.candidates && data.candidates[0] && data.candidates[0].content && data.candidates[0].content.parts && data.candidates[0].content.parts[0]) {
    aiReply = data.candidates[0].content.parts[0].text;
}

            if (aiReply) {
                // Return response as a direct message chain thread reply
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
