FROM python:3.10

ENV TELEGRAM_BOT_TOKEN=''
ENV OPENAI_API_KEY=''

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

WORKDIR /app

CMD ["python", "tg_bot.py"]



