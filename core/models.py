from django.db import models

# Create your models here.

class TestModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column="Test name")
    test_text = models.TextField(db_column="test text")