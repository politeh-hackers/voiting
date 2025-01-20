from g4f.client import Client
import re
from biography.models import Biography
from base.constants import Constants
from media.models import Media
from actual.models import Actual
from appeals.models import Appeal

def generations_for_news(validated_data):
    if not validated_data.get('h1') or not validated_data.get('title') or not validated_data.get('description'):

        if Media or Actual:
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
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": formatted_request}],
                web_search=False
            )
            generated_content = response.choices[0].message.content.strip()
            print(generated_content)
            quote_pattern = r"^.*?:\s*(.*)"
            lines = generated_content.split('\n')
            for line in lines:
                match = re.search(quote_pattern, line)
                if line.startswith("1.") and match:
                    validated_data['h1'] = match.group(1).strip()
                elif line.startswith("2.") and match:
                    validated_data['title'] = match.group(1).strip()
                elif line.startswith("3.") and match:
                    validated_data['description'] = match.group(1).strip()
            return validated_data

        if Appeal:
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
                content=validated_data.get('text', '') and validated_data.get('photos', '')
            )
            client = Client()
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": formatted_request}],
                web_search=False
            )
            generated_content = response.choices[0].message.content.strip()
            print(generated_content)
            quote_pattern = r"^.*?:\s*(.*)"
            lines = generated_content.split('\n')
            for line in lines:
                match = re.search(quote_pattern, line)
                if line.startswith("1.") and match:
                    validated_data['h1'] = match.group(1).strip()
                elif line.startswith("2.") and match:
                    validated_data['title'] = match.group(1).strip()
                elif line.startswith("3.") and match:
                    validated_data['description'] = match.group(1).strip()
            return validated_data

        if Biography:
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
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": formatted_request}],
                web_search=False
            )
            generated_content = response.choices[0].message.content.strip()
            print(generated_content)
            quote_pattern = r"^.*?:\s*(.*)"
            lines = generated_content.split('\n')
            for line in lines:
                match = re.search(quote_pattern, line)
                if line.startswith("1.") and match:
                    validated_data['h1'] = match.group(1).strip()
                elif line.startswith("2.") and match:
                    validated_data['title'] = match.group(1).strip()
                elif line.startswith("3.") and match:
                    validated_data['description'] = match.group(1).strip()
            return validated_data