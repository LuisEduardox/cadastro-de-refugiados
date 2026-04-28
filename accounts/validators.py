from django.core.exceptions import ValidationError

ALLOWED_EMAIL_DOMAINS = {
    'gmail.com',
    'hotmail.com',
    'yahoo.com',
    'academico.ifpb.edu.br',
}

BLACKLISTED_PASSWORDS = {
    '123456', '123456789', 'brasil', '12345', '102030', 'senha', '12345678',
    '1234', '10203', '123123', '123', '1234567', '654321', '1234567890',
    'gabriel', 'abc123', 'q1w2e3r4t5y6', '101010', '159753', '123321',
    'senha123', 'mirantte', 'flamengo', 'felicidade', 'qwerty', 'felipe',
    '121212', '111111', '142536', 'familia', 'password', 'sucesso', 'vitoria',
    'matheus', 'rafael', 'junior', '112233', 'gustavo', 'mariana', '1q2w3e4r',
    '000000', 'novo', '131313', 'lucas123', 'estrela', 'daniel', 'musica',
    'camila', 'eduardo', 'guilherme',
}


def email_domain_is_allowed(email):
    domain = email.split('@')[-1].lower()
    return domain in ALLOWED_EMAIL_DOMAINS


class BlacklistedPasswordValidator:
    def validate(self, password, user=None):
        if password.lower() in BLACKLISTED_PASSWORDS:
            raise ValidationError(
                "Essa senha é muito comum. Por favor, escolha uma senha mais segura.",
                code='password_blacklisted',
            )

    def get_help_text(self):
        return "Sua senha não pode ser uma das senhas mais comuns."
