from django.db.models import Q

# Create your views here.
from django.views.generic import ListView
from django.views.generic.base import TemplateView

from surman.models import AnswerGroup


class AnswerListView(ListView):
    """Bir egitmenin genel, kendisiyle veya bulundugu siniflarla ilgili cevaplari gorebildigi view"""
    paginate_by = 1

    def get_queryset(self):
        if self.request.user and self.request.user.userprofile:
            return AnswerGroup.objects \
                .filter(Q(answers__question__survey__site=self.request.site) & (
                Q(answers__question__related_course__in=
                  self.request.user.userprofile.trainer.filter(site=self.request.site)) |
                Q(answers__question__related_trainer=self.request.user.userprofile) |
                Q(answers__question__related_course__isnull=True,
                  answers__question__related_trainer__isnull=True))) \
                .distinct()
        else:
            return AnswerGroup.objects.none()

    def get_context_data(self, **kwargs):
        context = super(AnswerListView, self).get_context_data(**kwargs)
        if context['object_list'].exists():
            context["user_courses"] = self.request.user.userprofile.trainer.filter(site=self.request.site)
            context['answergroup'] = context['object_list'].get()
            context["visible_questions"] = context['answergroup'].answers \
                .filter(Q(question__survey__site=self.request.site) & (
                Q(question__related_course__in=
                  self.request.user.userprofile.trainer.filter(site=self.request.site)) |
                Q(question__related_trainer=self.request.user.userprofile) |
                Q(question__related_course__isnull=True,
                  question__related_trainer__isnull=True))) \
                .values_list("question", flat=True)
        return context


class UserAnalysisView(TemplateView):
    """Bir egitmenin anket sonuclarinin islendigi ve kendi ozelestirisini daha rahat yapabildigi bir view"""
    pass
