# -*- coding: utf-8 -*-
import json
import logging

from django.shortcuts import render, render_to_response, RequestContext, redirect
from django.http.response import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from abkayit.backend import prepare_template_data
from abkayit.models import Site, Menu

from userprofile.models import UserProfile
from userprofile.forms import InstProfileForm,CreateInstForm
from userprofile.userprofileops import UserProfileOPS

from training.models import Course, TrainessCourseRecord
from training.forms import CreateCourseForm

log=logging.getLogger(__name__)

@login_required(login_url='/')
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
def show_course(request, course_id):
	try:
		data = prepare_template_data(request)	
		course = Course.objects.get(id=course_id)
		data['course'] = course
		return render_to_response('training/course_detail.html', data)
	except ObjectDoesNotExist:
		print "kurs bulunamadi.."
		return HttpResponse("Kurs Bulunamadi")

@login_required
def list_courses(request):
	data = prepare_template_data(request)
	courses = Course.objects.filter(start_date__year='2016')
	data['courses'] = courses
	return render_to_response('training/courses.html', data)	

@login_required
def edit_course(request):
	return HttpResponse("Yeni kurs kaydi")

@login_required
def apply_to_course(request):
	data=prepare_template_data(request)
	if request.method == "POST":
		selected_courses = []
		for key in request.POST.iterkeys():
			if key!="csrfmiddlewaretoken":
				selected_courses.append(request.POST.get(key))
		try:
			userprofile = UserProfile.objects.get(user=request.user)
			TrainessCourseRecord.objects.filter(trainess=userprofile).delete()
			created = True
			for course_pre in json.loads(request.POST.get('course')):
				course_record, created = TrainessCourseRecord.objects.get_or_create(
												trainess=userprofile, 
												course=Course.objects.get(id=course_pre['id']), 
												preference_order=course_pre['preference'])
				if(created == False):
					return HttpResponse(json.dumps({'status':'nok'}), content_type="application/json")
			if(created):
				return HttpResponse(json.dumps({'status':'ok'}), content_type="application/json")
		except ObjectDoesNotExist:
			print "Profil Bulunamadi"
	courses = Course.objects.filter(approved=True)
	course_records = TrainessCourseRecord.objects.filter(trainess=request.user)
	data['courses'] = courses
	data['course_records'] = {cs.course:cs.preference_order for cs in course_records}
	return render_to_response('training/courserecord.html', data)

@login_required
def control_panel(request):
	uprofile = UserProfile.objects.get(user=request.user).is_student
	if not uprofile:
		#TODO: template form haline getirilip her basvurunun yanına onay butonu koyulup en alta secimleri kaydet butonu eklenmeli.
		data = prepare_template_data(request)
		course = Course.objects.filter(approved=True).filter(trainer__user=request.user)[0].pk
		trainess1 = TrainessCourseRecord.objects.filter(course=course).filter(preference_order=1).values_list('trainess',flat=True)
		data['trainess1'] = UserProfile.objects.filter(pk__in=trainess1)
		trainess2 = TrainessCourseRecord.objects.filter(course=course).filter(preference_order=2).values_list('trainess',flat=True)
		data['trainess2'] = UserProfile.objects.filter(pk__in=trainess2)
		return render_to_response("training/controlpanel.html", data)
	else:
		#TODO: burada kullanici ogrenci ise yapılacak islem secilmeli. simdilik kurslari listeleme olarak birakiyorum
		return redirect("listcourses")
