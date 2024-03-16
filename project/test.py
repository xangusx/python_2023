class Categories:
    def __init__(self):
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

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

    def is_category_valid(self,category):
        def category_vaild(category,categories):
            if category in categories:
                return True

            for sub_category in categories:
                print(sub_category)
                print(type(sub_category))
                if type(sub_category) in {list} :
                    if category_vaild(category,sub_category):
                        return True
            return False
        return category_vaild(category,self._categories)

categories = Categories()
category = input('Which category do you want to find? ')
# target_categories = categories.find_subcategories(category)
# print(target_categories)
print(categories.is_category_valid(category))


