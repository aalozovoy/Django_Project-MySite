from django.http import HttpRequest, HttpResponse
import time

def set_useragent_on_request_middleware(get_response):
    print('initial call')
    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response
    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.request_time = 0
        self.ip_time = {}

    def __call__(self, request: HttpRequest):
        response = self.get_response(request)
        delay_time = 0
        if request.META.get('REMOTE_ADDR') not in self.ip_time:
            self.ip_time[request.META.get('REMOTE_ADDR')] = time.time()
        elif time.time() - self.ip_time[request.META.get('REMOTE_ADDR')] <= delay_time:
            self.ip_time[request.META.get('REMOTE_ADDR')] = time.time()
            return HttpResponse("Too many requests")
        else:
            self.ip_time[request.META.get('REMOTE_ADDR')] = time.time()
        return response


    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')



    # def __call__(self, request: HttpRequest):
    #     self.requests_count += 1
    #     print('requests count', self.requests_count)
    #     response = self.get_response(request)
    #     self.responses_count += 1
    #     print('responses count', self.responses_count)
    #     print(request.META.get('REMOTE_ADDR'))
    #     return response

















