# -*- coding:utf-8  -*-

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from abkayit.models import *

from userprofile.models import UserProfile

log = logging.getLogger(__name__)


@csrf_exempt
def index(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    content = None
    data = {}
    if not request.user.is_authenticated():
        state = "Eğer bir hesabınız varsa, sayfanın sağ üst tarafından giriş yapabilirsiniz!"
        alert_type = "alert-info"
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                log.info("%s user successfully logged in" % request.user, extra=d)
                return HttpResponseRedirect('/')
            else:
                state = "Kullanıcı veya Parola Eşleşmiyor!"
                alert_type = "alert-danger"
        data['state'] = state
        data['alert_type'] = alert_type
    try:
        if not request.GET.get('menu_id'):
            menu_id = Menu.objects.all().order_by('order').first()
        else:
            menu_id = request.GET.get('menu_id')
        content = Content.objects.get(menu=menu_id)
    except ObjectDoesNotExist:
        log.error("%s entered content not found " % request.user, extra=d)
    except Exception as e:
        log.error("%s error occured %s " % (request.user, e.message), extra=d)
    data['content'] = content
    return render(request, 'dashboard.html', data)


@csrf_exempt
@login_required(login_url='/')
def testbeforeapply(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = {}
    state = "Kurs tercihi yapabilmek için aşağıdaki sorulara doğru yanıt vermelisiniz!"
    alert_type = "alert-info"
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if not user_profile.userpassedtest:
            questions = Question.objects.filter(active=True).order_by('no')
            if questions:
                data['questions'] = questions
                if request.POST:
                    is_passed = True
                    for q in questions:
                        uansw = request.POST[str(q.no)][0]
                        if q.rightanswer.id != int(uansw):
                            state = "Tüm sorulara doğru cevap veriniz"
                            alert_type = "alert-danger"
                            is_passed = False
                    if is_passed:
                        user_profile.is_passed = True
                        user_profile.save()
                return render_to_response('faqtest.html', data)
            else:
                user_profile.userpassedtest = True
                user_profile.save()
        return redirect("applytocourse")
    except ObjectDoesNotExist:
        return redirect('createprofile')
