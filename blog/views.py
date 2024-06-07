from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from rest_framework import viewsets, status
from .serializers import PostSerializer
from rest_framework.response import Response

class BlogImage(viewsets.ModelViewSet):
  queryset = Post.objects.all()
  serializer_class = PostSerializer

  def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

def js_test(request):
  return render(request, 'blog/js_test.html', {})

def post_list(request):
  posts = Post.objects.order_by('created_date')
  return render(request, 'blog/post_list.html', {'posts':  posts})

def post_detail(request, pk):
  post = get_object_or_404(Post, pk=pk)
  return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.image = request.POST('image')
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method== "POST":
      form = PostForm(request.POST, instance=post)
      if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_date= timezone.now()
        post.image = request.POST['image']
        post.save()
        return redirect('post_detail', pk=post.pk)
    else:
      form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

