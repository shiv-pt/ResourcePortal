from django.shortcuts import render,redirect
from numpy import issubsctype

from material.models import Material
from user_view.models import notification
from user_view.models import issues
from user_view.models import Member
from django.core.paginator import Paginator

# Create your views here.

def issue_delete(request,id):
    print(id)
    issue=issues.objects.get(issue_id=id)
    issue.delete()
    return redirect("/issuestatus")

def profile(request):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    member=Member.objects.filter(usn=request.user.username).first()
    return render(request,'profile.html',{'member':member})

def youruploads(request):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    usn=request.user.username
    youruploads=Member.objects.get(usn=usn)
    youruploads=youruploads.material.all()
    print(youruploads)
    return render(request,'youruploads.html',{'youruploads':youruploads})

def issue(request):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    if request.method=='POST':
        category=request.POST['category']
        desc=request.POST['desc']
        usn=request.user.username
        member=Member.objects.get(usn=usn)
        issue=issues(category=category,desc=desc,issue_status="Pending",usn=member)
        issue.save()
        return redirect('/issuestatus/')
    return render(request,'issues.html')

def issuestatus(request):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    issue = issues.objects.filter(usn=request.user.username)
    paginator = Paginator(issue, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'issuestatus.html', {'issues': page_obj})
        
def reportedcontent(request):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    usn=request.user.username
    reportedcontent=Member.objects.get(usn=usn)
    reportedcontent=reportedcontent.report.all() 
    return render(request,'reportedcontent.html',{'reportedcontent':reportedcontent})

def notifications(request):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    usn=request.user.username
    notifications=notification.objects.filter(usn=usn)

    return render(request,'notifications.html',{'notifications':notifications})

def removenotification(request,id):
    if request.user.is_authenticated==False:
        return redirect('/login/')
    notification.objects.get(notification_id=id).delete()
    return redirect('/notifications/')

def searching(request):
    material=Material.objects.all()
    if request.method == 'POST':
        searchtext = request.POST['searchtext']
        
        searchwords=searchtext.split() 
        if len(searchwords)>0:
            matdict={}
            for word in searchwords:
                material=material.filter(title__icontains=word)
                for i in material:
                    if i in matdict.keys():
                        matdict[i] += 1
                    else:
                        matdict[i] = 1
            matdict=sorted(matdict.items(), key=lambda x: x[1], reverse=True)
            print(matdict)
            matlist=[]
            for i in matdict:
                matlist.append(i[0])

            if len(matlist)>0:
                return render(request, 'home.html', {'mat':matlist})
            else:
                return render(request, 'home.html',{'error': 'No results found'})
    
    return render(request, 'home.html', {'mat': material})
