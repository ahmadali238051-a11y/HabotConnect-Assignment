Candidate Name: Mohd Ahmad
Email: ahmadali238051@gmail.com
Phone: 9696445866

# HabotConnect Task 3 — Schema Mapping

## Student Onboarding Schema

| Incoming Field | Data Type | DCYN Required | Validation / Transformation | Output |
|---|---|---|---|---|
| student_reference | String | No | 1–20 characters; must begin with `STU-`; trim whitespace and convert to uppercase | Normalized student reference |
| student_age | Integer | No | Must be between 3 and 21 inclusive | Validated integer |
| parent_email | String (Email) | No | Must be a valid email address; maximum 254 characters | Validated email |
| region | String | No | 2–30 characters; trim whitespace, convert to uppercase, and accept only UAE-ABU-DHABI, UAE-DUBAI, or UAE-SHARJAH | Normalized region |
| has_learning_difficulty | Boolean (DCYN) | Yes | Accept only Yes, No, True, False, 1, or 0; normalize to Boolean | True / False |
| requires_lsa_support | Boolean (DCYN) | Yes | Accept only Yes, No, True, False, 1, or 0; normalize to Boolean | True / False |
| consent_to_process_data | Boolean (DCYN) | Yes | Accept only Yes, No, True, False, 1, or 0; normalize to Boolean; must be True for processing | True / False |
| requires_transport_support | Boolean (DCYN) | Yes | Accept only Yes, No, True, False, 1, or 0; normalize to Boolean | True / False |
| requires_medical_assistance | Boolean (DCYN) | Yes | Accept only Yes, No, True, False, 1, or 0; normalize to Boolean | True / False |


## Business Rules / Cross-Field Validation

| Rule | Condition | Result |
|---|---|---|
| Consent required | consent_to_process_data must resolve to True | Reject payload if False |
| LSA dependency | If requires_lsa_support = True, then has_learning_difficulty must be True | Reject invalid combination |
| Unknown fields | Incoming field must exist in the defined schema | Reject unexpected fields |

### Validation Principle

The validation process is deterministic and fail-closed. Every incoming
field must match a predefined schema and validation rule. DCYN fields are
converted into canonical Boolean values, while invalid or ambiguous values
are rejected. Cross-field business rules are evaluated before validated
data is accepted by the application.

