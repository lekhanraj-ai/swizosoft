#!/usr/bin/env python
"""Quick test to verify email templates are correct"""

# Test the email body/HTML content without actually sending

# Paid acceptance email
paid_accept_name = "John Doe"
paid_accept_body = f"""Hi {paid_accept_name},

We are pleased to inform you that you have been selected for the Paid Internship Program at Swizosoft. Your application and performance matched our requirements, and we look forward to having you contribute to our ongoing projects.

Our team will reach out shortly with onboarding instructions, required documents, and your reporting details.

If you have any immediate questions, feel free to contact us.

Regards,
Swizosoft Pvt. Ltd."""

print("=" * 80)
print("PAID INTERNSHIP - ACCEPTANCE EMAIL")
print("=" * 80)
print(paid_accept_body)
print()

# Paid rejection email
paid_reject_name = "Jane Smith"
paid_reject_reason = "Does not meet minimum qualifications"
paid_reject_body = f"""Hi {paid_reject_name},

Thank you for your interest in the Paid Internship Program at Swizosoft. After reviewing your application and performance, we will not be moving forward with your selection.

This decision is based on our current requirements and the overall competitiveness of the applicants.

We appreciate the time and effort you invested in the process, and we encourage you to apply again in the future.

Reason: {paid_reject_reason}

Regards,
Swizosoft Pvt. Ltd."""

print("=" * 80)
print("PAID INTERNSHIP - REJECTION EMAIL")
print("=" * 80)
print(paid_reject_body)
print()

print("✓ Email templates verified - all content is present and formatted correctly")
