from django.core.urlresolvers import reverse


def menu(request):
    if request.path.startswith(reverse('admin:index')):
        return {}
    return {'menu': request.site.menu_set.order_by('order')}
