import re

def remove_proper_nouns(sentence):
    # Разделение предложения на слова
    words = sentence.split()

    # Удаление слов, начинающихся с большой буквы, кроме первого слова
    filtered_words = [words[0]] + [word for word in words[1:] if not word.istitle()]

    # Сбор слов обратно в предложение
    filtered_sentence = ' '.join(filtered_words)

    return filtered_sentence

def process_text(file_path):
    # Чтение файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Разбиение текста на предложения
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)

    # Удаление пустых строк и обработка каждого предложения
    processed_sentences = [remove_proper_nouns(sentence) for sentence in sentences if sentence.strip()]

    # Сохранение каждого предложения в отдельной строке
    with open('/app/processed_text.txt', 'w', encoding='utf-8') as output_file:
        output_file.write('\n'.join(processed_sentences))

    return processed_text


processed_text = process_text('/app/FiftyShadesofGrey.txt')

print(processed_text)
