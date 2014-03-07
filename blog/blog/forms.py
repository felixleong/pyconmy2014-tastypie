from django import forms
from django.contrib.auth import get_user_model
from .models import Article


# http://djangopatterns.com/patterns/models/automatically_filling_user/
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article

    def clean_author(self):
        if not self.cleaned_data['author']:
            return get_user_model()()
        return self.cleaned_data['author']
