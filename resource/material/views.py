from django.shortcuts import render,redirect

from material.models import Material
from user_view.models import Member

# Create your views here.


def upload_material(request):
    if request.user.is_authenticated == False:
        return redirect('/login/')
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        type = request.POST['type']
        semester = request.POST['semester']
        if type == 'document':
            print('document')
            document = request.FILES['document']
            video = None
            link = None
        elif type == 'video':
            print('video')
            document = None
            video = request.FILES['video']
            link = None
        elif type == 'link':
            print('link')
            document = None
            video = None
            link = request.POST['link']
        else:
            document = None
            video = None
            link = None

        if request.FILES.get('thumbnail', False):
            thumbnail = request.FILES['thumbnail']
        else:
            thumbnail = None
        like_count = 0
        dislike_count = 0
        print(title, description, type, semester, document, video, link, like_count, dislike_count)
        material = Material(title=title, description=description, type=type, semester=semester, link=link,
                            document=document, video=video, thumbnail=thumbnail, like_count=like_count,
                            dislike_count=dislike_count)
        material.save()
        member=Member.objects.get(usn=request.user.username)
        member.material.add(material)
        return redirect('/')
    return render(request, 'material_upload.html')
