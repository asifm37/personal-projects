from datetime import date, datetime


def calculateAge(birth_date, cur_date):
    today = date.today()
    if (today.month, today.day) == (birth_date.month, birth_date.day):
        print("\n", " Happy Birthday! ".center(100, '-'))
        if today == birth_date:
            print("Welcome to Day 0 :-p".center(100))

    if birth_date < cur_date:
        date_diff = cur_date - birth_date
        if (cur_date.month, cur_date.day) < (birth_date.month, birth_date.day):
            years = cur_date.year - birth_date.year - 1
            months = 12 + (cur_date.month - birth_date.month)
        else:
            years = cur_date.year - birth_date.year
            months = cur_date.month - birth_date.month

        if cur_date.day < birth_date.day:
            months -= 1
            days = (date(1, cur_date.month + 1, 1) - date(1, cur_date.month, 1)).days - (birth_date.day - cur_date.day)
        else:
            days = cur_date.day - birth_date.day

        print(" Age ".center(100, '-'))
        print(f"{years} Years, {months} Months, {days} Days".center(100))
        print(f"or {date_diff.days} Days".center(100))
        print(f"or {date_diff.total_seconds()} total Seconds".center(100))
    else:
        print("Date of birth needs to be earlier than the age at date.")


# Driver Program
date_format = "%d-%m-%Y"
try:
    birth_date = datetime.strptime(input("Enter Your Date of Birth (DD-MM-YYYY): "), date_format).date()
    # print(birth_date)

    today_date = date.today()
    cur_date = input(f"Age at the Date of (Default: {date.today().strftime(date_format)}): ")
    if cur_date:
        cur_date = datetime.strptime(cur_date, date_format).date()
    else:
        cur_date = today_date
    # print(cur_date)

    calculateAge(birth_date, cur_date)
except ValueError:
    print("\n", " INVALID INPUT ".center(100, '-'))
    print("Input Should be in DD-MM-YYYY Format Only".center(100))
    print("OR Invalid Date. Please Try Again!!!".center(100))
