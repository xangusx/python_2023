import sys

class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

class Record:
    """
    instance = Record(category,description,amount)

    instance.category
        return category

    instance.description
        return description

    instance.amount
        return amount
    """
    def __init__(self,category,description,amount):
        self._category = category
        self._description = description
        self._amount = amount
    
    @property
    def category(self):
        return self._category
    # @category.setter
    # def category(self,item):
    @property
    def description(self):
        return self._description
    # @description.setter
    # def description(self,item):

    @property
    def amount(self):
        return self._amount
    # @amount.setter
    # def amount(self,value):
    #     self._amount = int(value)
    #     print("set amount")
    
class Records:
    """Maintain a list of all the 'Record's and the initial amount of money.

    add(record,categories)
        Add a record to the record list.

    view()
        Display all the records.

    delete(category)
        Delete the special category you selete in the records.

    find(category,target_categories)
        Find the special category you selete in the records.

    save()
        Save all records in the records.txt .   
    """

    def __init__(self):
        filename = 'records.txt'
        self._initial_money = 0
        self._records = list()
        try:
            with open(filename, 'r') as f:
                try:
                    self._initial_money = int(f.readline().strip())
                except:
                    print(f"{bcolors.FAIL}initial money is lost!{bcolors.RESET}")
                    self._initial_money = int(input(f'{bcolors.WARNING}How much money do you have?{bcolors.RESET}'))
                try:
                    bill_list = f.readlines()
                    if len(bill_list) == 0 or bill_list[0] == '\n':
                        raise ImportError(f"{bcolors.FAIL}file is empty!{bcolors.RESET}")
                    for line in bill_list:
                        try:
                            val = line.split(",")
                            if len(val) != 3 :
                                raise ValueError(f"{bcolors.FAIL}file format error, some records may be lost!{bcolors.RESET}")    
                            else:
                                self._records.append(Record(val[0], val[1], int(val[2])))
                        except ValueError as error:
                            print(error)
                except ImportError as error:
                    print(error)
                finally:
                    f.close()
                    print(f"{bcolors.OK}Welcome back!{bcolors.RESET}")
        except FileNotFoundError:
            try:
                initial_money = int(input(f'{bcolors.WARNING}How much money do you have?{bcolors.RESET}'))
            except:
                print(f"{bcolors.FAIL}Invalid value for money. Set to 0 by default.{bcolors.RESET}\n")

    def add(self,record,categories):
        try:
            record_list = [ item.split(" ") for item in record.strip().split(", ")]
            for i in record_list:
                if len(i) != 3:
                    raise ValueError(f"{bcolors.FAIL}The format of a record should be like this: food breakfast -50. \nFail to add a record.{bcolors.RESET}")
                elif categories.is_category_valid(i[0]):
                # else:
                    i[2] = int(i[2])
                    if i[2] == 0:
                        raise ValueError(f"{bcolors.FAIL}Amount cannot be zero.{bcolors.RESET}")
                    record = Record(i[0], i[1], i[2])
                    self._records.append(record)
                    self._initial_money += i[2]          
        except ValueError as error:
            print(error)


    def view(self):
        print("Here's your expense and income records:")
        print("Category        Description          Amount")
        print("=============== ==================== ======")
        for item in self._records:
            if item.amount >= 0:
                print(f"{item.category:15s} {item.description:20s} {bcolors.OK}{item.amount}{bcolors.RESET}")
            else: print(f"{item.category:15s} {item.description:20s} {bcolors.FAIL}{item.amount}{bcolors.RESET}")
        print("===========================================")
        if self._initial_money >=0 :
            print(f"Now you have {bcolors.OK}{self._initial_money}{bcolors.RESET} dollars.")
        else: 
            print(f"Now you have {bcolors.FAIL}{self._initial_money}{bcolors.RESET} dollars.")


    def delete(self,category):
        filter_records = filter(lambda item : item.category == category, self._records)
        if not filter_records : 
            print(f"{bcolors.FAIL}Doesn't find the {category} in records{bcolors.RESET}")
        else:
            filter_list = list(filter_records)
            print("Index Category        Description          Amount")
            print("===== =============== ==================== ======")
            for index, item in enumerate(filter_list):
                    if item.amount >= 0:
                        print(f"{index:5d} {item.category:15s} {item.description:20s} {bcolors.OK}{item.amount}{bcolors.RESET}")
                    else: print(f"{index:5d} {item.category:15s} {item.description:20s} {bcolors.FAIL}{item.amount}{bcolors.RESET}") 
            print("=================================================")
            delete_index = int(input("which index you want to delete?"))
            for index, item in enumerate(filter_list):
                if delete_index == index:
                    self._initial_money -= item.amount
                    print(f"{bcolors.OK}remove {item.category} {item.description} {item.amount} successfully!{bcolors.RESET}")
                    self._records.remove(item)
                      

    def find(self,category,target_categories):
        if target_categories == []:
            print(f"{bcolors.FAIL}Doesn't have this category{bcolors.RESET}")
            return
        filter_records = filter(lambda i : i.category in target_categories, self._records)
        filter_list = list(filter_records)
        if not filter_list : 
            print(f"{bcolors.FAIL}Doesn't find the {category} in records{bcolors.RESET}")
        else :
            total = 0
            print(f"Here's your expense and income records under category \"{category}\":")
            print("Category        Description          Amount")
            print("=============== ==================== ======")
            for item in filter_list:
                total += item.amount
                if item.amount >= 0:
                    print(f"{item.category:15s} {item.description:20s} {bcolors.OK}{item.amount}{bcolors.RESET}")
                else: print(f"{item.category:15s} {item.description:20s} {bcolors.FAIL}{item.amount}{bcolors.RESET}") 
            print("===========================================")
            if total >= 0:
                print(f"The total amount above is {bcolors.OK}{total}{bcolors.RESET}.")
            else: print(f"The total amount above is {bcolors.FAIL}{total}{bcolors.RESET}.")

    def save(self):
        with open('records.txt','w') as f:
            f.write(str(self._initial_money) + '\n')
            record_str = []
            for item in self._records:
                record_single = item.category + ',' + item.description + ',' + str(item.amount)
                record_str.append(record_single + '\n')
            f.writelines(record_str)
            f.close()
        print(f"{bcolors.OK}save the records file{bcolors.RESET}")

class Categories:
    """Maintain the category list and provide some methods.

    view()
        View all the categories in the records.
    
    is_category_valid(category)
        Check the category is valid.

    find_subcategories(category)
        Find the category and the subcategories that you select.
    """
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

    @property
    def categories(self):
        return self._categories

    def view(self):
        def indent_list(L, level=-1):
            if L == None:
                return
            if type(L) in {list, tuple}:
                for child in L:
                    indent_list(child, level+1)
            else:
                print(f'{" "*2*level}- {L}')
        indent_list(self._categories)

    def is_category_valid(self,category):
        def category_valid(category,categories):
            if category in categories:
                return True
            for sub_category in categories:
                if type(sub_category) == list :
                    if category_valid(category,sub_category):
                        return True
            return False
        return category_valid(category,self._categories)

    def find_subcategories(self, category):
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                        and type(categories[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(category, categories[index + 1], True)
            else:
                if categories == category or found:
                    yield categories

        return list(find_subcategories_gen(category, self._categories))

    # def _flatten(self, L):
    #     if type(L) == list:
    #         result = []
    #         for child in L:
    #             result.extend(flatten(child))
    #         return result
    #     else:
    #         return [L]

categories = Categories()
records = Records()

while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / find / exit)? ')
    if command == 'add':
        record = input('Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n')
        records.add(record, categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        category = input("Which category do you want to delete? ")
        records.delete(category)
    elif command == 'view categories':
        categories.view()
    elif command == 'find':
        category = input('Which category do you want to find? ')
        target_categories = categories.find_subcategories(category)
        # print(target_categories)
        records.find(category,target_categories)
    elif command == 'exit':
        records.save()
        break
    else:
        sys.stderr.write('Invalid command. Try again.\n')
