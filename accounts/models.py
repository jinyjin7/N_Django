from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, name, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(extra_fields.get('password'))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, name, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class BaseUser(AbstractBaseUser):
    class Meta:
        db_table = 'users'

    source_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100,default="user")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email})"

    def get_natural_key(self):
        return (self.email,)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_student(self):
        return hasattr(self, 'student_profile')

    @property
    def is_teacher(self):
        return hasattr(self, 'teacher_profile')

    @property
    def user_type(self):
        if self.is_student:
            return 'student'
        elif self.is_teacher:
            return 'teacher'
        return 'none'


class SchoolChoices(models.TextChoices):
    ELEMENTARY = "elementary", _("초등학교")
    MIDDLE = "middle", _("중학교")
    HIGH = "high", _("고등학교")

class School(models.Model):
    class Meta:
        db_table = 'schools'

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    school_type = models.CharField(max_length=20, choices=SchoolChoices.choices)

    def __str__(self):
        return self.name

# 학생,선생님
class Student(models.Model):
    class Meta:
        db_table = 'student'

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='student_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    grade = models.PositiveIntegerField(blank=True, null=True)
    classroom = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.name} 학생 - {self.school}"



class Teacher(models.Model):
    class Meta:
        db_table = 'teacher'

    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='teachers')
    subject = models.CharField(max_length=100, blank=True)  # 담당 과목

    def __str__(self):
        return f"{self.user.name} 선생님 - {self.school}"

# 프로필
class AbstractBaseProfile(models.Model):
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    intro = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(blank=True, null=True)

    GENDER_CHOICES = [('M', '남'), ('F', '여')]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)

    class Meta:
        abstract = True


class StudentProfile(AbstractBaseProfile):
    class Meta:
        db_table = 'student_profile'

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='student_profile')

    def __str__(self):
        return f"{self.student} 프로필"


class TeacherProfile(AbstractBaseProfile):
    class Meta:
        db_table = 'teacher_profile'

    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name='teacher_profile')

    def __str__(self):
        return f"{self.teacher} 프로필"