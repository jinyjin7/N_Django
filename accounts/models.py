from django.db import models
from django.utils.translation import gettext_lazy as _


# 기본 user 모델 -> 선생님과 학생 필터
class BaseUserQuerySet(models.QuerySet):
    def teachers(self):
        return self.filter(type='T')

    def students(self):
        return self.filter(type='S')


class BaseUser(models.Model):
    class Meta:
        db_table = 'users'

    source_id = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    GENDER_CHOICES = [
        ('M', '남'),
        ('F', '여'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    TYPE_CHOICES = [
        ('T', '선생님'),
        ('S', '학생'),
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    profile_image = models.URLField(blank=True, null=True)
    age = models.PositiveIntegerField()
    intro = models.TextField(blank=True)


# 학생 모델
class StudentModel(BaseUser):
    class Meta:
        db_table = 'student'

    school = models.OneToOneField('School', on_delete=models.CASCADE, related_name='student')
    classroom = models.PositiveIntegerField(max_length=20,blank=True,null=True)
    grade = models.PositiveIntegerField(max_length=20,blank=True,null=True)

    def __str__(self):
        return f"{self.name} 학생,{self.school} {self.grade}학년 {self.classroom}"

# 교사 모델
class Teacher(BaseUser):
    class Meta:
        db_table = 'teacher'

    school = models.OneToOneField('School', on_delete=models.CASCADE, related_name='teacher')
    is_admin = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.school} {self.name}선생님. ({self.email})"



# 학교 종류 선택 및 학교 모델
class SchoolChoices(models.TextChoices):
    ELEMENTARY_SCHOOL = "elementary_school", _("Elementary school")
    MIDDLE_SCHOOL = "middle_school", _("Middle school")
    HIGH_SCHOOL = "high_school", _("High school")


class School(models.Model):
    class Meta:
        db_table = 'school'

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True)
    school_type = models.CharField(max_length=255,choices=SchoolChoices.choices,verbose_name="학교 유형")

    def __str__(self):
        return self.name



