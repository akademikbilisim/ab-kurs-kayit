import logging

from django.core.urlresolvers import reverse
from django.http import Http404

log = logging.getLogger(__name__)


class CurrentSiteMiddleware(object):
    def process_request(self, request):
        if request.path.startswith(reverse('admin:index')):
            return

        domain_parts = request.get_host().split('.')

        if len(domain_parts) > 2:
            subdomain = domain_parts[0]
            if subdomain.lower() == 'www':
                subdomain = None
            domain = '.'.join(domain_parts[1:])
        else:
            subdomain = None
            domain = request.get_host()

        request.subdomain = subdomain
        request.domain = domain

        from abkayit.models import Site
        try:
            request.site = Site.objects.get(domain=domain)
        except Site.MultipleObjectsReturned as e:
            log.error(e.message, extra=request.log_extra)
            raise Http404
        except Site.DoesNotExist as e:
            log.error(e.message, extra=request.log_extra)
            raise Http404
