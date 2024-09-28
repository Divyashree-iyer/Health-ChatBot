from django.http import JsonResponse
from django.shortcuts import render
from .models import Conversation, Patient
from datetime import datetime
from .langchain_logic import graph
from langchain_core.messages import HumanMessage
from django.utils import timezone

def llm_response(message):
    x = graph.graph.invoke({"messages":[HumanMessage(content=message)]})
    return x['messages'][1].content


# View for chat page
def chat_view(request):
    patient = Patient.objects.first()  # Get the first (or only) patient
    
    if request.method == 'POST':
        user_message = request.POST.get('message')

        Conversation.objects.create(message=user_message, is_bot=False, timestamp=timezone.now())

        bot_reply = llm_response(user_message)
        
        bot_obj = Conversation.objects.create(message=bot_reply, is_bot=True, timestamp=timezone.now())
        return JsonResponse({'bot_reply': bot_obj.message, 'timestamp': bot_obj.timestamp})
    
    conversations = Conversation.objects.all().order_by('timestamp')
    appointment_update = 'No appointment requests at the moment.'

    return render(request, 'chat/chat.html', {
        'patient': patient,
        'conversations': conversations,
        'appointment_update': appointment_update
    })
