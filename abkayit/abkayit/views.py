# -*- coding:utf-8  -*-

import logging

from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from abkayit.models import Menu, Content, Question, Answer

log = logging.getLogger(__name__)


def index(request):
    data = {}
    content = None
    data['state'] = ""
    if not request.user.is_authenticated():
        data['alerttype'] = "alert-info"
        data['state'] = _("If you already have an account, please login from top right hand side of the page")
    try:
        if not request.GET.get('menu_id'):
            menu_id = Menu.objects.filter(site=request.site).order_by('order').first()
        else:
            menu_id = request.GET.get('menu_id')
        content = Content.objects.get(menu=menu_id)
    except ObjectDoesNotExist:
        content = None
        log.error("%s entered content not found " % request.user, extra=request.log_extra)
    except Exception as e:
        log.error("%s error occured %s " % (request.user, e.message), extra=request.log_extra)
    data['content'] = content
    return render(request, 'base/dashboard.html', data)


@csrf_exempt
@login_required(login_url='/')
def testbeforeapply(request):
    data = {"note": "Kurs tercihi yapabilmek için aşağıdaki sorulara doğru yanıt vermelisiniz!"}
    try:
        if not request.user.userprofile.userpassedtest:
            questions = Question.objects.filter(active=True, is_faq=True).order_by('no')
            if questions:
                data['questions'] = questions
                if request.POST:
                    userpasstest = True
                    wronganswers = ""
                    for q in questions:
                        uansw = request.POST.get(str(q.no))
                        if not uansw:
                            data['note'] = "Tüm sorulara cevap veriniz."
                            return render(request, 'abkayit/faqtest.html', data)
                        ranswer = Answer.objects.get(pk=int(uansw))
                        if not ranswer.is_right:
                            log.info("yanlis cevap: %s" % q.no, extra=request.log_extra)
                            wronganswers += "%s " % q.no
                            userpasstest = False
                    if userpasstest:
                        request.user.userprofile.userpassedtest = True
                        request.user.userprofile.save()
                        return redirect("applytocourse")
                    else:
                        data["note"] = "Tüm sorulara doğru cevap veriniz yanlış cevaplar %s" % wronganswers
                return render(request, 'abkayit/faqtest.html', data)
            else:
                request.user.userprofile.userpassedtest = True
                request.user.userprofile.save()
        return redirect("applytocourse")
    except ObjectDoesNotExist:
        return redirect('createprofile')


def auth_login(request):
    """simple wrapper around django's login view"""
    if request.method == "POST":
        from django.contrib.auth.views import login
        return login(request)
    else:
        from django.shortcuts import redirect
        return redirect("/")


def auth_logout(request):
    """simple wrapper around django's logout view"""
    if request.method == "POST":
        from django.contrib.auth.views import logout
        return logout(request, next_page="/")
    else:
        from django.shortcuts import redirect
        return redirect("/")
