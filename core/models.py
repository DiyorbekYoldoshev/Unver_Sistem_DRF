from django.db import models



class Faculty(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Department(models.Model):

    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE)


class Group(models.Model):

    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department,on_delete=models.CASCADE)


