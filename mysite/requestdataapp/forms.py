from django import forms
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

class UserBioForm(forms.Form):
    '''заменяет форму для ввода информации пользователя (вместо прописывания в html)'''
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label='Your age', min_value=1, max_value=150)
    bio = forms.CharField(label='Biography', widget=forms.Textarea)
    '''
    CharField() - поле для ввода символов
    IntegerField() - целочисленное поле
    label - отображается перед полем
    widget - виджет для отображения
    max_length - max длина
    min_value - max значение
    max_value - min значение
    TextField - большое текстовое поле
    '''
# Чтобы отобразить форму на странице передаем экземпляр в views.py -> user_form -> context

def validate_file_name(file: InMemoryUploadedFile) -> None:
    '''возвращает ничего или исключение'''
    if file.name and 'virus' in file.name:
        raise ValidationError("file name should not contain 'virus'")
    elif file.size > 1024*1024:
        raise ValidationError('Error! The download is not possible! The file size is more than 1 MB.')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
