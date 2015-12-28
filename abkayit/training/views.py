# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.views.decorators import staff_member_required

from abkayit.backend import prepare_template_data
from abkayit.models import Site, Menu
from abkayit.decorators import active_required

from userprofile.models import UserProfile
from userprofile.forms import InstProfileForm,CreateInstForm
from userprofile.userprofileops import UserProfileOPS

from training.models import Course, TrainessCourseRecord
from training.forms import CreateCourseForm

log=logging.getLogger(__name__)

@login_required(login_url='/')
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def submitandregister(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data=prepare_template_data(request)
    userops=UserProfileOPS()
    # TODO:site ve pages'e bi care bulmak lazim
    site=Site.objects.get(is_active=True)
    pages=Menu.objects.filter(site=site.pk).order_by('order')
    note="Kurs onerisi olustur:"
    try:
        curuserprof=UserProfile.objects.get(user=request.user)
    except:
        log.info("%s kullanici profili bulunamadi" % (request.user),extra=d)
    curinstprofform=InstProfileForm(prefix="cur")
    forms={}
    for x in xrange(4):
        forms[x]=[CreateInstForm(prefix=str(x)+"inst"),InstProfileForm(prefix=str(x)+"instprof")]
    form=CreateCourseForm()
    if "submit" in request.POST:
        allf=[]
        forms={}
        for x in xrange(4):
            if str(x)+"inst-email" in request.POST:
                forms[x]=[CreateInstForm(request.POST,prefix=str(x)+"inst"),InstProfileForm(request.POST,prefix=str(x)+"instprof")]
                allf.append(forms[x][0].is_valid())
                allf.append(forms[x][1].is_valid())
            else:
                pass
        curinstprofform=InstProfileForm(request.POST,prefix="cur")
        form=CreateCourseForm(request.POST)
        if all([curinstprofform.is_valid(), form.is_valid()]) and all(allf):
            curinst=curinstprofform.save(commit=False)
            curinst.user=request.user
            curinst.save()
            course=form.save(commit=False)
            if 'fulltext' in request.FILES:
                course.fulltext = request.FILES['fulltext']
            course.save()
            for key,f in forms.items():
                instx=f[0].save(commit=False)
                passwd=userops.generatenewpass(8)
                instx.set_password(passwd)
                instx.save()
                instxprof=f[1].save(commit=False)
                instxprof.user=instx
                instxprof.save()
                course.trainer.add(instxprof)
            course.trainer.add(curinst)
            course.save()
            note="Egitim oneriniz basari ile alindi."
        else:
            note="Olusturulamadi"
    return render_to_response("training/submitandregister.html",{'site':site,'pages':pages,'note':note,'form':form,'curinstprofform':curinstprofform,'forms':forms},context_instance=RequestContext(request))

@login_required
def new_course(request):
    return HttpResponse("Yeni kurs kaydi")

@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def show_course(request, course_id):
    try:
        data = prepare_template_data(request)    
        course = Course.objects.get(id=course_id)
        data['course'] = course
        return render_to_response('training/course_detail.html', data)
    except ObjectDoesNotExist:
        return HttpResponse("Kurs Bulunamadi")

@login_required
@user_passes_test(active_required, login_url=reverse_lazy("active_resend"))
def list_courses(request):
    data = prepare_template_data(request)
    courses = Course.objects.filter(site=data['site'])
    data['courses'] = courses
    return render_to_response('training/courses.html', data)    

@login_required
def edit_course(request):
    return HttpResponse("Yeni kurs kaydi")

@login_required
def apply_to_course(request):
    data=prepare_template_data(request)
    data['closed'] = "0"
    message = ""
    now = datetime.date(datetime.now())
    if now < data['site'].application_start_date:
        data['note'] = _("You can choose courses in future")
        data['closed'] = "1"
        return render_to_response('training/courserecord.html', data)
    elif now > data['site'].application_end_date:
        data['note'] = _("The course choosing process is closed")
        data['closed'] = "1"
        return render_to_response('training/courserecord.html', data) 
    note = _("You can choose courses in order of preference.")
    if request.method == "POST":
        if now < data['site'].application_start_date:
            message = _("You can choose courses in future")
            data['closed'] = True
            return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")
        elif now > data['site'].application_end_date:
            message = _("The course choosing process is closed")
            data['closed'] = True
            return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")
        try:
            userprofile = UserProfile.objects.get(user=request.user)
            TrainessCourseRecord.objects.filter(trainess=userprofile).delete()
            for course_pre in json.loads(request.POST.get('course')):
                try:
                    course_record = TrainessCourseRecord(trainess=userprofile, 
                                          course=Course.objects.get(id=course_pre['value']), 
                                          preference_order=course_pre['name'])
                    course_record.save()
                    message = "Tercihleriniz başarılı bir şekilde güncellendi"
                except:
                    message = "Tercihleriniz kaydedilirken hata oluştu"
                    return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")
            return HttpResponse(json.dumps({'status':'0', 'message':message}), content_type="application/json")
        except ObjectDoesNotExist:
            message = "Tercihleriniz kaydedilirken hata oluştu"
            return HttpResponse(json.dumps({'status':'-1', 'message':message}), content_type="application/json")
    courses = Course.objects.filter(approved=True)
    course_records = TrainessCourseRecord.objects.filter(trainess__user=request.user).order_by('preference_order')
    data['courses'] = courses
    data['course_records'] = course_records
    data['note'] = note
    return render_to_response('training/courserecord.html', data)

@login_required
def control_panel(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = prepare_template_data(request)
    note = _("You can accept trainees")
    now = datetime.date(datetime.now())
    try:
        uprofile = UserProfile.objects.get(user=request.user).is_student
        log.info(uprofile, extra = d)
        if not uprofile:    
            if now < data['site'].aproval_start_date:
                data['note'] = _("You can choose courses in future")
                data['closed'] = "1"
                return render_to_response("training/controlpanel.html", data,context_instance=RequestContext(request))
            elif now > data['site'].aproval_end_date:
                data['note'] = _("The course choosing process is closed")
                data['closed'] = "1"
                return render_to_response("training/controlpanel.html", data,context_instance=RequestContext(request))

            courses = Course.objects.filter(approved=True).filter(trainer__user=request.user)
            log.info(courses, extra = d)

            if courses:
                trainess = {}
                for course in courses:
                        trainess1 = TrainessCourseRecord.objects.filter(course=course.pk).filter(preference_order=1).values_list('trainess',flat=True)
                        trainess2 = TrainessCourseRecord.objects.filter(course=course.pk).filter(preference_order=2).values_list('trainess',flat=True)
                        trainess[course] = {}
                        trainess[course]['trainess1'] = UserProfile.objects.filter(pk__in=trainess1)
                        trainess[course]['trainess2'] = UserProfile.objects.filter(pk__in=trainess2)
                data['trainess'] = trainess
                log.info(data, extra = d)
                if request.POST:
                    log.info(request.POST, extra=d)
                    for course in courses:
                        try:
                            course.trainess.clear()
                            for student in request.POST.getlist('students' + str(course.pk)):
                                course.trainess.add(UserProfile.objects.get(user_id=student))
                            course.save()
                        except Exception:
                            pass   
            data['note'] = note
            return render_to_response("training/controlpanel.html", data,context_instance=RequestContext(request))
        else:
            return redirect("applytocourse")
    except UserProfile.DoesNotExist:
        #TODO: burada kullanici ogrenci ise yapılacak islem secilmeli. simdilik kurslari listeleme olarak birakiyorum
        return redirect("createprofile")

@staff_member_required
def allcourseprefview(request):
    d = {'clientip': request.META['REMOTE_ADDR'], 'user': request.user}
    data = prepare_template_data(request)
    data['datalist']=TrainessCourseRecord.objects.all()
    return render_to_response("training/allcourseprefs.html",data,context_instance=RequestContext(request))

