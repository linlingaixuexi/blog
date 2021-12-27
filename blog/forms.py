from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)

    class Meta:
        model = Post
        fields = ('images','title','text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
