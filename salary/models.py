# models.py
from django.db import models

class PoliceSalary(models.Model):
    grade = models.CharField(max_length=50)
    rank = models.CharField(max_length=50)
    basic_salary = models.IntegerField()

    def __str__(self):
        return f"{self.grade}계급 {self.rank} - {self.basic_salary}원"
