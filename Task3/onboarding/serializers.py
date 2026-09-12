from rest_framework import serializers

from .dcyn_library import DCYNValidationError, normalize_dcyn
from .models import StudentOnboarding


class StrictDCYNBooleanField(serializers.Field):
    default_error_messages = {
        "invalid": "Accepted binary values are Yes, No, True, False, 1, or 0 only."
    }

    def to_internal_value(self, data):
        try:
            return normalize_dcyn(data)
        except DCYNValidationError:
            self.fail("invalid")

    def to_representation(self, value):
        return bool(value)


class StudentOnboardingSerializer(serializers.ModelSerializer):
    has_learning_difficulty = StrictDCYNBooleanField()
    requires_lsa_support = StrictDCYNBooleanField()
    consent_to_process_data = StrictDCYNBooleanField()
    requires_transport_support = StrictDCYNBooleanField()
    requires_medical_assistance = StrictDCYNBooleanField()

    class Meta:
        model = StudentOnboarding
        fields = (
            "student_reference",
            "student_age",
            "parent_email",
            "region",
            "has_learning_difficulty",
            "requires_lsa_support",
            "consent_to_process_data",
            "requires_transport_support",
            "requires_medical_assistance",
        )
        extra_kwargs = {
            "student_reference": {"min_length": 1, "max_length": 20},
            "student_age": {"min_value": 3, "max_value": 21},
            "region": {"min_length": 2, "max_length": 30},
        }

    def to_internal_value(self, data):
        if not isinstance(data, dict):
            raise serializers.ValidationError("A JSON object is required.")

        unknown_fields = sorted(set(data) - set(self.fields))
        if unknown_fields:
            raise serializers.ValidationError(
                {
                    "unknown_fields": [
                        f"Unexpected field: {name}" for name in unknown_fields
                    ]
                }
            )
        return super().to_internal_value(data)

    def validate_student_reference(self, value):
        normalized = value.strip().upper()
        if not normalized.startswith("STU-"):
            raise serializers.ValidationError("Student reference must begin with STU-.")
        return normalized

    def validate_region(self, value):
        normalized = value.strip().upper()
        allowed_regions = {"UAE-ABU-DHABI", "UAE-DUBAI", "UAE-SHARJAH"}
        if normalized not in allowed_regions:
            raise serializers.ValidationError(
                "Region must be UAE-ABU-DHABI, UAE-DUBAI, or UAE-SHARJAH."
            )
        return normalized

    def validate(self, attrs):
        if attrs["consent_to_process_data"] is not True:
            raise serializers.ValidationError(
                {"consent_to_process_data": "Consent must be Yes before processing."}
            )
        if attrs["requires_lsa_support"] and not attrs["has_learning_difficulty"]:
            raise serializers.ValidationError(
                {
                    "requires_lsa_support": (
                        "LSA support cannot be Yes when learning difficulty is No."
                    )
                }
            )
        return attrs
