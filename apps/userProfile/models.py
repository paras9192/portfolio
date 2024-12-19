from django.db import models

class Jobs(models.Model):
    status = models.CharField(max_length=100, default="IN_PROGRESS")
    description = models.CharField(max_length=200, default="System Generate Job Description")
    date_and_time = models.DateTimeField(auto_now_add=True)  

    class Meta:
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return self.description


class UserData(models.Model):
    job_id = models.OneToOneField(Jobs, on_delete=models.CASCADE, related_name="user_data",unique=True) 
    type = models.CharField(max_length=100, default="Yucampus")
    user_data = models.JSONField(blank=False) 
    date_and_time = models.DateTimeField(auto_now_add=True)  

    class Meta:
        verbose_name_plural = 'User Data'

    def __str__(self):
        return self.type
