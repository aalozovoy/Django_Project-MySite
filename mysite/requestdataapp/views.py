from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    '''обработка параметров запросов (также в можно в шаблоне)
    GET - словарь, get - запрос.
    '''
    context = {
        'a': a,
        'b': b,
        'result': result
    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)

def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/user-bio-form.html')

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    message = 'Add a file to download.'
    if request.method == 'POST' and request.FILES.get('myfile'):
        '''FILES - файл, get - запрос'''
        myfile = request.FILES['myfile']
        '''считывание файла'''
        fs = FileSystemStorage()
        '''сохранение на файловую систему'''
        if myfile.size <= 1024*1024:
            filename = fs.save(myfile.name, myfile)
            print('saved file', filename)
            message = 'The file is uploaded.'
        else:
            message = 'Error! The download is not possible! The file size is more than 1 MB.'

    context = {'message': message}
    return render(request, 'requestdataapp/file-upload.html', context=context)

