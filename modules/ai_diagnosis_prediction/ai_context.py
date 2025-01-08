from modules.ai_diagnosis_prediction.strategies.prediction_strategy import PredictionStrategy

class AIContext:
    def __init__(self, strategy: PredictionStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PredictionStrategy):
        self.strategy = strategy

    def load_model(self, model_path):
        self.strategy.load_model(model_path)

    def generate_disease_name(self, symptom_description):
        return self.strategy.generate_disease_name(symptom_description)
