from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class StudentOnboarding(models.Model):
    student_reference = models.CharField(max_length=20, unique=True)
    student_age = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(21)]
    )
    parent_email = models.EmailField(max_length=254)
    region = models.CharField(max_length=30)
    has_learning_difficulty = models.BooleanField()
    requires_lsa_support = models.BooleanField()
    consent_to_process_data = models.BooleanField()
    requires_transport_support = models.BooleanField()
    requires_medical_assistance = models.BooleanField()
    ingested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "student_onboarding"
