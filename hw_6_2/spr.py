
# --------------------------- Homework_6.2  ------------------------------------

'''

Виконав: Роман Стебельський

Homework_6.2 Принцип єдиної відповідальності

'''



# SRP
class BankAccounting:

    def __init__(self, account_no: str):
        self.accounts_list: list[str] = []
        self.save(account_no)

    def save(self, account_no: str) -> None:
        self.accounts_list.append(account_no)
        print("Success, saved to DB")


class BankAccount:

    @staticmethod
    def get_account_numbers(Bank: BankAccounting):
        return Bank.accounts_list

    @staticmethod
    def search_account_number(Bank: BankAccounting, id_acc: int):
        return Bank.accounts_list[id_acc]

if __name__ == "__main__":

    b_acc = BankAccounting('26001')
    b_acc.save('26002')
    b_acc.save('26003')

    list_acc = BankAccount.get_account_numbers(b_acc)
    print(list_acc)
    acc = BankAccount.search_account_number(b_acc, 2)
    print(acc)

'''

Результат:

Success, saved to DB
Success, saved to DB
Success, saved to DB
['26001', '26002', '26003']
26003

'''