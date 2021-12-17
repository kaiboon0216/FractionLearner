
from django import forms
from .models import FilesAdmin,Comment,Qcomment

class DocumentForm(forms.ModelForm):
    class Meta:
         model = FilesAdmin
         fields = ['file', 'title']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

class QcommentForm(forms.ModelForm):
    class Meta:
        model = Qcomment
        fields = ['qcomment']

class SolutionForm(forms.ModelForm):
    class Meta:
        model = Qcomment
        fields = ['r_token']