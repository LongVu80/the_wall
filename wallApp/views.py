from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def login(request):
    user = User.objects.filter(username = request.POST['username'])
    if user:
        userLogin = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), userLogin.password.encode()):
            request.session['user_id'] = userLogin.id
            messages.success(request, "you have successfully logged in!!")
            return redirect('/success/')
        messages.error(request, 'Invalid Username or Password!')
        return redirect ('/')
    messages.error(request, 'That username is not in our system, please check the spelling or register for an account.')
    return redirect('/')


def register(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for err in errors.values():
            messages.error(request, err)
        return redirect ('/')
    hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    newUser = User.objects.create(
        firstName = request.POST['firstName'],
        lastName = request.POST['lastName'],
        email = request.POST['email'],
        username = request.POST['username'],
        password = hashedPw
    )
    request.session['user_id'] = newUser.id
    return redirect('/success/')


def logout(request):
    request.session.clear()
    return redirect ('/')


def success(request):
    if 'user_id' in request.session:
        context = {
            'name' : User.objects.get(id=request.session['user_id']),
            'messages' : Message.objects.all().order_by('-created_at')
        }
        return render(request, 'wall.html', context)
    return redirect ('/')

def message(request):
    Message.objects.create(
        message = request.POST['message'], 
        user = User.objects.get(id=request.session['user_id']))
    return redirect('/success/')

def comment(request):
    print(request.POST['message_id'])
    Comment.objects.create(
        comment = request.POST['comment'], 
        user = User.objects.get(id=request.session['user_id']), 
        message = Message.objects.get(id = request.POST['message_id'])
    )
    return redirect('/success/')

def deleteMessage(request, message_id):
    messageDelete = Message.objects.get(id = message_id)
    if messageDelete.user.id == request.session['user_id']:
        messageDelete.delete()
        return redirect('/success/')
    return redirect('/success/')

def deleteComment(request, comment_id):
    commentDelete = Comment.objects.get(id= comment_id)
    if commentDelete.user.id == request.session['user_id']:
        commentDelete.delete()
        return redirect('/success/')
    return redirect('/success/')