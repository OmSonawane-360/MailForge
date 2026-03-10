from email_validator import validate_email, EmailNotValidError


def validate_email_list(email_list):
    valid_emails = []
    invalid_emails = []

    for email in email_list:
        try:
            # Normalize and validate
            v = validate_email(email)
            normalized_email = v.email
            valid_emails.append(normalized_email)

        except EmailNotValidError:
            invalid_emails.append(email)

    return {
        "valid_emails": valid_emails,
        "valid_count": len(valid_emails),
        "invalid_emails": invalid_emails,
        "invalid_count": len(invalid_emails),
    }