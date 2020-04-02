from django import forms

from .models import Book, Item


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'pdf', 'cover')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('text', 'complete')
