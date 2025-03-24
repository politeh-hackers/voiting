from g4f.client import Client
import re
from base.constants import Constants


def validate_generated_content(content):
    lines = content.split('\n')
    if len(lines) < 3:
        return False 
    if not (lines[0].startswith("1. Slug:") and
            lines[1].startswith("2. H1:") and
            lines[2].startswith("3. Title:") and
            lines[3].startswith("4. Description:")):
        return False
    return True

def generate_with_retry(client, formatted_request, max_retries=10):
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
                print(generated_content)
                print(f"Попытка {attempt + 1}: Ответ GPT не соответствует формату. Повторная генерация...")
        except Exception as e:
            print(f"Попытка {attempt + 1}: Ошибка при генерации: {e}")
    raise ValueError("Не удалось получить корректный ответ после нескольких попыток")


def generations_for_news(validated_data):
    print("генерация...")
    formatted_request = (
        "На основе следующего текста новости сгенерируйте строго без любых спецсимволов (включая кавычки, звездочки, подчеркивания и т.п.) только:\n"
        "1. Slug для URL: транслит на латиницу через дефисы, длина {min_h1}-{max_h1} символов. Пример: primer-teksta-dlya-url\n"
        "2. H1 заголовок: на русском, длина {min_h1}-{max_h1} символов. Пример: Пример заголовка H1\n"
        "3. Title для SEO: на русском, длина {min_title}-{max_title} символов. Пример: Пример заголовка Title\n"
        "4. Description: на русском, длина {min_description}-{max_description} символов. Пример: Пример описания для SEO\n"
        "Формат ответа ТОЛЬКО так:\n"
        "1. Slug: пример-sluga-dlya-url\n"
        "2. H1: Пример заголовка H1\n"
        "3. Title: Пример заголовка Title\n"
        "4. Description: Пример описания для SEO\n"
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
        quote_pattern = r"^.*?:\s*[^a-zA-Zа-яА-Я\-]*(.*?)[^a-zA-Zа-яА-Я\-]*$"
        lines = generated_content.split('\n')
        for line in lines:
            match = re.search(quote_pattern, line)
            if line.startswith("1. Slug:") and match:
                validated_data['slug'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("2. H1:") and match:
                validated_data['h1'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("3. Title:") and match:
                validated_data['title'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("4. Description:") and match:
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
    print("генерация...")
    formatted_request = (
        "На основе следующего текста обращения сгенерируйте строго без любых спецсимволов (включая кавычки, звездочки, подчеркивания и т.п.) только:\n"
        "1. Slug для URL: транслит на латиницу через дефисы, длина {min_h1}-{max_h1} символов. Пример: primer-teksta-dlya-url\n"
        "2. H1 заголовок: на русском, длина {min_h1}-{max_h1} символов. Пример: Пример заголовка H1\n"
        "3. Title для SEO: на русском, длина {min_title}-{max_title} символов. Пример: Пример заголовка Title\n"
        "4. Description: на русском, длина {min_description}-{max_description} символов. Пример: Пример описания для SEO\n"
        "Формат ответа ТОЛЬКО так:\n"
        "1. Slug: пример-sluga-dlya-url\n"
        "2. H1: Пример заголовка H1\n"
        "3. Title: Пример заголовка Title\n"
        "4. Description: Пример описания для SEO\n"
        "\nТекст обращения:\n{text}"
    ).format(
        min_h1=Constants.MIN_LEN_H1,
        max_h1=Constants.MAX_LEN_H1,
        min_title=Constants.MIN_LEN_TITLE,
        max_title=Constants.MAX_LEN_TITLE,
        min_description=Constants.MIN_LEN_DESCRIPTION,
        max_description=Constants.MAX_LEN_DESCRIPTION,
        text=validated_data.get('text', '')
    )
    
    client = Client()
    try:
        generated_content = generate_with_retry(client, formatted_request)
        print(generated_content)
        quote_pattern = r"^.*?:\s*[^a-zA-Zа-яА-Я\-]*(.*?)[^a-zA-Zа-яА-Я\-]*$"
        lines = generated_content.split('\n')
        for line in lines:
            match = re.search(quote_pattern, line)
            if line.startswith("1. Slug:") and match:
                validated_data['slug'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("2. H1:") and match:
                validated_data['h1'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("3. Title:") and match:
                validated_data['title'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("4. Desription:") and match:
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
        "На основе следующего текста биографии сгенерируйте строго без любых спецсимволов (включая кавычки, звездочки, подчеркивания и т.п.) только:\n"
        "1. Slug для URL: транслит на латиницу через дефисы, длина {min_h1}-{max_h1} символов. Пример: primer-teksta-dlya-url\n"
        "2. H1 заголовок: на русском, длина {min_h1}-{max_h1} символов. Пример: Пример заголовка H1\n"
        "3. Title для SEO: на русском, длина {min_title}-{max_title} символов. Пример: Пример заголовка Title\n"
        "4. Description: на русском, длина {min_description}-{max_description} символов. Пример: Пример описания для SEO\n"
        "Формат ответа ТОЛЬКО так:\n"
        "1. Slug: пример-sluga-dlya-url\n"
        "2. H1: Пример заголовка H1\n"
        "3. Title: Пример заголовка Title\n"
        "4. Description: Пример описания для SEO\n"
        "\nТекст биографии:\n{text}"
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
        print(generated_content)
        quote_pattern = r"^.*?:\s*[^a-zA-Zа-яА-Я\-]*(.*?)[^a-zA-Zа-яА-Я\-]*$"
        lines = generated_content.split('\n')
        for line in lines:
            match = re.search(quote_pattern, line)
            if line.startswith("1. Slug:") and match:
                validated_data['slug'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("2. H1:") and match:
                validated_data['h1'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("3. Title:") and match:
                validated_data['title'] = match.group(1).strip().replace('"', '').replace("'", "")
            elif line.startswith("4. Description:") and match:
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
