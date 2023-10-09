
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


def exception_email_not_validate(email: str, message: str) -> dict:
    return {
        "email": email,
        "domain_tld": False,
        "domain_dns_mx": False,
        "syntax": False,
        "score": -1,
        "message": f"Email not validated - {message}"
    }


def content_error_response(message: str) -> dict:
    return (
        {
            "status": False,
            "erro": message
        }
    )
