from django import forms
from .models import Article


# http://djangopatterns.com/patterns/models/automatically_filling_user/
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
