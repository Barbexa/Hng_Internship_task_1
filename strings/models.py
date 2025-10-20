from django.db import models

# Create your models here.

class AnalyzedString(models.Model):
    id= models.CharField(max_length=64, primary_key=True, editable=False)
    value=models.TextField(unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    character_frequency_map = models.JSONField(default=dict)

    def __str__(self):
        return f"String: {self.value[:30]}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['value'], name='unique_string_value')
        ]
