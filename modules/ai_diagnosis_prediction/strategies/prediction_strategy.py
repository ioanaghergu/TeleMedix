from abc import ABC, abstractmethod

class PredictionStrategy(ABC):
    @abstractmethod
    def load_model(self, model_path):
        pass

    @abstractmethod
    def generate_disease_name(self, symptom_description):
        pass
