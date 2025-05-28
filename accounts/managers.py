from django.db import models
from models import School
from django.db.models import QuerySet

class TeacherManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related('school')

    def for_school(self, school_code):
        try:
            school = School.objects.get(code=school_code)
        except School.DoesNotExist:
            raise School.DoesNotExist(f"해당 학교코드인 '{school_code}'를 찾을 수 없습니다")
        return self.filter(school=school)



class StudentManager(models.Manager):

    def get_queryset(self) -> QuerySet:
        return super().get_queryset().select_related('school')

    def for_school(self, school_code):
        try:
            school = School.objects.get(code=school_code)
        except School.DoesNotExist:
            raise School.DoesNotExist(f"해당 학교코드인 '{school_code}'를 찾을 수 없습니다")
        return self.filter(school=school)

    def by_grade(self, grade):
        return self.filter(grade=grade)

    def in_classroom(self, grade, classroom):
        return self.filter(grade=grade, classroom=classroom)