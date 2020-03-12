from django.db import models

# Create your models here.
class Professors(models.Model):
    professor_id = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    def __str__(self):
        return u'%s, %s, %s' % (self.professor_id, self.first_name,self.last_name)

class Moudles(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    year =models.CharField(max_length=4)
    semester = models.CharField(max_length=1)
    taughtBy = models.ManyToManyField(Professors)
    class Meta:
        unique_together = ("name", "code", "year", "semester")
    def __str__(self):
        return u'%s, %s, %s, %s' % (self.name, self.code, self.year, self.semester)


class Rating(models.Model):
    professer = models.ForeignKey(Professors, on_delete=models.CASCADE)
    stars = models.IntegerField()
    module = models.ForeignKey(Moudles, on_delete=models.CASCADE)
    def __str__(self):
        return u'%s, %s, %s' % (self.professer_id, self.stars, self.module.code)
class Users(models.Model):
    userName = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=10)
    is_active = models.CharField(max_length=1,default='0')
    email =models.EmailField()
    def __str__(self):
        return u'%s, %s, %s' % (self.userName, self.password, self.email)
