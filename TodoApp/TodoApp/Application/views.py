import http
import os.path
from wsgiref.util import FileWrapper

from django.http import HttpResponseRedirect, FileResponse, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.urls.base import reverse
import mimetypes
from TodoApp import Application
from TodoApp.Application.forms import CreateAssignmentForm
from TodoApp.Application.models import Assignment
from TodoApp.settings import MEDIA_ROOT


# Create your views here.



def index_view(request):
    if request.method == "GET":
        todos = Assignment.objects.all()
    context = {
        'todos': todos,
    }
    return render(request, template_name='index.html', context=context, status=200)

def create_todo(request):
    if request.method == 'GET':
        form = CreateAssignmentForm()
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST)
        if form.is_valid():
            offer = form.save()
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'create-todo.html', context=context)

def edit_todo(request, pk):
    todo = Assignment.objects.get(pk=pk)
    form = CreateAssignmentForm( instance=todo)
    if request.method == 'POST':
        form = CreateAssignmentForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form,
        'pk': pk,
    }
    return render(request, 'edit-todo.html', context=context, status=200)

def delete_todo(request, pk):
    item = Assignment.objects.get(pk=pk)
    item.delete()
    return HttpResponseRedirect(reverse('index'))

def download(reqeust):
    todos = Assignment.objects.all()
    filepath = str(MEDIA_ROOT) + '/tasks.txt'
    with open(filepath, 'w+') as f:
        for i in range(len(todos)):
            f.write(f"{i + 1}. " + str(todos[i]) + '\n')
        f.close()
    filename = 'tasks.txt'
    path = open(filepath, 'r')
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response['Content-Description'] = "attachment; filename=%s" % filename
    return response

