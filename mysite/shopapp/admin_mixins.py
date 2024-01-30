from django.db.models import QuerySet
from django.db.models.options import Options
from django.http import HttpRequest, HttpResponse

import csv


class ExpotrasCVSMixin:
    '''Экспорт данных (моделей)'''
    def export_csv(self, request: HttpRequest, queryset: QuerySet):
        meta: Options = self.model._meta
        '''meta - список всех доступных полей'''
        field_names = [field.name for field in meta.fields]
        '''field_names - получение списка из строк с названиями полей'''

        response = HttpResponse(content_type='text/csv')
        '''response - объект (файл) в который выводятся (записываются) данные'''
        response['Content-Disposition'] = f'attachment; filename={meta}-export.csv'
        '''response['Content-Disposition'] - для скачивания файла с 'готовым' именем'''
        csv_writer = csv.writer(response)
        '''csv_writer - запись результата в ответ'''
        csv_writer.writerow(field_names)
        '''запись заголовков (граф таблицы)'''

        for obj in queryset:
            csv_writer.writerow([getattr(obj, field) for field in field_names])
        return response
        '''при возврате response, django его автоматически обрабатывает, браузер скачивает'''

    export_csv.short_description = 'Export as CSV'
    '''описание действия'''





