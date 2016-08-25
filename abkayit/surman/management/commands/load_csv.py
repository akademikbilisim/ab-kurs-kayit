# coding=utf-8
import argparse

from datetime import datetime

import pytz
from django.core.management.base import BaseCommand, CommandError

from surman.models import Question, AnswerGroup, Answer

dtformat = "%Y/%m/%d %I:%M:%S %p"


class Command(BaseCommand):
    can_import_settings = True

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('file', type=argparse.FileType('r'))
        parser.add_argument('key_file', type=argparse.FileType('r'))
        parser.add_argument('site_name', type=str)
        parser.add_argument('site_year', type=str)
        parser.add_argument('survey', type=str)
        parser.add_argument('-ts', '--timestamp_name', type=str, default="Timestamp")
        parser.add_argument('-tk', '--token_name', type=str, default="Fiş")

    def get_objects(self, **options):
        from abkayit.models import Site
        from surman.models import Survey
        try:
            site = Site.objects.get(name=options["site_name"], year=options['site_year'])
        except Site.DoesNotExist as e:
            raise CommandError("Site not found")
        try:
            survey, _ = Survey.objects.get_or_create(name=options["survey"], site=site)
        except Site.DoesNotExist as e:
            raise CommandError("Survey not found")
        import csv
        try:
            csvfile = csv.reader(options["file"])
        except csv.Error:
            raise CommandError("CSV file is not valid")

        keys = map(str.strip, options["key_file"].readlines())

        return keys, csvfile, site, survey

    def read_file(self, csvfile):
        headers = csvfile.next()
        assert len(headers) == len(set(headers)), "Some headers are not unique"
        body = iter(csvfile)
        return headers, body

    def create_questions(self, survey, headers, ignore_list=list()):
        questions = Question.objects.filter(key__in=headers, survey=survey).values_list("key", "id")
        if questions.exists():
            return dict(questions)
        questions = []
        for idx, h in enumerate(headers):
            if idx in ignore_list:
                continue
            questions.append(Question(
                    survey=survey,
                    key=h,
                    text=h,
                    extra="imported\n",
            ))
        Question.objects.bulk_create(questions)
        return dict(Question.objects.filter(key__in=headers, survey=survey).values_list("key", "id"))

    def insert_answers(self, headers, questions, body, keys, timestamp_index, token_index):
        used_keys = []
        answers = []
        for row in body:
            dt, tz = row[timestamp_index].split(" GMT")
            dt = datetime.strptime(dt, dtformat)
            # Python2 hack (Python2 does not support timezone parsing via strptime)
            newdt = dt.replace(tzinfo=pytz.FixedOffset(int(tz) * 60))
            token = row[token_index]
            if token not in keys or token in used_keys:
                print "Reused token {}".format(row)
                continue
            used_keys.append(token)
            answer_group = AnswerGroup.objects.create(
                    token=token,
                    created=newdt,
            )
            for idx, col in enumerate(row):
                if idx in [token_index, timestamp_index] or not col:
                    continue
                answers.append(Answer(
                        question_id=int(questions[headers[idx].decode("utf-8")]),
                        group=answer_group,
                        text=col))
        Answer.objects.bulk_create(answers, batch_size=1000)

    def handle(self, *args, **options):
        keys, csvfile, site, survey = self.get_objects(**options)
        headers, body = self.read_file(csvfile)

        token_index = headers.index(options["timestamp_name"])
        timestamp_index = headers.index(options["token_name"])

        questions = self.create_questions(survey, headers, [token_index, timestamp_index])
        self.insert_answers(headers, questions, body, keys, token_index, timestamp_index)
