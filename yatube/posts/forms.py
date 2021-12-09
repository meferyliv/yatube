from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image',)
        help_texts = {
            'text': 'Обязательно напишите текст поста',
            'group': 'Указывать группу не обязательно',
            'image': 'Можно прикрепить изображение к посту',
        }

    def clean_data(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Напишите текст поста')
        return data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {
            'text': 'Обязательно напишите текст поста',
        }

    def clean_data(self):
        data = self.cleaned_data['text']
        if data == '':
            raise forms.ValidationError('Напишите текст комментария')
        return data
