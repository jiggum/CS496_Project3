from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.storyboard.models import *
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict

# Create your views here.

def main(request):
    ctx = {
            'novels' : Novel.objects.all(),
    }
    return render(request, 'storyboard/main.html',ctx)

@login_required(login_url='/session/login/')
def insert_view(request):
    prev_p = request.POST.get('prev_p', None)
    try:
        novel_title = Paragraph.objects.get(id = prev_p).novel.title
        prev_text = Paragraph.objects.get(id = prev_p).text
    except:
        novel_title = "Title"
        prev_text = "Text"
    ctx = {
            'prev_p' : prev_p,
            'novel_title' : novel_title,
            'prev_text' : prev_text,
    }
    return render(request, 'storyboard/insert.html',ctx)

def insert(request):
    user = request.user
    title = request.POST['title']
    text_array = request.POST['text'].replace("\r","").split("\n\n")
    prev_p = request.POST.get('prev_p', None)
    start_i = 0
    is_userfirst = True
    novel = None
    if prev_p ==None:
        new_novel = Novel(title = title, writer = user)
        new_novel.save()
        new_p = Paragraph(text = text_array[start_i], novel = new_novel, writer = user,is_first = True, is_userfirst = is_userfirst)
        new_p.save()
        is_userfirst = False
        prev_p = new_p
        start_i +=1
    else:
        prev_p = Paragraph.objects.get(id = prev_p)
        novel = prev_p.novel
        prev_p = prev_p.prev_paragraph
    if prev_p == None:
        new_p = Paragraph(text = text_array[start_i], novel = novel, writer = user, is_first = True, is_userfirst = is_userfirst, index = novel.paragraph_set.filter(is_first = True).count()+1)
        new_p.save()
        is_userfirst = False
        prev_p = new_p
        start_i +=1

    for i in range(start_i,len(text_array)):
        new_p = Paragraph(prev_paragraph = prev_p, text = text_array[i], novel = prev_p.novel, writer = user, is_userfirst = is_userfirst, index = prev_p.next_paragraph_set.count()+1)
        new_p.save()
        is_userfirst = False
        prev_p = new_p

    return redirect('/')

def novel_view(request, novel_id):
    paragraphs = []
    novel = Novel.objects.get(id=novel_id)
    cursor = novel.paragraph_set.filter(is_first = True).order_by('pub_date')
    while cursor.exists():
        paragraphs.append(cursor[0])
        cursor = cursor[0].next_paragraph_set.all()
    ctx = {
        'novel' : novel,
        'paragraphs' : paragraphs,
    }

    return render(request, 'storyboard/novel.html',ctx)

def get_parallel_story_json(request):
    prev_p = Paragraph.objects.get(id = request.GET['phid'])
    paragraphs = []
    if request.GET['direction'] == "prev":
        direction = -1
    else:
        direction = 1
    if prev_p.is_first:
        cursor = prev_p.novel.paragraph_set.filter(is_first = True, index = (prev_p.index+direction-1)%prev_p.novel.paragraph_set.filter(is_first = True).count()+1)
    else:
        cursor = prev_p.prev_paragraph.next_paragraph_set.filter(index = (prev_p.index+direction-1)%prev_p.prev_paragraph.next_paragraph_set.all().count()+1)

    while cursor.exists():
        paragraphs.append(model_to_dict(cursor[0]))
        cursor = cursor[0].next_paragraph_set.all()
    ctx = {
        'paragraphs' : paragraphs,
    }

    return JsonResponse(json.dumps(ctx),safe=False)