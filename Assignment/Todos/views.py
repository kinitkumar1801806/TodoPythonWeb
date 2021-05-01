from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customers,Moderators,Todos
from .serializers import CustomersSerializers,ModeratorsSerializers,TodosSerializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from webpush import send_user_notification
import json
import requests

# Since in this web we are using the django authentication to login 
#so password validation and strength matters
#password should be of length >8 and contain atleast 1 small letter and 1 capital ;letter and 1 special character

#we store username and password normally without using REST Framework as our main focus is on handling todos using REST Framework

#for customers login
def clogin(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('ctodos')
        user=User.objects.create_user(username=username,password=password)
        user.save()
        customer=Customers(customer=user)
        customer.save()        
        return redirect('ctodos')
    return HttpResponse("Failure")

#for moderators login
def mlogin(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('mtodos')
        user=User.objects.create_user(username=username,password=password)
        user.save()
        moderator=Moderators(moderator=user)
        moderator.save()
        return redirect('mtodos')
    return HttpResponse("Failure")   


# Handling post ,put and get request of todos using REST Framework
class todos(APIView):
    def get(self, request,id):
        todos1=Todos.objects.all()
        serializer=TodosSerializers(todos1,many=True)
        return Response(serializer.data)
    def put(self,request,id):
        todos = Todos.objects.get(id=int(id))
        serializer = TodosSerializers(todos, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self,request,id):
        serializer=TodosSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#displaying Todos for Customers
def cTodos(request):
    response = requests.get('http://127.0.0.1:8000/electura/todos/0')#0 stands for all
    created=False
    completed=False
    data = response.json()
    for d in data:
        if d['Status'] and d['Customer']==request.user.username:
            completed=True
        elif not d['Status'] and d['Customer']==request.user.username:
            created=True
    muser=Moderators.objects.all()
    return render(request,"Customer_Todos.html",{'todos':data,'muser':muser,'created':created,'completed':completed,'username':request.user.username})


#displaying Todos for moderators
def mTodos(request):
    response = requests.get('http://127.0.0.1:8000/electura/todos/0')
    data = response.json()
    assigned=False
    finished=False
    for d in data:
        if d['Status'] and d['Moderators']==request.user.username:
            finished=True
        elif not d['Status'] and d['Moderators']==request.user.username:
            assigned=True
    return render(request,"Moderator_Todos.html",{'todos':data,'assigned':assigned,'finished':finished,'username':request.user.username})

#Recieving the form data of todo
def addTodo(request):
    if request.method=='POST':
        title=request.POST.get('title','')
        musername=request.POST.get('musername','')
        description=request.POST.get('description','')
        cusername=request.user.username
        muser=Moderators.objects.all()
        for m in muser:
            if m.moderator.username==musername:
                post_data={'Customer':cusername,'Moderators':musername,'title':title,'description':description,'Status':False}
                response = requests.post('http://127.0.0.1:8000/electura/todos/0', data=post_data)
                payload = {"head": "You have a new Task ", "body": title+"\n"+description+"\n"+"Assigned By : "+request.user.username}
                push_notification(m.moderator,payload)
                return redirect('ctodos')
        return HttpResponse("Failure! Please enter a valid moderator username")

#user logout function
def logout1(request):
    logout(request)
    return redirect('home')

# function to mark a task completed
def markComplete(request,id):
    if request.method=='POST':
        title=request.POST.get('title','')
        musername=request.POST.get('moderator','')
        description=request.POST.get('description','')
        cusername=request.POST.get('customer','')
    put_data = {'Customer':cusername,'Moderators':musername,'title':title,'description':description,'Status':True}
    response = requests.put('http://127.0.0.1:8000/electura/todos/'+str(id), data=put_data)
    payload = {"head": "Task Completed", "body": title+"\n"+description+"\n"+"Complted by : "+request.user.username}
    cuser=Customers.objects.all()
    for c in cuser:
        if c.customer.username==cusername:
            push_notification(c.customer,payload)
    return redirect('mtodos')

#To send notification
def push_notification(user,payload):
    print(user)
    send_user_notification(user=user,payload=payload,ttl=1000)