from django.test import TestCase

from .serializers import StudentOnboardingSerializer


class StudentOnboardingSerializerTest(TestCase):

    def test_valid_payload_is_accepted(self):
        data = {
            "student_reference": "STU-001",
            "student_age": 10,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_invalid_dcyn_value_is_rejected(self):
        data = {
            "student_reference": "STU-001",
            "student_age": 10,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Maybe",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("has_learning_difficulty", serializer.errors)

    def test_consent_is_required(self):
        data = {
            "student_reference": "STU-001",
            "student_age": 10,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "No",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("consent_to_process_data", serializer.errors)

    def test_lsa_requires_learning_difficulty(self):
        data = {
            "student_reference": "STU-001",
            "student_age": 10,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "No",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("requires_lsa_support", serializer.errors)

    def test_unknown_field_is_rejected(self):
        data = {
            "student_reference": "STU-001",
            "student_age": 10,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
            "random_field": "something",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("unknown_fields", serializer.errors)

    def test_minimum_age_is_accepted(self):
        data = {
            "student_reference": "STU-003",
            "student_age": 3,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_age_below_minimum_is_rejected(self):
        data = {
            "student_reference": "STU-002",
            "student_age": 2,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("student_age", serializer.errors)

    def test_maximum_age_is_accepted(self):
        data = {
            "student_reference": "STU-004",
            "student_age": 21,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_age_above_maximum_is_rejected(self):
        data = {
            "student_reference": "STU-005",
            "student_age": 22,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("student_age", serializer.errors)

    def test_student_reference_must_start_with_stu(self):
        data = {
            "student_reference": "ABC-001",
            "student_age": 10,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("student_reference", serializer.errors)

    def test_student_reference_is_normalized(self):
        data = {
            "student_reference": "stu-001",
            "student_age": 10,
            "parent_email": "parent@example.com",
            "region": "UAE-DUBAI",
            "has_learning_difficulty": "Yes",
            "requires_lsa_support": "Yes",
            "consent_to_process_data": "Yes",
            "requires_transport_support": "No",
            "requires_medical_assistance": "No",
        }

        serializer = StudentOnboardingSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(
            serializer.validated_data["student_reference"],
            "STU-001",
        )
