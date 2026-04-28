ALLOWED_EMAIL_DOMAINS = {
    'gmail.com',
    'hotmail.com',
    'yahoo.com',
    'academico.ifpb.edu.br',
}


def email_domain_is_allowed(email):
    domain = email.split('@')[-1].lower()
    return domain in ALLOWED_EMAIL_DOMAINS
