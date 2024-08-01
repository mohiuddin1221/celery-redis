from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import MessageBord, Message
import threading
from .forms import MessageModelFrom
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.contrib.auth.models import User
from .tasks import *
@login_required
def messagebord_view(request):
    messagebord = get_object_or_404(MessageBord, id=1)
    form = MessageModelFrom()
    if request.method == 'POST':
        if request.user in messagebord.suscribers.all():
            form = MessageModelFrom(request.POST)
            if form.is_valid():
                message = form.save(commit=False)
                message.author = request.user
                message.message = messagebord  # Correctly assign the instance
                message.save()
                send_email(message)
                messages.success(request, 'Message posted successfully')
            else:
                messages.error(request, 'There was an error in the form')
        else:
            messages.warning(request, 'You need to be subscribed')
        return redirect('messagebord-view')  # Ensure the URL name matches your urlpatterns
    
    context = {
        'messagebord': messagebord,
        'form': form
    }
    return render(request, 'a_messagebord/index.html', context)


@login_required
def subscribe(request):
    messagebord = get_object_or_404(MessageBord,id=1)


    if request.user not in messagebord.suscribers.all():
        messagebord.suscribers.add(request.user)
    else:
        messagebord.suscribers.remove(request.user)
    return redirect('messagebord-view')


def send_email(message):
    messageboard = message.message
    subscribers = messageboard.suscribers.all()
    for subscriber in subscribers:
        subject = f'New Message from {message.author.username}'
        body = f'{message.author.username}: {message.body}\n\nRegards from\nMy Message Board'
        send_email_task(subject, body, subscriber.email)

#         email_thread = threading.Thread(target=send_email_thread, args=(subject, body, subscriber))
#         email_thread.start()

# def send_email_thread(subject, body, subscriber):
#         email = EmailMessage(subject, body, to=[subscriber.email])
#         email.send()
#         return HttpResponse('Emails sent successfully')