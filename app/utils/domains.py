
WHITE_LIST = (
    [
        "gmail.com",
        "yahoo.com",
        "hotmail.com",
        "outlook.com",
        "icloud.com",
        "live.com"
    ]
)


def exception_email_not_validate(email: str, mensage: str) -> dict:
    return {
        "email": email,
        "domain_tld": False,
        "domain_dns_mx": False,
        "syntax": False,
        "score": -1,
        "mensage": f"Email not validated - {mensage}"
    }
