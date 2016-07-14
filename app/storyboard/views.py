from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from app.storyboard.models import *
from django.http import JsonResponse
import json
from django.forms.models import model_to_dict

# Create your views here.

def main(request):
    ctx = {
            'paragraphs' : Paragraph.objects.filter(is_first = True).order_by('-pub_date'),
            'header_title' : "Story Street",
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
    text_array = request.POST['text'].replace("\r","").replace('<h2>','<div><br></div><h2>').replace(' style="line-height: 28.5714px;"','').replace('<span><br></span>','<br>').replace('<span>','').replace('</span>','').split('<div><br></div><div><br></div>')
    text_array = [x for x in text_array if len(x)>0 and x!="<div>"]
    prev_p = request.POST.get('prev_p', None)
    start_i = 0
    is_userfirst = True
    novel = None
    if prev_p ==None:
        new_novel = Novel(title = title, writer = user)
        new_novel.save()
        new_p = Paragraph(text = text_array[start_i], novel = new_novel, writer = user,is_first = True, is_userfirst = is_userfirst, is_parallelfirst = True, is_parallellast = True)
        new_p.save()
        is_userfirst = False
        prev_p = new_p
        start_i +=1
    else:
        prev_p = Paragraph.objects.get(id = prev_p)
        novel = prev_p.novel
        #prev_p = prev_p.prev_paragraph
    """
    if prev_p == None:
        try:
            parallel_last = novel.paragraph_set.get(is_first = True, is_parallellast = True)
            parallel_count = parallel_last.index
            parallel_exists = True
            parallel_last.is_parallellast = False
            parallel_last.save()
        except:
            parallel_exists = False
            parallel_count = 0
        new_p = Paragraph(text = text_array[start_i], novel = novel, writer = user, is_first = True, is_userfirst = is_userfirst, index = parallel_count+1, is_parallellast = True, is_parallelfirst = not parallel_exists)
        new_p.save()
        is_userfirst = False
        prev_p = new_p
        start_i +=1
    """

    for i in range(start_i,len(text_array)):
        try:
            parallel_last = prev_p.next_paragraph_set.get(is_parallellast = True)
            parallel_count = parallel_last.index
            parallel_exists = True
            parallel_last.is_parallellast = False
            parallel_last.save()
        except:
            parallel_exists = False
            parallel_count = 0


        new_p = Paragraph(prev_paragraph = prev_p, text = text_array[i], novel = prev_p.novel, writer = user, is_userfirst = is_userfirst, index = parallel_count+1, is_parallellast = True, is_parallelfirst = not parallel_exists)
        new_p.save()
        is_userfirst = False
        prev_p = new_p

    return redirect('/')

def novel_view(request, para_id):
    paragraphs = []
#    novel = Novel.objects.get(id=novel_id)
 #   cursor = novel.paragraph_set.filter(is_first = True).order_by('pub_date')
    cursor = Paragraph.objects.filter(id = para_id);
    novel = cursor[0].novel;
    while cursor.exists():
        paragraphs.append(cursor[0])
        cursor = cursor[0].next_paragraph_set.all()
    ctx = {
        'paragraphs' : paragraphs,
        'novel' : novel,
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

def team_view(request):
    return render(request, 'storyboard/team.html')

def profile_view(request, user_name):
    user = User.objects.get(username = user_name)
    ctx = {
            'paragraphs' : user.paragraph_set.filter(is_userfirst = True).order_by('-pub_date'),
            'header_title' : user.username,
    }
    return render(request, 'storyboard/main.html', ctx)


def test_view(request):
    return render(request, 'storyboard/test.html')

def like(request):
    user = request.user
    prev_p = request.GET.get('prev_p', None)
    target_p = Paragraph.objects.get(id=prev_p)
    status = 0
    if LikeCheck.objects.filter(paragraph=target_p, user = user).exists():
        status = 0
    else:
        target_p.like_all()
        likecheck = LikeCheck(user = user, paragraph = target_p)
        likecheck.is_up = True
        likecheck.save()
        status = 1
    ctx={
        'state':status,
            }
    return JsonResponse(json.dumps(ctx),safe=False)
def like_check(request):
    user = request.user
    prev_p = request.GET.get('prev_p', None)
    target_p = Paragraph.objects.get(id=prev_p)
    status = 0
    if LikeCheck.objects.filter(paragraph=target_p, user = user).exists():
        status = 1
    else:
        status = 0
    ctx={
        'state':status,
            }
    return JsonResponse(json.dumps(ctx),safe=False)

