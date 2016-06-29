# -*- coding:utf-8  -*-

import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from abkayit.models import Menu, Content, Question, Answer
from abkayit.backend import getsiteandmenus

from userprofile.models import UserProfile

log = logging.getLogger(__name__)


@csrf_exempt
def index(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    content = None
    data['state'] = ""
    if not request.user.is_authenticated():
        data['alerttype'] = "alert-info"
        data['state'] = _("If you already have an account, please login from top right hand side of the page")
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                log.info("%s user successfuly logged in" % request.user, extra=d)
                return HttpResponseRedirect('/')
            else:
                data['state'] = _("Login Failed!")
                data['alerttype'] = "alert-danger"
    try:
        if not request.GET.get('menu_id'):
            menu_id = Menu.objects.filter(site=data['site']).order_by('order').first()
        else:
            menu_id = request.GET.get('menu_id')
        content = Content.objects.get(menu=menu_id)
    except ObjectDoesNotExist:
        content = None
        log.error("%s entered content not found " % request.user, extra=d)
    except Exception as e:
        log.error("%s error occured %s " % (request.user, e.message), extra=d)
    data['content'] = content
    return render_to_response('dashboard.html', data)


@csrf_exempt
@login_required(login_url='/')
def testbeforeapply(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = getsiteandmenus(request)
    data["note"] = "Kurs tercihi yapabilmek için aşağıdaki sorulara doğru yanıt vermelisiniz!"
    try:
        if not request.user.userprofile.userpassedtest:
            questions = Question.objects.filter(active=True, is_faq=True).order_by('no')
            if questions:
                data['questions'] = questions
                if request.POST:
                    userpasstest = True
                    for q in questions:
                        uansw = request.POST[str(q.no)][0]
                        ranswer = Answer.objects.get(pk=int(uansw))
                        if not ranswer.is_right:
                            data["note"] = "Tüm sorulara doğru cevap veriniz"
                            userpasstest = False
                    if userpasstest:
                        request.user.userprofile.userpassedtest = True
                        request.user.userprofile.save()
                        return redirect("applytocourse")
                return render_to_response('abkayit/faqtest.html', data)
            else:
                request.user.userprofile.userpassedtest = True
                request.user.userprofile.save()
        return redirect("applytocourse")
    except ObjectDoesNotExist:
        return redirect('createprofile')
