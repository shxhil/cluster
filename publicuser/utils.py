


def generate_username(name,mobile_number,year):
        first_chars=name[:4].lower()

        last_mobile=str(mobile_number[-4:])

        year_last=str((year)[-2:])

        return first_chars + last_mobile + year_last