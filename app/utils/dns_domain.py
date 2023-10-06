
from re import search
from subprocess import run, PIPE

from domains import WHITE_LIST
from domains import exception_email_not_validate

def _check_tld(records: list) -> bool:
    try:
        check = [index for index, record in enumerate(records) if "could not resolve domain" in record.lower()]
        if len(check) > 0:
            return True
        else:
            return False
    except Exception as _:
        return False

def _count_record_mx(records: list) -> int:
    try:
        check = [index for index, record in enumerate(records) if "mx " in record.lower()]
        if len(check) > 0:
            return len(check)
        else:
            return 0
    except Exception as _:
        return 0

def _check_user_name_email(user_name_email: str) -> bool:
    try:
        if search(r"^[a-zA-Z0-9._%+-]+$", user_name_email):
            return True
        else:
            return False
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
        if return_code_dns_recon == 0:
            if tld_exists and count_mx > 0 and email_valid:
                score = [True, True, True, 90.0, "Trusted email"]
            elif tld_exists and count_mx > 0 and not email_valid:
                score = [True, True, False, 70.0, "Invalid email username syntax"]
            elif tld_exists and count_mx == 0 and not email_valid:
                score = [True, False, False, 45.0, "Only TLD is valid"]
            elif tld_exists and count_mx == 0 and email_valid:
                score = [True, False, True, 65.0, "TLD and name user mail is valid"]
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
        user_email = email.split("@")[0]
        domain_email = email.split("@")[1].strip()

        command = run(["dnsrecon", "-d", domain_email], stdout=PIPE, stderr=PIPE)
        records_dns = command.stdout.decode("utf-8").split("\n")

        if domain_email not in WHITE_LIST:
            tld_exists = _check_tld(records_dns)
            count_mx = _count_record_mx(records_dns)
        else:
            tld_exists = True
            count_mx = 1
        
        user_email_valid = _check_user_name_email(user_email)
        
        return _define_score(command.returncode, email, tld_exists, count_mx, user_email_valid)
    except Exception as erro:
        return exception_email_not_validate(email, erro)
