import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .exam_models import Chat

@method_decorator(csrf_exempt, name='dispatch')
class ChatView(View):
    def get(self, request):
        # Retrieve all chat messages
        chats = Chat.objects.all()
        chat_data = [
            {
                "username": chat.username,
                "chat_message": chat.chat_message,
                "date": chat.date.isoformat()
            }
            for chat in chats
        ]
        return JsonResponse(chat_data, safe=False)

    def post(self, request):
        try:
            # Debugging: Print raw request body
            print("Raw request body:", request.body)

            data = json.loads(request.body.decode('utf-8'))

            print("Parsed JSON:", data)  # Debugging

            username = data.get("username")
            chat_message = data.get("chat_message")

            if not username or not chat_message:
                return JsonResponse({"error": "Username and message are required."}, status=400)

            new_chat = Chat.objects.create(username=username, chat_message=chat_message)

            return JsonResponse({
                "username": new_chat.username,
                "chat_message": new_chat.chat_message,
                "date": new_chat.date.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
