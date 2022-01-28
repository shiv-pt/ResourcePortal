from django.shortcuts import redirect, render
from django.core.paginator import Paginator

from user_view.models import Member, issues
from material.models import Material

def adminissue(request):
    issue = issues.objects.all()
    paginator = Paginator(issue, 10)
    page = request.GET.get('page')
    issue = paginator.get_page(page)
    return render(request, 'address.html', {'issues': issue})
    
def adminflag(request):
    material = Member.objects.raw('SELECT * FROM member A, material B, member_report C WHERE A.usn = C.member_id AND C.material_id = B.id')
    paginator = Paginator(material, 10)
    page = request.GET.get('page')
    material = paginator.get_page(page)
    return render(request, 'flags.html', {'issues': material})

def address_issues(request,id,act):
    obj = issues.objects.filter(issue_id = id).update(issue_status=act)
    return redirect('/adminissue')

def issue_delete(request,id):
    print(id)
    issue=issues.objects.get(issue_id=id)
    issue.delete()
    return redirect("/issuestatus")
