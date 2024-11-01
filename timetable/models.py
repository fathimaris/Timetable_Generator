from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
class Subject(models.Model):
    subject_name = models.CharField(max_length=200)
    Course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')

    def __str__(self):
        return self.subject_name
class Staff(models.Model):
    staff_name = models.CharField(max_length=100)
    subjects = models.ManyToManyField(Subject, related_name='staff', blank=True)

    def __str__(self):
        return self.staff_name

