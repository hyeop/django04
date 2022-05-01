from django.shortcuts import render,redirect
from .models import Board
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages

def unlikey(req, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(req.user)
    return redirect("board:detail", bpk)


def likey(req, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(req.user)
    return redirect("board:detail", bpk)

def index(req):
    pg = req.GET.get("page", 1)
    cate = req.GET.get("cate", "")
    kw = req.GET.get("kw", "")
    
    
    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u)
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(content__contains=kw)
        else:
            b = Board.objects.all()
    else:
        b = Board.objects.all()




    # Paginator(A,B)
    # A : 레코드들   B : 단위
    pag = Paginator(b,10)
    obj = pag.get_page(pg)

    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw
    }
    return render(req, "board/index.html", context)


# Create your views here.
def update(req, bpk):
    b = Board.objects.get(id=bpk)

    if req.user != b.writer:
        messages.error(req, "너 혼나!")
        return redirect("board:index")

    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        b.subject = s
        b.content = c
        b.save()
        return redirect("board:detail", bpk)
    context = {
        "b": b
    }
    return render(req, "board/update.html", context)

def create(req):
    if req.method == "POST":
        s = req.POST.get("sub")
        c = req.POST.get("con")
        t = timezone.now()
        Board(subject=s, writer=req.user, content=c, pubdate=t).save()
        return redirect("board:index")
    return render(req, "board/create.html")


def delete(req, bpk):
    b = Board.objects.get(id=bpk)
    if req.user == b.writer:
        b.delete()
    else:
        messages.error(req, "너 혼나!")

    return redirect("board:index")

def detail(req, bpk):
    b = Board.objects.get(id=bpk)
    context = {
        "b" : b
    }
    return render(req, "board/detail.html", context)


