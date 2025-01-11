from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Message, MessageHistory, Notification

# Create your views here.
def view_message_history(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    history = message.history.all()
    return render(request, 'message_history.html', {'message': message, 'history': history})