
from subprocess import run, PIPE

from models.syntax_email import SyntaxEmail

from domains import WHITE_LIST
from domains import exception_email_not_validate

def _check_tld(records: list) -> bool:
    try:
        check = [record.lower() for record in records]
        if "could not resolve domain" in check:
            return False
        else:
            return True
    except Exception as _:
        return False

def _count_record_mx(records: list) -> int:
    try:
        check = [record.lower() for record in records]
        if "mx " in check:
            return 1
        else:
            return 0
    except Exception as _:
        return 0

def _check_email(email: str) -> bool:
    try:
        data = {"syntax_email": email}
        _ = SyntaxEmail(**data)
        return True
    except Exception as _:
        return False

def _define_score(
    return_code_dns_recon: int,
    email: str,
    tld_exists: bool,
    count_mx: int,
    email_valid: bool
) -> dict:
    try:
        if return_code_dns_recon in (0, 1):
            if tld_exists and count_mx > 0 and email_valid:
                score = [True, True, True, 90.0, "Trusted email"]
            elif tld_exists and count_mx > 0 and not email_valid:
                score = [True, True, False, 70.0, "unreliable email syntax"]
            elif tld_exists and count_mx == 0 and not email_valid:
                score = [True, False, False, 45.0, "Only TLD is valid"]
            elif tld_exists and count_mx == 0 and email_valid:
                score = [True, False, True, 65.0, "TLD and Email is valid"]
            else:
                score = [False, False, False, 0.0, "Untrusted email"]
            return {
                "email": email,
                "domain_tld": score[0],
                "domain_dns_mx": score[1],
                "syntax": score[2],
                "score": score[3],
                "mensage": score[4]
            }
        else:
            return exception_email_not_validate(email, "erro in dnsrecon")
    except Exception as erro:
        return exception_email_not_validate(email, erro)  

def run_dns_record(email: str) -> dict:
    try:
        domain_email = email.split("@")[1].strip()

        if domain_email not in WHITE_LIST:
            command = run(["dnsrecon", "-d", domain_email], stdout=PIPE, stderr=PIPE)
            returncode = command.returncode
            records_dns = command.stdout.decode("utf-8").split("\n")
            tld_exists = _check_tld(records_dns)
            count_mx = _count_record_mx(records_dns)
        else:
            tld_exists = True
            count_mx = 1
            returncode = 0
        
        email_valid = _check_email(email)
        
        return _define_score(returncode, email, tld_exists, count_mx, email_valid)
    except Exception as erro:
        return exception_email_not_validate(email, erro)
