from django.utils import timezone
from .models import Post, PostImage
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    template_name = 'blog/post_detail.html'
    post = get_object_or_404(Post, pk=pk)
    photos = PostImage.objects.filter(post=post)
    comments = post.comments.filter(approved_comment=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'photos':photos,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post_created = True
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            print("Form invalid, see below error msg")
            print(form.errors)
    # if GET method form, or anything wrong then we will create blank form
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
