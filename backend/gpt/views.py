from g4f.client import Client
import re
from base.constants import Constants


def validate_generated_content(content):
    lines = content.split('\n')
    if len(lines) < 3:
        return False 
    if not (lines[0].startswith("1. H1:") and
            lines[1].startswith("2. Title:") and
            lines[2].startswith("3. Description:")):
        return False
    return True

def generate_with_retry(client, formatted_request, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": formatted_request}],
                web_search=False
            )
            generated_content = response.choices[0].message.content.strip()
            if validate_generated_content(generated_content):
                return generated_content
            else:
                print(f"Попытка {attempt + 1}: Ответ GPT не соответствует формату. Повторная генерация...")
        except Exception as e:
            print(f"Попытка {attempt + 1}: Ошибка при генерации: {e}")
    raise ValueError("Не удалось получить корректный ответ после нескольких попыток")


def generations_for_news(validated_data):
    print("генерация...")
    formatted_request = (
        "На основе следующего текста новости сгенерируйте:\n"
        "1. H1 (заголовок): Напишите заголовок H1 от {min_h1} до {max_h1} символов, используя транслит через дефисы (например: 'primer-teksta-dlya-zagolovka').\n"
        "2. Title (заголовок для SEO): Напишите заголовок Title на русском языке, длиной от {min_title} до {max_title} символов.\n"
        "3. Description (описание): Напишите описание на русском языке, длиной от {min_description} до {max_description} символов.\n"
        "\nТекст новости:\n{content}"
    ).format(
        min_h1=Constants.MIN_LEN_H1,
        max_h1=Constants.MAX_LEN_H1,
        min_title=Constants.MIN_LEN_TITLE,
        max_title=Constants.MAX_LEN_TITLE,
        min_description=Constants.MIN_LEN_DESCRIPTION,
        max_description=Constants.MAX_LEN_DESCRIPTION,
        content=validated_data.get('content', '')
    )
    
    client = Client()
    try:
        generated_content = generate_with_retry(client, formatted_request)
        quote_pattern = r"^.*?:\s*[\"']?(.*?)[\"']?$"
        lines = generated_content.split('\n')
        for line in lines:
            match = re.search(quote_pattern, line)
            if line.startswith("1. H1:") and match:
                h1 = match.group(1).strip().replace('"', '').replace("'", "")
                validated_data['h1'] = h1
                validated_data['slug'] = h1 
            elif line.startswith("2. Title:") and match:
                validated_data['title'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("3. Description:") and match:
                validated_data['description'] = match.group(1).strip().replace('"', '').replace("'", "")
        
        print("генерация прошла успешно!")
        return validated_data
    
    except Exception as e:
        print(f"Ошибка: {e}")
        validated_data['h1'] = "default-h1"
        validated_data['slug'] = "default-slug"
        validated_data['title'] = "Заголовок по умолчанию"
        validated_data['description'] = "Описание по умолчанию"
        return validated_data

def generations_for_appeals(validated_data):
    formatted_request = (
        "На основе следующего текста обращения сгенерируйте:\n"
        "1. H1 (заголовок): Напишите заголовок H1 от {min_h1} до {max_h1} символов, используя транслит через дефисы (например: 'primer-teksta-dlya-zagolovka').\n"
        "2. Title (заголовок для SEO): Напишите заголовок Title на русском языке, длиной от {min_title} до {max_title} символов.\n"
        "3. Description (описание): Напишите описание на русском языке, длиной от {min_description} до {max_description} символов.\n"
        "\nТекст обращения:\n{content}"
    ).format(
        min_h1=Constants.MIN_LEN_H1,
        max_h1=Constants.MAX_LEN_H1,
        min_title=Constants.MIN_LEN_TITLE,
        max_title=Constants.MAX_LEN_TITLE,
        min_description=Constants.MIN_LEN_DESCRIPTION,
        max_description=Constants.MAX_LEN_DESCRIPTION,
        content=validated_data.get('text', '') 
    ) 
    client = Client()
    try:
        generated_content = generate_with_retry(client, formatted_request)
        quote_pattern = r"^.*?:\s*[\"']?(.*?)[\"']?$"
        lines = generated_content.split('\n')
        for line in lines:
            match = re.search(quote_pattern, line)
            if line.startswith("1. H1:") and match:
                h1 = match.group(1).strip().replace('"', '').replace("'", "")
                validated_data['h1'] = h1
                validated_data['slug'] = h1 
            elif line.startswith("2. Title:") and match:
                validated_data['title'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("3. Description:") and match:
                validated_data['description'] = match.group(1).strip().replace('"', '').replace("'", "")
        
        print("генерация прошла успешно!")
        return validated_data

    except Exception as e:
        print(f"Ошибка: {e}")
        validated_data['h1'] = "default-h1"
        validated_data['slug'] = "default-slug"
        validated_data['title'] = "Заголовок по умолчанию"
        validated_data['description'] = "Описание по умолчанию"
        return validated_data

def generations_for_biography(validated_data):
    print("генерация...")
    formatted_request = (
        "На основе следующего текста биографии сгенерируйте:\n"
        "1. H1 (заголовок): Напишите заголовок H1 от {min_h1} до {max_h1} символов, используя транслит через дефисы (например: 'primer-teksta-dlya-zagolovka').\n"
        "2. Title (заголовок для SEO): Напишите заголовок Title на русском языке, длиной от {min_title} до {max_title} символов.\n"
        "3. Description (описание): Напишите описание на русском языке, длиной от {min_description} до {max_description} символов.\n"
        "\nТекст биографии:\n{content}"
    ).format(
        min_h1=Constants.MIN_LEN_H1,
        max_h1=Constants.MAX_LEN_H1,
        min_title=Constants.MIN_LEN_TITLE,
        max_title=Constants.MAX_LEN_TITLE,
        min_description=Constants.MIN_LEN_DESCRIPTION,
        max_description=Constants.MAX_LEN_DESCRIPTION,
        content=validated_data.get('content', '')
    )
    
    client = Client()
    try:
        generated_content = generate_with_retry(client, formatted_request)
        quote_pattern = r"^.*?:\s*[\"']?(.*?)[\"']?$"
        lines = generated_content.split('\n')
        for line in lines:
            match = re.search(quote_pattern, line)
            if line.startswith("1. H1:") and match:
                h1 = match.group(1).strip().replace('"', '').replace("'", "")
                validated_data['h1'] = h1
                validated_data['slug'] = h1 
            elif line.startswith("2. Title:") and match:
                validated_data['title'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("3. Description:") and match:
                validated_data['description'] = match.group(1).strip().replace('"', '').replace("'", "")
        
        print("генерация прошла успешно!")
        return validated_data
    
    except Exception as e:
        print(f"Ошибка: {e}")
        validated_data['h1'] = "default-h1"
        validated_data['slug'] = "default-slug"
        validated_data['title'] = "Заголовок по умолчанию"
        validated_data['description'] = "Описание по умолчанию"
        return validated_data
