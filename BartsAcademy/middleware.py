from django.shortcuts import redirect

class AgeGateMiddleware:
    EXCLUDED_URLS = ['/preview/agegate']
    IGNORED_PATHS = ['/favicon.ico']  # Add any other paths you want to ignore

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.session.get('agegate') and 
            request.path not in self.EXCLUDED_URLS and 
            request.path not in self.IGNORED_PATHS):
            request.session['next_url'] = request.path
            print(f"path is: {request.path}")
            return redirect('/preview/agegate')

        response = self.get_response(request)
        return response