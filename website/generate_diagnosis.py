from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from modules.ai_diagnosis_prediction.DiagnosisClassifier import DiagnosisClassifier

diagnosis = Blueprint('diagnosis', __name__)

model = DiagnosisClassifier()

def generate_diagnosis_from_symptoms(symptoms):
    model.load_model("modules/ai_diagnosis_prediction/trained_model")
    predicted_disease = model.generate_disease_name(symptoms)
    return predicted_disease

@diagnosis.route('/diagnosis', methods=['GET', 'POST'])
@login_required
def generate_diagnosis():
    diagnosis_result = None

    if request.method == 'POST':
        symptoms = request.form.get('symptoms')

        if symptoms: 
            diagnosis_result = generate_diagnosis_from_symptoms(symptoms)

            if not diagnosis_result: 
                flash("No diagnosis found. Please check the symptoms input.", category="error")
        else:
            flash("Please enter symptoms to generate diagnosis.", category="error")
    
    return render_template('diagnosis.html', diagnosis=diagnosis_result)