def menu(request):
    return {'menu': request.site.menu_set.order_by('order')}
