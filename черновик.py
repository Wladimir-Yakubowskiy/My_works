
class Cat:

    name = 'Васька'
    age = 6


    def widgets(self):
        name_label = Label(Cat.window, text=Cat.name)
        age_label = Label(Cat.window, text=Cat.age)
        name_label.pack()
        age_label.pack()


    def words(self):
        self.widgets.name_label.config(text='Это хороший кот!')
        self.widgets(Cat)

Cat.words(Cat)

