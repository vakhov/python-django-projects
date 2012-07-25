from django.http import HttpResponse
from management.models import Domain

class MultiSiteMiddleware: 
    def process_request(self, request):
        if request.path.startswith('/admin/'): 
            return 
        try: 
            host = request.get_host().rsplit(':', 1)[0].replace('www.', '')
            domain = Domain.objects.get(name=host)
        except:
            return HttpResponse("Invalid site")

        request.site = domain.site
        return
