from django import forms

from .models import WordDoc


class FileForm(forms.ModelForm):
    doc_file = forms.FileField(label='', widget=forms.FileInput(
        attrs={
            "accept": ".docx"}
    ))

    class Meta:
        model = WordDoc
        fields = ('doc_file',)
