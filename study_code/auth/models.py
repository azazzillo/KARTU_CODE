from django.db import models
from django.contrib.auth.models import AbstractBaseUser



class CustomUser(AbstractBaseUser):
    email = models.EmailField()
    first_name = models.CharField(
        verbose_name="имя",
        max_length=200
    )
    last_name = models.CharField(
        verbose_name="фамилия",
        max_length=200
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} | {self.email}"


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
        verbose_name="предмет",
        related_name="глава предмета"
    )

    class Meta:
        verbose_name = "глава"
        verbose_name_plural = "главы"

    def __str__(self) -> str:
        return f"{self.title} ({self.subject})"


class Student(CustomUser):
    group = models.ForeignKey(
        to=Group,
        verbose_name="группа",
        related_name="группы студента"
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


class Task(models.Model):
    chapter = models.ForeignKey(
        to=Chapter,
        verbose_name="глава",
        related_name="глава из задания"
    )
    tutor = models.ForeignKey(
        to=Tutor,
        verbose_name="преподаватель",
        related_name="преподаватель задание"
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

    STATUSES = {
        ACTIVE: "Active",
        DONE: "Done",
        INACTIVE: "Inactive",
        ON_CHECKING: "On checking",
    }

    student = models.ForeignKey(
        to=Student,
        verbose_name="студент",
        related_name="выполнивший"
    )
    task = models.ForeignKey(
        to=Task,
        verbose_name="задание",
        related_name="задание результат"
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
