from g4f.client import Client
from django.http import JsonResponse
import json
import re
from base.constants import Constants

def generations_for_news(data: dict):
    if not data.get('h1') or not data.get('title') or not data.get('description'):
            formatted_request = (
                "На основе следующего текста новости сгенерируйте:\n"
                "1. H1 (заголовок): Напишите заголовок H1 от {min_h1} до {max_h1} символов, используя транслит через дефисы (например: 'zagadka-s-privet').\n"
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
                content=data.get('content', '')
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
                    data['h1'] = match.group(1).strip()
                elif line.startswith("2.") and match:
                    data['title'] = match.group(1).strip()
                elif line.startswith("3.") and match:
                    data['description'] = match.group(1).strip()
            return data