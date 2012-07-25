from django.http import HttpResponse
from models import Domain

class MultiSiteMiddleware: 
    def process_request(self, request):
        try: 
            host = request.get_host().rsplit(':', 1)[0].replace('www.', '')
            domain = Domain.objects.get(name=host)
        except:
            return HttpResponse("Invalid site")

        request.site = domain.site
        return
