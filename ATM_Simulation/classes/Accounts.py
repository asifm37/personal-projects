import pickle

SB_MIN_BAL = 2000
CA_MIN_BAL = 10000


class Account:
    account_number = 0
    __account_password = None
    __account_balance = 0
    _account_type = None
    _account_holder_name = None
    _account_branch = None
    __accounts_dict = {}
    __account_db_file = "resources/accounts_list.data"
    _last_account_number = 1000
    _last_account_file = "resources/last_account.data"

    def __init__(self, account_pin, account_type, customer_name):
        self.account_number = self._get_last_account() + 1
        self._set_last_account(self.account_number)
        self.__account_password = account_pin
        self.__account_balance = 0
        self._account_type = account_type
        self._account_holder_name = customer_name
        self._account_branch = 'HQ - CKM'

    @classmethod
    def _get_last_account(cls):
        try:
            with open(cls._last_account_file, 'rb') as in_file:
                cls._last_account_number = pickle.load(in_file)
        except FileNotFoundError:
            return cls._last_account_number
        return cls._last_account_number

    @classmethod
    def _set_last_account(cls, value):
        cls._last_account_number = value
        with open(cls._last_account_file, 'wb') as output:
            pickle.dump(cls._last_account_number, output)

    def get_type(self):
        return self._account_type

    def get_balance(self):
        return self.__account_balance

    def __get_pin(self):
        return self.__account_password

    @classmethod
    def _update_account(cls, cur_account):
        cls.__accounts_dict.update({cur_account.account_number: cur_account})

    def __set_pin(self, new_pin):
        if len(str(new_pin)) != 4:
            return False, "PASSWORD SHOULD BE 4 DIGIT"
        if self.__get_pin() == new_pin:
            return False, "PASSWORD CANNOT BE SAME AS OLD ONE"
        self.__account_password = new_pin
        self._update_account(self)
        return True, "SUCCESS"

    def get_minimum_balance(self):
        return SB_MIN_BAL if self._account_type == 'SB' else CA_MIN_BAL

    def withdraw(self, amount):
        if amount > 0 and self.__account_balance - amount > self.get_minimum_balance():
            self.__account_balance -= amount
            self._update_account(self)
            return self.__account_balance, "SUCCESS"
        else:
            return False, "INVALID WITHDRAW"

    def deposit(self, amount):
        if amount > 0:
            self.__account_balance += amount
            self._update_account(self)
            return self.__account_balance, "SUCCESS"
        else:
            return False, "INVALID DEPOSIT"

    def transfer(self, to_account_number, amount):
        if to_account_number == self.account_number:
            return False, "CANNOT BE SAME ACCOUNT"
        to_account, msg = Account.__get_account(to_account_number)
        if to_account:
            withdraw_status, msg = self.withdraw(amount)
            if withdraw_status:
                deposit_status, msg = to_account.deposit(amount)
                if deposit_status:
                    return self.__account_balance, f"{msg}\n{amount} is Deposited to {to_account_number} Successfully!"
            else:
                return False, msg
        else:
            return False, msg

    def change_pin(self, current_pin, new_pin):
        status, msg = self.authenticate_account(current_pin)
        if status:
            return self.__set_pin(new_pin)
        else:
            return False, msg

    def authenticate_account(self, account_pin):
        if self.__account_password == account_pin:
            return True, f"Welcome {self._account_holder_name.title()} to CKM Bank ATM"
        else:
            return False, f"Invalid Password for {self.account_number}!"

    @classmethod
    def __get_account(cls, account_number):
        for acc_num, cur_account in cls.__accounts_dict.items():
            if acc_num == account_number:
                return cur_account, f"Account {account_number} is Found!"
        return None, f"Account {account_number} is Not Found in our Bank!"

    @classmethod
    def get_authenticated_account(cls, account_number, account_pin):
        cur_account, msg = cls.__get_account(account_number)
        if cur_account:
            status, msg = cur_account.authenticate_account(account_pin)
            if status:
                return cur_account, msg
        return None, msg

    @classmethod
    def create_account(cls, name, acc_type, pin):
        cur_account = Account(pin, acc_type, name)
        cls.__accounts_dict[cur_account.account_number] = cur_account
        return True, f"Your Account Created Successfully!\n\tYour Account Number is {cur_account.account_number}"

    @classmethod
    def save_accounts_to_file(cls):
        with open(cls.__account_db_file, 'wb') as output:
            pickle.dump(cls.__accounts_dict, output, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def read_account_to_memory(cls):
        try:
            with open(cls.__account_db_file, 'rb') as in_file:
                cls.__accounts_dict = pickle.load(in_file)
            cls.print_account_table()
        except FileNotFoundError:
            pass

    @classmethod
    def print_account_table(cls):
        print('+', "-"*74, '+', sep='')
        print(f"|{'Account Number'.center(16)}|{'Type'.center(6)}|{'Name'.center(18)}|{'Branch'.center(10)}"
              f"|{'Balance'.rjust(20)}|")
        print('+', "-" * 74, '+', sep='')
        for _, cur_account in cls.__accounts_dict.items():
            print(cur_account)
        print('+', "-"*74, '+', sep='')

    def __str__(self) -> str:
        return f"|{str(self.account_number).center(16)}|{self._account_type.center(6)}|" \
               f"{self._account_holder_name.title().center(18)}|{self._account_branch.center(10)}|" \
               f"{str(self.__account_balance).rjust(20)}|"
