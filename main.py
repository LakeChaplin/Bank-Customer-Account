import uuid


class BankAccount:
    def __init__(self, owner, balance=0):
        self.account_number = uuid.uuid4()
        self.balance = balance
        self.owner = owner

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            return 'insufficient funds'
        self.balance -= amount

    def transfer_to(self, bank, account_number, amount):
        if amount > self.balance:
            return 'insufficient funds'
        self.withdraw(amount)
        target_account = BankAccount.get_account_by_number(bank, account_number)
        if not target_account:
            return 'target account not found'
        target_account.deposit(amount)

        return 'transfer completed'

    @classmethod
    def get_account_by_number(cls, bank, account_number):
        for customer in bank.customers:
            for account in customer.accounts:
                if account.account_number == account_number:
                    return account
        return None

    @classmethod
    def get_customer_accounts(cls, bank, customer_id):
        for customer in bank.customers:
            if customer.customer_id == customer_id:
                return customer.accounts
        return None


class BankCustomer:
    def __init__(self, name):
        self.customer_id = uuid.uuid4()
        self.name = name
        self.accounts = []

    def add_account(self, account):
        self.accounts.append(account)

    def create_account(self, initial_balance):
        new_account = BankAccount(self, initial_balance)
        self.add_account(new_account)

    def get_customer_id(self):
        return self.customer_id


class Bank:
    def __init__(self, name):
        self.name = name
        self.customers = []

    def add_customer(self, customer):
        if customer not in self.customers:
            self.customers.append(customer)

    def get_customer_accounts(self, customer_id):
        for customer in self.customers:
            if customer.get_customer_id() == customer_id:
                return customer.accounts

        return None

    def create_customer(self, name):
        new_customer = BankCustomer(name)
        self.add_customer(new_customer)

    def get_all_customers(self):
        return self.customers



# Создаем банк
tinkoff = Bank('Tinkoff')

# Создаем клиентов
elon = BankCustomer('Elon Musk')
peter = BankCustomer('Peter Thiel')

# Добавляем клиентов в банк
tinkoff.add_customer(elon)
tinkoff.add_customer(peter)

# Создаем счета для клиентов
elon.create_account(1000000)
peter.create_account(500000)

# Проверяем балансы счетов
print(f'Elon Musk\'s balance: {elon.accounts[0].balance}')
print(f'Peter Thiel\'s balance: {peter.accounts[0].balance}')

# Выполняем перевод между счетами
target_account = BankAccount.get_account_by_number(tinkoff, peter.accounts[0].account_number)
result = elon.accounts[0].transfer_to(tinkoff, peter.accounts[0].account_number, 50000)
print(result)

# Проверяем балансы после перевода
print(f'Elon Musk\'s balance: {elon.accounts[0].balance}')
print(f'Peter Thiel\'s balance: {peter.accounts[0].balance}')

# Получаем список всех клиентов банка
all_customers = tinkoff.get_all_customers()
for customer in all_customers:
    print(f'Customer: {customer.name}')



