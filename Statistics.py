from settings import COUNT_CRT

class Statistic:
    def __init__(self):
        # PER DAY
        self.birth_at_day = 0
        self.BIRTH_PER_DAY = []

        self.ALIVE_PER_DAY = [COUNT_CRT]

        self.dead_at_day = 0
        self.DEAD_PER_DAY = []

        self.mut_at_day = 0
        self.MUT_PER_DAY = []

        self.DOM_VS_OTHER = []

        # DIGITS

        self.oldest_alive_breed = 1
        self.youngest_alive_breed = 1
        self.avarage_day = 1
        self.oldest_creature = 1

    def reset(self):
        self.ALIVE_PER_DAY = [COUNT_CRT]
        self.DEAD_PER_DAY = []
        self.MUT_PER_DAY = []
        self.DOM_VS_OTHER = []

        self.birth_at_day = 0
        self.dead_at_day = 0
        self.mut_at_day = 0

    def new_day(self, alive):
        self.BIRTH_PER_DAY.append(self.birth_at_day)
        self.ALIVE_PER_DAY.append(alive)
        self.DEAD_PER_DAY.append(self.dead_at_day)
        self.MUT_PER_DAY.append(self.mut_at_day)

        self.birth_at_day = 0
        self.dead_at_day = 0
        self.mut_at_day = 0

    def get(self):
        print(self.BIRTH_PER_DAY)
        print(self.DEAD_PER_DAY)
        print(self.MUT_PER_DAY)
        print(self.ALIVE_PER_DAY)