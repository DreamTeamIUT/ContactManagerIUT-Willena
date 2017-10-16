class EasyMenu:
    def __init__(self, title):
        self.elements = []
        self.title = title
        self.prompt = ""
        self.multiple = False

    def add_entry(self, name, func, *args):
        element = {'title': name, 'func': func, 'arg': args}
        self.elements.append(element)

    def show_menu(self):
        i = 0
        print(self.title)
        for menu in self.elements:
            i += 1
            print(str(i) + " - " + menu['title'])
        print()

    def set_prompt(self, message):
        self.prompt = message

    def wait_for_choise(self):
        if self.multiple is True:
            tmp = []
            chx = input(self.prompt)
            list = chx.split(",")
            try:
                for l in list:
                    index = int(l) - 1
                    if len(self.elements) > index >= 0:
                        tmp.append(index)
                    else:
                        raise ValueError()
                return tmp
            except ValueError:
                print("Choix invalide, reesayez")
                return self.wait_for_choise()

        else:
            try:
                ch = int(input(self.prompt))  # self.elements[ch]['func']()
                return self.elements[ch - 1]['func'], self.elements[ch - 1]['arg']
            except (ValueError, IndexError):
                print("Choix invalide, reesayez")
                return self.wait_for_choise()

    def set_multiple(self, sel):
        self.multiple = sel

    def clear(self):
        self.elements = []
