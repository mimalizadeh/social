from django import forms
from home.models import Post, Comment


class PostCreateUpdateFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class PostCreateForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


class CommentCreateFrom(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write a comment ...'})
        }
        labels = {
            'body': ''
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(
                attrs={'class': 'form-control h-2', 'rows': 2, 'placeholder': 'Write a answer ...'})
        }
        labels = {
            'body': ''
        }


class PostSearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='',
                             widget=forms.TextInput(attrs={'class': 'form-control me-2', 'placeholder': 'Search in posts'}))
