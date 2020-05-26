from getpass import getpass
from classes.Accounts import Account

RETRY = 3
WIN_WIDTH = 60


def retry_logic(func):
    def inner(*args, **kwargs):
        retry = RETRY
        while retry > 0:
            result = func(*args, **kwargs)
            if result:
                return result
            else:
                retry -= 1
        return None
    return inner


def print_and_binary_choice(msg):
    choice = input(f"{msg.title()} [(Y)es/(N)o]: ")
    return True if choice.upper().startswith('Y') else False


@retry_logic
def print_and_get_option(options_list):
    for num, option in enumerate(options_list, start=1):
        print(f" > {num} - {option}".title())
    try:
        choice = int(input("Select Your Option: "))
        if 0 < choice <= len(options_list):
            return options_list[choice-1]
    except ValueError:
        return None
    return None


@retry_logic
def get_pin(msg="Current"):
    pin_str = getpass(f"Enter Your {msg} 4-Digit Password:", None)
    try:
        assert len(str(pin_str)) == 4
        _ = int(pin_str)
        return pin_str
    except ValueError:
        print("PIN SHOULD BE 4-Digits")
    except AssertionError:
        print("PIN SHOULD BE 4-Digit Numbers")
    return False


@retry_logic
def get_valid_amount_input(transaction_type="this", restrict_amount=None):
    while True:
        try:
            amount = float(input(f"Enter The Amount for {transaction_type.title()} Transaction: "))
            if restrict_amount:
                assert int(amount) % 100 == 0
            return amount
        except ValueError:
            print("Invalid Amount Input Try Again!")
        except AssertionError:
            print("Amount Should be Multiple of 100's")


def print_title(msg, box=False):
    if box:
        print('\n', '-'*WIN_WIDTH, sep='')
    print(f" {msg} ".center(WIN_WIDTH, '-'), sep='')


def print_center(msg):
    print(msg.center(WIN_WIDTH))


class ATM:
    atm_id = 100

    def __init__(self):
        self.atm_id = ATM.atm_id + 1
        self.location = 'CKM'
        self.cur_account = None
        self.continue_transaction = True
        self.main_menu = {"create account": ATM.create_account,
                          "banking": self.account_transactions,
                          "exit": self.save_and_exit}
        self.transaction_menu = {"withdraw": self.withdraw_screen,
                                 "deposit": self.deposit_screen,
                                 "balance enquiry": self.get_balance_screen,
                                 "transfer": self.transfer_screen,
                                 "change pin": self.change_pin_screen,
                                 "back": self.set_continue_transaction,
                                 "exit": self.save_and_exit}
        Account.read_account_to_memory()

    @classmethod
    def save_and_exit(cls):
        print_title("Saving and Exiting")
        Account.save_accounts_to_file()
        exit(0)

    @staticmethod
    def create_account():
        print_title("Create New Account at CKM Bank")
        acc_type = str(input("Which Type of Account You Wish to Create\n"
                             " [SB - Saving Account, CA - Current Account]: "))
        username = str(input("Enter Your Full Name: "))
        pin = get_pin()
        if pin:
            status, msg = Account.create_account(username, acc_type.upper(), pin)
            print_title(msg) if status else print("Oops Something Went Wrong!\n" + msg + "Try Again")
        else:
            print_title("Too Many Tries!")
            return None

    @staticmethod
    def _get_account():
        account_number = int(input("Enter Your Account Number: "))
        account_pin = get_pin()
        if account_pin:
            account_obj, msg = Account.get_authenticated_account(account_number, account_pin)
            print_title(msg)
            return account_obj if account_obj else None
        else:
            print_title("Too Many Tries!")
            return None

    def account_transactions(self):
        print_title("Account Transaction")
        self.cur_account = ATM._get_account()
        self.set_continue_transaction(True)
        while self.continue_transaction and self.cur_account:
            transaction_option = print_and_get_option(list(self.transaction_menu.keys()))
            if transaction_option:
                self.transaction_menu[transaction_option]()
                # self.set_continue_transaction(print_and_binary_choice("Would you like to continue the Transaction"))
            else:
                print_title("Too Many Tries!")
                self.set_continue_transaction()
        print_title("Transaction is Complete... Bye!")
        del self.cur_account

    def withdraw_screen(self):
        print_title("Withdraw Transaction")
        amount = get_valid_amount_input("withdraw", restrict_amount=100)
        cur_balance, msg = self.cur_account.withdraw(amount)
        if cur_balance:
            print_title(f"Withdraw is Successful")
            self.get_balance_screen()
        else:
            print_title(f"Withdraw is Failed\n MSG: {msg}")

    def deposit_screen(self):
        print_title("Deposit Transaction")
        amount = get_valid_amount_input("deposit")
        cur_balance, msg = self.cur_account.deposit(amount)
        if cur_balance:
            print_title(f"Deposit is Successful")
            self.get_balance_screen()
        else:
            print_title(f"Deposit is Failed\n MSG: {msg}")

    def get_balance_screen(self):
        print_title("Current Balance")
        print(f"Your {self.cur_account.get_type()} Account Current Balance is {self.cur_account.get_balance()}"
              .center(WIN_WIDTH))
        print_title("~*~")

    def transfer_screen(self):
        print_title("Transfer Transaction")
        to_account_number = int(input("Enter The Recipient Account Number: "))
        amount = get_valid_amount_input("transfer")
        cur_balance, msg = self.cur_account.transfer(to_account_number, amount)
        if cur_balance:
            print_title(f"Transfer is Complete\n")
            self.get_balance_screen()
        else:
            print_title(f"Transfer is Failed. MSG: {msg}")

    def change_pin_screen(self):
        print_title("Change Your Account PIN")
        current_pin = get_pin("Old")
        new_pin = get_pin("New")
        if current_pin and new_pin:
            status, msg = self.cur_account.change_pin(current_pin, new_pin)
        else:
            status = False
            msg = "Too Many Invalid Inputs"
        if status:
            print_center(f"PIN Change for the {self.cur_account.account_number} is Successful!")
            print_title(f"STATUS: {msg}")
        else:
            print_title(f"PIN Change is Failed! STATUS: {msg}")
        self.set_continue_transaction()

    def set_continue_transaction(self, change_state=False):
        self.continue_transaction = change_state

    def main_screen(self):
        while True:
            print_title("Welcome to CKM Bank ATM", box=True)
            main_option = print_and_get_option(list(self.main_menu.keys()))
            if main_option:
                self.main_menu[main_option]()
            else:
                print_title("Too Many Tries. Exiting... Bye!")


atm_obj = ATM()
atm_obj.main_screen()
