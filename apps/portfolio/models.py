from django.db import models

class ThemeMetaData(models.Model):
    job_id = models.ForeignKey('userProfile.Jobs', on_delete=models.CASCADE, related_name="theme_meta_data") 
    meta_data = models.JSONField(blank=False) 
    date_and_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Theme Meta Data'

    def __str__(self):
        return f"Meta Data for Job: {self.job_id.id}"


class PortFolio(models.Model):
    job_id = models.OneToOneField('userProfile.Jobs', on_delete=models.CASCADE, related_name="final_portfolio",unique=True) 
    final_json = models.JSONField(blank=False) 
    date_and_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'final Portfolio'

    def __str__(self):
        return f"Portfolio for Job: {self.job_id.id}"
