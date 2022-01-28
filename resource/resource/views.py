from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import HttpResponse
import os
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from user_view.models import Member
from material.models import Material
from wsgiref.util import FileWrapper
import mimetypes

def explore(request,id):
    #mat1 = Material.objects.raw('SELECT * FROM material')
    mat = Material.objects.raw('SELECT * FROM material WHERE id=%s',[id])
    print(mat[0].link==None, mat[0].document, mat[0].video)
    if(mat[0].link!=None):
        return redirect(mat[0].link)
    else:
        fs = FileSystemStorage()
        if(mat[0].document!=""):
            filename = mat[0].document
        else:
            filename = mat[0].video
        filename=str(filename)
        name=filename[12:]
        filepath = os.path.join(fs.location, filename)
        try:
            wrapper = FileWrapper(open(filepath, 'rb'))
            content_type = mimetypes.guess_type(filepath)[0]
            response = HttpResponse(wrapper, content_type=content_type)
            response['Content-Length'] = os.path.getsize(filepath)
            response['Content-Disposition'] = "attachment; filename=%s" % name
            return response
        except:
            return HttpResponse("File not found")   
    #return render(request, 'home.html', {'mat': mat1})

def refineddatat(request,mat):
    user = request.user
    member = Member.objects.get(usn=user.username)
    liked = member.likes.all()
    disliked = member.dislikes.all()
    report = member.report.all()

    lst = []
    for i in mat:
        temp = {}
        temp['id'] = i.id
        temp['title'] = i.title
        temp['description'] = i.description
        temp['type'] = i.type
        temp['thumbnail'] = i.thumbnail
        temp['semester'] = i.semester
        temp['link'] = i.link
        temp['document'] = i.document
        temp['video'] = i.video
        temp['like_count'] = i.like_count
        temp['dislike_count'] = i.dislike_count
        temp['isliked'] = False
        temp['isdisliked'] = False
        temp['isreported'] = False

        lst.append(temp)

        for i in liked:
            for j in lst:
                if(i.id == j['id']):
                    j['isliked'] = True
        for i in disliked:
            for j in lst:
                if(i.id == j['id']):
                    j['isdisliked'] = True
        for i in report:
            for j in lst:
                if(i.id == j['id']):
                    j['isreported'] = True
        for i in lst:
            print(i['isliked'], i['isdisliked'], i['isreported'])
    return lst


def home(request):
    mat = Material.objects.all()
    if request.user.is_authenticated==False:
        print("not logged in")
        render(request, 'home.html', {'mat': mat})
    
    return render(request, 'home.html', {'mat': mat})
    

def userLogout(request):
    logout(request)
    return redirect('/')


def userLogin(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_ob = User.objects.filter(username=username).first()
        print(user_ob)

        if user_ob is None:
            msg = {'msg': 'User does not exist'}
            print(msg)
            return render(request, 'login_register.html', { "msg": msg, "page": page })

        user = authenticate(username=username, password=password)
        print(user)
        if user is None:
            msg = {'msg': 'Invalid Credentials'}
            print(msg)
            return render(request,'login_register.html', {'msg': msg, "page": page})

        login(request, user)
        return redirect('/')
    return render(request, 'login_register.html', {'page': page})


def userRegister(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        if User.objects.filter(email=email).first() is not None:
            msg = {'msg': 'Email already exists'}
            print(msg)
            return render(request, 'login_register.html', {'msg2': msg, "page": "register"})
        elif User.objects.filter(username=username).first() is not None:
            msg = {'msg': 'Username already exists'}
            print(msg)
            return render(request, 'login_register.html', {'msg2': msg, "page": "register"})
        else:
            user_ob = User.objects.create(
                username=username, email=email, first_name=first_name, last_name=last_name)
            user_ob.set_password(password)
            user_ob.save()
            login(request, user_ob)
            member=Member.objects.create(usn=username,first_name=first_name,last_name=last_name,email=email)
            member.save()
            return redirect('/')
    return render(request, 'login_register.html', {'page': "register"})
