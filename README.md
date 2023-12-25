# Bot-OpenAI-langchain

## Loading
docker load -i tg_bot.tar

## Testing
docker run -e TELEGRAM_BOT_TOKEN='' -e OPENAI_API_KEY='' -it tg_bot
