from modules.ai_diagnosis_prediction.strategies.prediction_strategy import PredictionStrategy
from modules.ai_diagnosis_prediction.models.diagnosis_classifier import DiagnosisClassifier

class DiagnosisClassifierStrategy(PredictionStrategy):
    def __init__(self):
        self.model = DiagnosisClassifier()

    def load_model(self, model_path):
        self.model.load_model(model_path)

    def generate_disease_name(self, symptom_description):
        return self.model.generate_disease_name(symptom_description)
