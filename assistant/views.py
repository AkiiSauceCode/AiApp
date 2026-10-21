import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from google import genai


def index(request):
    return render(request, 'assistant/index.html')


@csrf_exempt
def ask_gemini(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "POST request required."},
            status=405
        )

    try:

        data = json.loads(request.body)

        prompt = data.get("prompt", "").strip()

        if not prompt:
            return JsonResponse(
                {"error": "Please enter a question."},
                status=400
            )

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return JsonResponse(
                {"error": "Gemini API key is not configured."},
                status=500
            )

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return JsonResponse({
            "response": response.text
        })

    except Exception as e:

        return JsonResponse({
            "error": str(e)
        }, status=500)