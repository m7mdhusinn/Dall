from django.db import models
from certificates.models import Certificate
from companies.models import Company
from courses.models import Course
from jobs.models import Job
from skills.models import Skill
# Create your models here.
class Major(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    jobs= models.ManyToManyField(Job)
    certificates=models.ManyToManyField(Certificate)
    companies=models.ManyToManyField(Company)
    courses=models.ManyToManyField(Course)
    skills=models.ManyToManyField(Skill)
    image=models.ImageField(upload_to="images/", default="images/avatar-default.png")

    def __str__(self):
        return self.name
