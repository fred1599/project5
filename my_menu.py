class Menu(list):
    def __init__(self):
        super().__init__()
        self.index = -1

    def add(self, objects):
        new_menu = []

        for obj in objects:
            new_menu.append(obj)

        self.index += 1
        self.append(new_menu)

    def get_choice(self):
        

        choice = input('Entrer votre choix: ')

        if choice == 'r':
            if self.index - 1 >= 0:
                self.pop(self.index)
                self.index -= 1

        else:
            try:
                choice = int(choice)
                if 1 <= choice <= len(self[self.index]):
                    return choice-1
                else:
                    return None
            except ValueError:
                return None

    def display(self):
        menu = self[self.index]

        for ind, obj in enumerate(self[self.index], start=1):
            print('{}: {}'.format(ind, obj))