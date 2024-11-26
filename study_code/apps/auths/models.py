from django.db import models
from django.contrib.auth.models import (
        AbstractBaseUser, BaseUserManager,
        PermissionsMixin
    )

import uuid


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None,
                    password=None, **extra_fields):
        if not email:
            raise ValueError('Укажите email.')
        if not first_name:
            raise ValueError('Укажите имя.')
        if not last_name:
            raise ValueError('Укажите фамилию.')

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('!!! is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('!!! is_superuser=True.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=extra_fields.pop('first_name', ''),  
            last_name=extra_fields.pop('last_name', ''),   
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        verbose_name="Имя",
        max_length=200,
        blank=True  
    )
    last_name = models.CharField(
        verbose_name="Фамилия",
        max_length=200,
        blank=True  
    )
    is_staff = models.BooleanField(
        default=False
    )
    is_superuser = models.BooleanField(
        default=False
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    class Meta:
        app_label = 'auths'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.email}"


class Group(models.Model):
    name = models.CharField(
        verbose_name="название",
        max_length=200
    )
    year = models.DateField(
        verbose_name="год"
    )

    class Meta:
        verbose_name = "группа"
        verbose_name_plural = "группы"

    def __str__(self) -> str:
        return f"{self.name}"


class Subject(models.Model):
    name = models.CharField(
        verbose_name="название",
        max_length=200
    )

    class Meta:
        verbose_name = "предмет"
        verbose_name_plural = "предметы"
  
    def __str__(self) -> str:
        return f"{self.name}"


class Chapter(models.Model):
    title = models.CharField(
        verbose_name="заголовок",
        max_length=200
    )
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.PROTECT,
        verbose_name="предмет"
    )

    class Meta:
        verbose_name = "глава"
        verbose_name_plural = "главы"

    def __str__(self) -> str:
        return f"{self.title} ({self.subject})"


class Student(CustomUser):
    group = models.ForeignKey(
        to=Group,
        on_delete=models.PROTECT,
        verbose_name="группа"
    )

    class Meta:
        verbose_name = "студент"
        verbose_name_plural = "студенты"
 
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} | {self.group}"


class Tutor(CustomUser):
    dolzhnost = models.CharField(
        verbose_name="должность",
        max_length=100
    )

    class Meta:
        verbose_name = "преподаватель"
        verbose_name_plural = "преподаватели"
    
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} | {self.email}"


class Invitation(models.Model):
    email = models.EmailField()
    token = models.UUIDField(
        default=uuid.uuid4, 
        unique=True
    )
    inviter = models.ForeignKey(
        to=CustomUser, 
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=10, 
        choices=(
            ("tutor", "Tutor"), 
            ("student", "Student")
        )
    )
    first_name = models.CharField(
        verbose_name="имя",
        max_length=50,
        default="None"
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=50,
        default="None"
    )
    position_or_group = models.CharField(
        max_length=100, 
        null=True, 
        blank=True,
        default="No"
    )
    is_used = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Invitation to {self.email} as {self.role}"


class Task(models.Model):
    chapter = models.ForeignKey(
        to=Chapter,
        on_delete=models.PROTECT,
        verbose_name="глава"
    )
    tutor = models.ForeignKey(
        to=Tutor,
        on_delete=models.PROTECT,
        verbose_name="преподаватель"
    )
    acc_rate = models.FloatField(
        verbose_name="рейтинг"
    )
    problem = models.TextField(
        verbose_name="описание"
    )

    class Meta:
        verbose_name = "задача"
        verbose_name_plural = "задачи"
 
    def __str__(self) -> str:
        return f"{self.tutor} {self.chapter.subject} | {self.email}"


class Result(models.Model):
    ACTIVE = "ACT"
    DONE = "DON"
    INACTIVE = "INA"
    ON_CHECKING = "OCH"

    STATUSES = [
        (ACTIVE, "Active"),
        (DONE, "Done"),
        (INACTIVE, "Inactive"),
        (ON_CHECKING, "On checking"),
    ]

    student = models.ForeignKey(
        to=Student,
        on_delete=models.PROTECT,
        verbose_name="студент"
    )
    task = models.ForeignKey(
        to=Task,
        on_delete=models.PROTECT,
        verbose_name="задание"
    )
    status = models.CharField(
        choices=STATUSES,
        default=INACTIVE,
        verbose_name="статус",
        max_length=3
    )

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результаты"

    def __str__(self) -> str:
        return f"{self.student}"
