def split_phone_email(records, source_col="Email", phone_col="Téléphone", email_col="Email"):
    """
    Splits combined phone+email field into separate columns.
    Assumes phone comes first, email comes second.
    """
    for row in records:
        field = row.get(source_col, "").strip()
        if field:
            parts = field.split()  # split by whitespace
            if len(parts) >= 2:
                # Phone = everything except last part
                phone = " ".join(parts[:-1]).strip()
                email = parts[-1].strip()

                row[phone_col] = phone
                row[email_col] = email
    return records