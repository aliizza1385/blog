from .models import Post
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .serializers import CommentSerializer, PostSerializer, UserSerializer, TagSerializer, CategorySerializer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Post, Tag, Category, Comment, User, ReplyComment, Like
from blog_project.settings import Host
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from blog_project.settings import EMAIL_HOST_USER
import random

# this for Category Crud


class CategoryCrud(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        qs = Category.objects.all()
        data = CategorySerializer(qs, many=True).data
        response = Response(data)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        response.headers["Content-Range"] = len(qs)
        return response

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


# this for post crud
class handle_react_data(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        qs = Post.objects.all()
        data = PostSerializer(qs, many=True).data

        # Modify the image URL for each post
        for post_data in data:
            image_url = post_data.get('image')
            modified_image_url = Host + image_url  # Modify the URL as needed
            post_data['image'] = modified_image_url  # Update the 'image' field

        response = Response(data)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        response.headers["Content-Range"] = len(qs)
        return response

    def create(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tag = request.POST.get('tag')
        image = request.FILES.get('image')

        p = Post()
        p.title = title
        p.content = content
        p.category = Category.objects.get(id=category)
        p.image = image
        p.save()
        tags = tag.split(',')
        for tag in tags:
            p.tag.add(tag)
        p.save()
        response_data = {"id": p.id}

        return Response(response_data)
        # auther = request.POST.get('auther')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        tag = request.POST.get('tag')
        tags = tag.split(',')
        image = request.FILES.get('image')  # Get the uploaded image
        post_id = kwargs.get('pk')
        p = Post.objects.get(id=post_id)
        # old_tags = list(p.tag.values_list('id', flat=True))
        if tag:
            p.tag.clear()

        # print(old_tags)
        if image:
            p.title = title
            p.content = content
            p.category = Category.objects.get(id=category)
            p.image = image
            for tag in tags:
                p.tag.add(tag)
            p.save()

        else:
            object = Post.objects.get(id=kwargs.get('pk'))
            object.title = title
            object.content = content
            object.category = Category.objects.get(id=category)
            for tag in tags:
                object.tag.add(tag)
            object.save()
        return Response({'id': kwargs.get('pk')})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# this for user crud
class UserCrud(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        qs = User.objects.all()
        data = UserSerializer(qs, many=True).data
        # Modify the image URL for each post
        for post_data in data:
            image_url = post_data.get('image')
            modified_image_url = Host + image_url  # Modify the URL as needed
            post_data['image'] = modified_image_url  # Update the 'image' field
        response = Response(data)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        response.headers["Content-Range"] = len(qs)
        return response

    def update(self, request, *args, **kwargs):
        # data = json.loads(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)

        image = request.FILES.get('image')  # Get the uploaded image
        if image:
            return super().update(request, *args, **kwargs)
        object = User.objects.get(id=kwargs.get('pk'))
        object.username = username
        object.email = email
        object.password = password
        object.save()
        return Response({'id': kwargs.get('pk')})


# this for Tag Crud
class TagCrud(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs):
        qs = Tag.objects.all()
        data = TagSerializer(qs, many=True).data
        response = Response(data)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        response.headers["Content-Range"] = len(qs)
        return response

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

# this for Tag Crud


class Comments_RUD(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        qs = Comment.objects.all()
        data = CommentSerializer(qs, many=True).data
        response = Response(data)
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        response.headers["Content-Range"] = len(qs)
        return response

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

########################################################################
# this end of cruds and start main


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        otp_random = random.randrange(10000, 99999)
        try:
            # Send OTP via email (you can customize the email content)
            if User.objects.filter(email=email, is_active = True).exists():
                messages.error(request, 'The user already exists', 'danger')
                return redirect('register')
            
            elif User.objects.filter(username=username, is_active = True).exists():
                messages.error(request, 'The user already exists', 'danger')
                return redirect('register')
            else:
                send_mail(subject='For otp in blog website', message=f'Your OTP is: {otp_random}', from_email=EMAIL_HOST_USER, recipient_list=[email])
                hashed_password = make_password(password)
                image = request.FILES.get('img')
                user = User(username=username, email=email,
                            password=hashed_password, image=image, is_active=False)
                user.save()
                request.session['otp_random'] = otp_random
                request.session['email'] = email
                return render(request, 'verify_otp_gmail.html',{'email':email})

        except Exception as e:
            messages.error(
                request, 'Error sending OTP. Please check your email address.', 'danger')
            return redirect('register')

    return render(request, 'register.html')


def verify(request):
    emali_from_session = request.session.get('email')
    if request.method == 'POST':
        otp_code = request.POST.get('otp_code')
        email = request.POST.get('email')
        user = get_object_or_404(User, email=email)
        # we get information like string we must change that to int
        otp_code = int(otp_code)
        # we must have otp_random,emali we save that in register fuction
        otp_random_from_session = request.session.get('otp_random')
        # otp i send and otp user send to backend
        if otp_code == otp_random_from_session:
            user.is_active = True
            user.save()
            messages.success(request, 'User created', 'success')
            return redirect('main')
        else:
            messages.success(request, 'OTP is wrong', 'danger')
            return redirect('verify')       
    return render(request, 'verify_otp_gmail.html',{'email':emali_from_session})


def Main(request):
    p = Post.objects.all()
    paginator = Paginator(p, 3)
    t = Tag.objects.all()
    c = Category.objects.all()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index-list-right.html', {'page_obj': page_obj, 'tags': t, 'categories': c})


def main_left(request):
    p = Post.objects.all()
    paginator = Paginator(p, 3)
    t = Tag.objects.all()
    c = Category.objects.all()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index-full-left.html', {'page_obj': page_obj, 'tags': t, 'categories': c})


def Login(request):
    if request.method == 'POST':
        U = request.POST.get('username')
        P = request.POST.get('password')
        user = authenticate(request, username=U, password=P)
        if user is not None:
            login(request, user)
            messages.success(request, 'User logened', 'success')
            return redirect("main")
        messages.success(request, 'User dose not exist', 'danger')
        return redirect("login")
    return render(request, 'customer_login.html')


def Logout_view(request):
    logout(request)
    messages.success(request, 'User logouted', 'danger')
    return redirect("main")


def post_detail(request, pk):
    if request.method == 'POST':
        content = request.POST['content']
        c = Comment()
        c.content = content
        c.post = Post.objects.get(id=pk)
        c.user = request.user  # Use the authenticated user
        c.save()

    p = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=p)
    return render(request, 'post-details-1.html', {'post': p, 'comments': comments})


def filter_category(request, slug):
    c = Category.objects.filter(slug=slug).first()

    posts = Post.objects.filter(category=c)
    paginator = Paginator(posts, 3)
    t = Tag.objects.all()
    c = Category.objects.all()
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index-list-right.html', {'page_obj': page_obj, 'tags': t, 'categories': c})


def search(request):
    search_query = request.GET.get("q", "")
    results = Post.objects.filter(title__icontains=search_query)
    # Define the paginator after filtering results
    paginator = Paginator(results, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    t = Tag.objects.all()
    c = Category.objects.all()
    return render(request, 'index-list-right.html', {'page_obj': page_obj, 'tags': t, 'categories': c})


def replis(request):
    if request.method == 'POST':
        repliy = request.POST.get("message")
        Comment_id = request.POST['comment_id']
        user = request.user
        R = ReplyComment()
        R.content = repliy
        R.parent_comment = Comment.objects.get(id=Comment_id)
        R.user = user
        R.save()
        print(Comment_id)
        messages.success(request, 'reply added', 'success')
        return redirect("main")


def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    user = request.user
    if Like.objects.filter(user=user, post=post).exists():
        Like.objects.filter(user=user, post=post).delete()
        post.likes_count -= 1
    else:
        Like.objects.create(user=user, post=post)
        post.likes_count += 1

    post.save()

    return redirect('main')
