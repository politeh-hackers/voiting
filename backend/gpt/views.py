from g4f.client import Client
from django.http import JsonResponse
import json

def generate(request):
    if request.method == "POST":
        body = json.loads(request.body)
        user_input = body.get("user_input", "")
        client = Client()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_input}],
            web_search=False
        )
        reply_content = response.choices[0].message.content
        return JsonResponse({"response": reply_content.strip()})

