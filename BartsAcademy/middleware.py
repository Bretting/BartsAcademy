from django.shortcuts import redirect
from crawlerdetect import CrawlerDetect

class AgeGateMiddleware:
    EXCLUDED_URLS = ['/agegate']
    IGNORED_PATHS = ['/favicon.ico']  # Add any other paths you want to ignore

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        crawler_detect = CrawlerDetect(user_agent)
        
        # Check if the user agent is Googlebot and set the session cookie
        if crawler_detect.isCrawler():
            request.session['agegate'] = True

        if (not request.session.get('agegate') and 
            request.path not in self.EXCLUDED_URLS and 
            request.path not in self.IGNORED_PATHS and
            request.path is not None):
            request.session['next_url'] = request.path
            return redirect('/agegate')
        
        if request.path in self.EXCLUDED_URLS:
            request.session['next_url'] = '/'

        response = self.get_response(request)
        return response