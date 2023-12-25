import telebot
import random
import os
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain, TransformChain, SequentialChain
from langchain.callbacks import get_openai_callback

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
api_key = os.environ.get('OPENAI_API_KEY', '')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
    return result

def transform_func(inputs: dict) -> dict:
    text = inputs["text"]
    return {"output_text": text}

template = """Paraphrase this text: {output_text} In the style of a {style}. Paraphrase: """
prompt = PromptTemplate(input_variables=["style", "output_text"], template=template)

style_paraphrase_chain = LLMChain(llm=OpenAI(temperature=0, openai_api_key=api_key),
                                      prompt=prompt, output_key='final_output')

chain = TransformChain(input_variables=["text"], output_variables=["output_text"], transform=transform_func)

sequential_chain = SequentialChain(chains=[chain, style_paraphrase_chain],
                                   input_variables=['text', 'style'], output_variables=['final_output'])

path = '/app/data.txt'
path2 = '/app/processed_text.txt'


# Flag to track whether the initial retrieval has occurred
initial_retrieval_done = False

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Write me)")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    global initial_retrieval_done

    if not initial_retrieval_done:
        # Perform initial retrieval
        retrieve(message)
        initial_retrieval_done = True
    else:
        # Subsequent messages trigger OpenAI to generate responses
        generate_response(message)

def retrieve(message):
    with open(path, 'r', encoding='utf-8') as file:
        sentences = file.readlines()

    random_sentence = random.choice(sentences)
    input_text = random_sentence

    result = count_tokens(sequential_chain, {'text': input_text, 'style': 'sexting_with_men'})
    bot.reply_to(message, result)

def generate_response(message):

    def similar():
        user_input = message.text

        with open(path2, 'r', encoding='utf-8') as file:
            sentences = file.readlines()

        random_sentence = random.choice(sentences)

        print(user_input, random_sentence)

        vectorizer = CountVectorizer().fit_transform([user_input, random_sentence])
        vectors = vectorizer.toarray()

        # Расчет косинусной близости
        cosine_sim = cosine_similarity(vectors[0].reshape(1, -1), vectors[1].reshape(1, -1))

        print(cosine_sim[0][0])
        return cosine_sim, random_sentence, user_input

    cos_sim_answer, random_sent, user_text = similar()

    while cos_sim_answer[0][0] < 0.1:
        cos_sim_answer = similar()

    combane_text = user_text + ' ' + random_sent
    result = count_tokens(sequential_chain, {'text': combane_text, 'style': 'sexting_with_men'})

    bot.reply_to(message, result)

bot.polling()

