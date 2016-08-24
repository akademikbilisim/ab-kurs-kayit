# -*- coding: utf-8 -*-

from training.models import Course
from userprofile.models import UserProfile
from userprofile.userprofileops import UserProfileOPS
from django.contrib.auth.models import User


# Buradaki fonksiyonlara gerek yok simdilik
class CourseSubOps:
    def __init__(self):
        pass

    @staticmethod
    def createinst(postrequest, numofinst):
        insts = []
        uprof = UserProfileOPS()
        for i in xrange(numofinst):
            n_str = str(i) + '-'
            upass = uprof.generatenewpass(10)  # uretilen parola olusturulan kullaniciya gonderilecek.
            inst = User(first_name=postrequest[n_str + 'first_name'], last_name=postrequest[n_str + 'last_name'],
                        email=postrequest[n_str + 'email'], username=postrequest[n_str + 'email'], password=upass)
            inst.save()
            instprof = UserProfile(job=postrequest[n_str + 'job'], title=postrequest[n_str + 'title'],
                                   organization=postrequest[n_str + 'organization'], is_instructor=True,
                                   user=inst)
            instprof.save()
            insts.append(instprof)
        return insts

    @staticmethod
    def createcourse(request, insts):
        try:
            start_date = request.POST['start_date_year'] + '-' + request.POST['start_date_month'] + '-' + request.POST[
                'start_date_day']
            end_date = request.POST['end_date_year'] + '-' + request.POST['end_date_month'] + '-' + request.POST[
                'end_date_day']
            course = Course(name=request.POST['name'], description=request.POST['description'],
                            goal=request.POST['goal'], partipation_rules=request.POST['partipation_rules'],
                            start_date=start_date, end_date=end_date, fulltext=request.FILES['fulltext'])
            for i in insts:
                course.trainers.add(i)
            course.save()
            return 1
        except:
            return -1
