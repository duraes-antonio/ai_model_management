from typing import TypeVar, Tuple

import keras
from keras.models import Model
from keras.callbacks import Callback, History

T = TypeVar('T')

Size = Tuple[int, int]


class SaveCallback(Callback):

    def on_train_end(self, logs=None):
        model: Model = self.model
        history: keras.callbacks.History = model.history
        print(history)

