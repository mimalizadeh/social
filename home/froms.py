from django import forms
from home.models import Post


class PostCreateUpdateFrom(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class PostCreateForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'from-control'}))
