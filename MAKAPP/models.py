from django.db import models


# Create your models here.
class JobTitle(models.Model):
    position = models.CharField(max_length=100)
    basic_salary = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.position


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    hours = models.PositiveIntegerField(default=0)
    jobtitle_status = models.ForeignKey(JobTitle, on_delete=models.CASCADE)
    gross_salary = models.PositiveIntegerField(default=0)
    # gross_salary = basic_salary * hours

    def save(self, *args, **kwargs):
        self.gross_salary = (self.hours * self.jobtitle_status.basic_salary)
        return super().save(*args, **kwargs)

    def __str__(self):
       return f"{self.first_name} {self.last_name}"