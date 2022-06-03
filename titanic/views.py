from context.models import Model
from context.domains import Dataset
from icecream import ic

class TitanicView:
    model = Model()
    dataset = Dataset()

    def modeling(self, train, test):
        model = self.model

