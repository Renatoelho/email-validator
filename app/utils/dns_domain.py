
from subprocess import run, PIPE

from domains import WHITE_LIST
from domains import exception_email_not_validate
from models.syntax_email import SyntaxEmail


def _check_tld(records: list) -> bool:
    try:
        if "could not resolve domain" in "".join(records).lower():
            return False
        else:
            return True
    except Exception as _:
        return False


def _check_mx(records: list) -> bool:
    try:
        if "could not resolve mx records" not in "".join(records).lower():
            list_mx = ["MX" for record in records if "mx " in record.lower()]
            if len(list_mx) > 0:
                return True
            else:
                return False
        else:
                return False
    except Exception as _:
        return False


def _check_email(email: str) -> bool:
    try:
        data = {"syntax_email": email}
        SyntaxEmail(**data)
        return True
    except Exception as _:
        return False


def _define_score(
    return_code_dns_recon: int,
    email: str,
    tld_exists: bool,
    mx_exists: bool,
    email_valid: bool
) -> dict:
    try:
        if return_code_dns_recon in (0, 1):
            if tld_exists and mx_exists and email_valid:
                score = (
                    [
                        True,
                        True,
                        True,
                        90.0,
                        "Trusted email"
                    ]
                )
            elif tld_exists and mx_exists and not email_valid:
                score = (
                    [
                        True,
                        True,
                        False,
                        70.0,
                        "Unreliable email syntax"
                    ]
                )
            elif tld_exists and not mx_exists and not email_valid:
                score = (
                    [
                        True,
                        False,
                        False,
                        45.0,
                        "Only TLD is valid"
                    ]
                )
            elif tld_exists and not mx_exists and email_valid:
                score = (
                    [
                        True,
                        False,
                        True,
                        65.0,
                        "TLD and Syntax email is valid"
                    ]
                )
            else:
                score = (
                    [
                        False,
                        False,
                        False,
                        0.0,
                        "Untrusted email"
                    ]
                )
            return {
                "email": email,
                "domain_tld": score[0],
                "domain_dns_mx": score[1],
                "syntax": score[2],
                "score": score[3],
                "message": score[4]
            }
        else:
            return exception_email_not_validate(email, "erro in dnsrecon")
    except Exception as erro:
        return exception_email_not_validate(email, erro)


def run_dns_record(email: str) -> dict:
    try:
        domain_email = email.split("@")[1].strip()

        if domain_email not in WHITE_LIST:
            command = run(
                [
                    "dnsrecon",
                    "-d",
                    domain_email
                ],
                stdout=PIPE,
                stderr=PIPE
            )
            returncode = command.returncode
            records_dns = command.stdout.decode("utf-8").split("\n")
            tld_exists = _check_tld(records_dns)
            mx_exists = _check_mx(records_dns)
        else:
            tld_exists = True
            mx_exists = True
            returncode = 0

        email_valid = _check_email(email)

        return _define_score(
            returncode,
            email,
            tld_exists,
            mx_exists,
            email_valid
        )
    except Exception as erro:
        return exception_email_not_validate(email, erro)
