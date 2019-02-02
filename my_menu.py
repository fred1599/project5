class Menus(list):

    def __init__(self):
        super().__init__(self)
        self.actual_index = -1

    def __add__(self, menu):
        if isinstance(menu, Menu):
            self.append(menu)
            self.actual_index += 1
        else:
            raise TypeError("{} est pas une liste !".
                    format(menu))
        return self

    def get_precedent(self):
        if self.actual_index > 0:
            menu = self[self.actual_index-1]
            self.actual_index -= 1
        else:
            menu = self[self.actual_index]
        return menu

    def get_suivant(self):
        self.actual = self.actual_index + 1
        if self.actual >= len(self):
            return self[-1]
        self.actual += 1
        return self[self.actual]

class Menu:
    def __init__(self, content):
        assert isinstance(content, list)
        self.content = content
        if not self.content:
            self.content = []

    def display(self):
        for ind, value in enumerate(self.content):
            line = '{}: {}'.format(ind+1, value)
            print(line)

    def _get_choice(self):
        limit = len(self.content)
        choice = input('Faîtes votre choix (r pour revenir): ')
        if choice == 'r':
            return choice
        try:
            choice = int(choice)
            if choice in range(1, limit+1):
                return choice
        except ValueError:
            pass
        return self._get_choice()

    def get_value(self, menus):
        choice = self._get_choice()
        if choice == 'r':
            menu = menus.get_precedent()
            return menu
        return self.content[choice-1]

