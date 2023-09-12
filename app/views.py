from django.shortcuts import render, redirect
from .forms import *
from .models import *
from datetime import datetime
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User, Group
from django.contrib import messages
import os
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

BLOG_POSTS_PER_PAGE = 5

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='customer').exists():
                    return redirect('/')
                else:
                    return redirect('/dashboard')
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form":form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/login')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})

def home(request):
    banner = Banner.objects.all()

    return render(request, 'main/index.html', {'banner' : banner})

def blog(request, *args, **kwargs):

    def get_blog_queryset(query=None):
        queryset = []
        queries = query.split(" ") # python install 2019 = [python, install, 2019]
        for q in queries:
            posts = Artikel.objects.filter(
                    Q(title__icontains=q) | 
                    Q(description__icontains=q)
                ).distinct()

            for post in posts:
                queryset.append(post)

        return list(set(queryset))

    context = {}

	# Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date'), reverse=True)
        
    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    context['blog_posts'] = blog_posts

    return render(request, 'main/blog.html' , context)

def blogsingle(request, id):
    artikel = Artikel.objects.get(idartikel=id)

    return render(request, 'main/blog-single.html', {'artikel' : artikel})

@login_required(login_url="/login")
@permission_required("app.view_profesional", login_url="/login", raise_exception=True)
def dashboard(request):
    profesional = Profesional.objects.all().count
    worker = Worker.objects.all().count
    item = Items.objects.all().count
    artikel = Artikel.objects.all().count
    banner = Banner.objects.all().count

    return render(request, 'admin/dashboard.html', {'profesional' : profesional,
                                                    'worker': worker,
                                                    'item' : item,
                                                    'artikel' : artikel,
                                                    'banner' : banner,
                                                    'datacust' : User.objects.exclude(is_staff = 1)})

@login_required(login_url="/login")
@permission_required("app.view_profesional", login_url="/login", raise_exception=True)
def profesional(request):
    profesional = Profesional.objects.all().order_by('-idprof')

    return render(request, 'admin/viewprof.html', {'profesional' : profesional})

@login_required(login_url="/login")
@permission_required("app.view_profesional", login_url="/login", raise_exception=True)
def worker(request):
    worker = Worker.objects.all().order_by('-idworker')

    return render(request, 'admin/viewwork.html', {'worker': worker,})

@login_required(login_url="/login")
@permission_required("app.view_profesional", login_url="/login", raise_exception=True)
def item(request):
    item = Items.objects.all().order_by('-iditems')

    return render(request, 'admin/viewitem.html', {'item' : item })

@login_required(login_url="/login")
@permission_required("app.view_banner", login_url="/login", raise_exception=True)
def view_banner(request):
    banner = Banner.objects.all()

    return render(request, 'admin/viewbanner.html' , {'banner' : banner})

@login_required(login_url="/login")
@permission_required("app.add_banner", login_url="/login", raise_exception=True)
def create_banner(request):
    if request.method == 'POST':
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/viewbanner")
    else:
        form = BannerForm()

    return render(request, 'admin/createbanner.html', {"form": form})

@login_required(login_url="/login")
@permission_required("app.change_banner", login_url="/login", raise_exception=True)
def update_banner(request,id):
    banner = Banner.objects.get(idbanner=id)
    if request.method == "GET":
        return render(request, 'admin/updatebanner.html', {
            'banner' : banner
        })
    else:
        if len(request.FILES) != 0:
            if len(banner.img) > 0:
                os.remove(banner.img.path)
            banner.img = request.FILES['img']
        banner.title = request.POST['title']
        banner.description = request.POST['description']
        banner.save()
        return redirect("/viewbanner")

@login_required(login_url="/login")
@permission_required("app.delete_banner", login_url="/login", raise_exception=True)
def delete_banner(request, id):
    banner = Banner.objects.get(idbanner=id)
    banner.delete()

    return redirect("/viewbanner")

@login_required(login_url="/login")
@permission_required("app.view_artikel", login_url="/login", raise_exception=True)
def view_blog(request):
    artikel = Artikel.objects.all()
    return render(request, 'admin/viewblog.html' , {'artikel' : artikel})

@login_required(login_url="/login")
@permission_required("app.add_artikel", login_url="/login", raise_exception=True)
def create_blog(request):
    if request.method == 'POST':
        form = ArtikelForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/viewblog")
    else:
        form = ArtikelForm()

    return render(request, 'admin/createblog.html', {"form": form})

@login_required(login_url="/login")
@permission_required("app.change_artikel", login_url="/login", raise_exception=True)
def update_blog(request,id):
    artikel = Artikel.objects.get(idartikel=id)
    if request.method == "GET":
        return render(request, 'admin/updateblog.html', {
            'artikel' : artikel
        })
    else:
        if len(request.FILES) != 0:
            if len(artikel.img) > 0:
                os.remove(artikel.img.path)
            artikel.img = request.FILES['img']

        artikel.author = request.user
        artikel.title = request.POST['title']
        artikel.kategori = request.POST['kategori']
        
        parsed_date = request.POST['date']
        formatted_date = datetime.strptime(parsed_date, '%b. %d, %Y')
        artikel.date = formatted_date.strftime('%Y-%m-%d')

        artikel.description = request.POST['description']
        artikel.save()
        
        return redirect("/viewblog")

@login_required(login_url="/login")
@permission_required("app.delete_artikel", login_url="/login", raise_exception=True)
def delete_blog(request, id):
    artikel = Artikel.objects.get(idartikel=id)
    artikel.delete()

    return redirect("/viewblog")

@login_required(login_url="/login")
@permission_required("app.add_profesional", login_url="/login", raise_exception=True)
def create_prof_form(request):
    if request.method == "GET" :
        nama_pemesan = request.user.first_name

        return render(request, 'customer/formprof.html', {"nama_pemesan" : nama_pemesan,
                                                          'checkbox_checked': True})    
    else:
        author = request.user
        no_telp_pemesan = request.POST['no_telp_pemesan']
        input_datetime_str = request.POST['tanggal_ketemu']
        layanan = request.POST['layanan']
        nama_penerima = request.POST['nama_penerima']
        no_telp_penerima = request.POST['no_telp_penerima']

        parsed_datetime = datetime.strptime(input_datetime_str, "%m/%d/%Y %I:%M %p")

        tanggal_ketemu = parsed_datetime.strftime("%Y-%m-%d %H:%M")

        Profesional(
            author = author,
            no_telp_pemesan = no_telp_pemesan,
            tanggal_ketemu = tanggal_ketemu,
            layanan = layanan,
            nama_penerima = nama_penerima,
            no_telp_penerima = no_telp_penerima,
        ).save()
        messages.success(request, 'Form submission successful')

        return redirect('/createprofesional')

@login_required(login_url="/login")
@permission_required("app.add_worker", login_url="/login", raise_exception=True)
def create_work_form(request):
    if request.method == "GET" :
        nama_pemesan = request.user.first_name

        return render(request, 'customer/formwork.html', {"nama_pemesan" : nama_pemesan})    
    else:
        author = request.user
        no_telp_pemesan = request.POST['no_telp_pemesan']
        input_datetime_str = request.POST['tanggal_ketemu']
        layanan = request.POST['layanan']
        nama_penerima = request.POST['nama_penerima']
        no_telp_penerima = request.POST['no_telp_penerima']

        parsed_datetime = datetime.strptime(input_datetime_str, "%m/%d/%Y %I:%M %p")

        tanggal_ketemu = parsed_datetime.strftime("%Y-%m-%d %H:%M")

        Worker(
            author = author,
            no_telp_pemesan = no_telp_pemesan,
            tanggal_ketemu = tanggal_ketemu,
            layanan = layanan,
            nama_penerima = nama_penerima,
            no_telp_penerima = no_telp_penerima,
        ).save()
        messages.success(request, 'Form submission successful')

        return redirect('/createworker')

@login_required(login_url="/login")
@permission_required("app.add_items", login_url="/login", raise_exception=True)
def create_item_form(request):
    if request.method == "GET" :
        nama_pemesan = request.user.first_name

        return render(request, 'customer/formitem.html', {"nama_pemesan" : nama_pemesan})    
    else:
        author = request.user
        no_telp_pemesan = request.POST['no_telp_pemesan']
        input_datetime_str = request.POST['tanggal_ketemu']
        layanan = request.POST['layanan']
        jumlah = request.POST['jumlah']
        nama_penerima = request.POST['nama_penerima']
        alamat = request.POST['alamat']
        no_telp_penerima = request.POST['no_telp_penerima']

        parsed_datetime = datetime.strptime(input_datetime_str, "%m/%d/%Y %I:%M %p")

        tanggal_ketemu = parsed_datetime.strftime("%Y-%m-%d %H:%M")

        Items(
            author = author,
            no_telp_pemesan = no_telp_pemesan,
            tanggal_ketemu = tanggal_ketemu,
            layanan = layanan,
            jumlah = jumlah,
            nama_penerima = nama_penerima,
            alamat = alamat,
            no_telp_penerima = no_telp_penerima,
        ).save()
        messages.success(request, 'Form submission successful')

        return redirect('/createitem')
