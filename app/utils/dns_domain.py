from subprocess import run, PIPE


def _check_tld(records: list) -> bool:
    try:
        check = [index for index, record in enumerate(records) if "require".lower() in record]
        if len(check) > 0:
            return True
        else:
            return False
    except Exception as _:
        return False

def _count_record_mx(records: list) -> int:
    try:
        check = [index for index, record in enumerate(records) if ".py".lower() in record]
        if len(check) > 0:
            return len(check)
        else:
            return 0
    except Exception as _:
        return 0

def _check_user_name_email(user_email: str) -> bool:
    try:
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
        if return_code_dns_recon == 0:
            if tld_exists and count_mx > 0 and email_valid:
                score = [True, True, True, 90.0, "Email valid"]
            elif tld_exists and count_mx > 0 and not email_valid:
                score = [True, True, False, 70.0, "Syntax user email invalid"]
            elif tld_exists and count_mx == 0 and not email_valid:
                score = [True, False, False, 45.0, "Only TLD is valid"]
            else:
                score = [False, False, False, 0.0, "Email invalid"]
            return {
                "email": email,
                "domain_tld": score[0],
                "domain_dns_mx": score[1],
                "syntax": score[2],
                "score": score[3],
                "mensage": score[4]
            }
        else:
            return {
                "email": email,
                "domain_tld": False,
                "domain_dns_mx": False,
                "syntax": False,
                "score": 0,
                "mensage": "Unable to validate email."
            }
    except Exception as _:
        return {
            "email": email,
            "domain_tld": False,
            "domain_dns_mx": False,
            "syntax": False,
            "score": 0,
            "mensage": "Unable to validate email."
        }    

def run_dns_record(email: str) -> str:
    try:
        user_email = email.split("@")[0].strip()
        #domain_email = email.split("@")[1].strip()
        domain_email = "-lha"
        print(user_email, "="*5, domain_email)

        command = run(["ls", domain_email], stdout=PIPE, stderr=PIPE)
        print(_define_score(command.returncode, email, True, 0, True))
    except Exception as _:
        print(_)
