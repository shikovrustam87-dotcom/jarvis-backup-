#!/bin/bash
# reminder: check_api_keys.sh
echo "=== REMINDER: Missing API Keys ==="
echo "The following keys need to be provided:"
echo "1. DISCORD_BOT_TOKEN - for discordbot tools"
echo "2. XAI_API_KEY - for x_search tool"
echo "3. AITUNNEL_API_KEY - for fallback providers"
echo "4. NEURALGATE_API_KEY - for neural gateway"
echo "5. GROQ_API_KEY - for STT and fallback"
echo "6. GOOGLE_API_KEY - to restore Gemini access"
echo ""
echo "Use: manage_connections to connect, or edit ~/.hermes/.env to add keys"
date