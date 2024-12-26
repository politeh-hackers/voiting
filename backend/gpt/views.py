import openai
from django.http import JsonResponse

# Укажи свой API-ключ
openai.api_key = "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"

def generate_response(request):
    if request.method == "POST":
        user_input = request.POST.get("user_input", "")
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=user_input,
                max_tokens=150
            )
            return JsonResponse({"response": response.choices[0].text.strip()})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)
