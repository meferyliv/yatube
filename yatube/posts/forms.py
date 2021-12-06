from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Обязательно напишите текст поста',
            'group': 'Указывать группу не обязательно'
        }

    def clean_data(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Напишите текст поста')
        return data
