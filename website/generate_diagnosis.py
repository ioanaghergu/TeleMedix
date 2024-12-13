from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from modules.ai_diagnosis_prediction.DiagnosisClassifier import DiagnosisClassifier
import PyPDF2
import spacy
import re

diagnosis = Blueprint('diagnosis', __name__)

model = DiagnosisClassifier()
nlp = spacy.load("en_core_web_sm")

def generate_diagnosis_from_symptoms(symptoms):
    model.load_model("modules/ai_diagnosis_prediction/trained_model")
    predicted_disease = model.generate_disease_name(symptoms)
    return predicted_disease

def extract_symptoms_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)
        
        symptoms_section = re.search(r"SYMPTOMS\s*([\s\S]+?)(?=\n\s*[A-Za-z]|\n\s*$)", text, re.IGNORECASE)
        
        if symptoms_section:
            symptoms = symptoms_section.group(1).strip().split("\n")
            symptoms = [symptom.strip('- ').strip() for symptom in symptoms if symptom.strip()]
            return symptoms
        else:
            return []
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []

@diagnosis.route('/diagnosis', methods=['GET', 'POST'])
@login_required
def generate_diagnosis():
    diagnosis_result = None
    extracted_symptoms = None

    manual_symptoms = request.form.get('symptoms')
    pdf_file = request.files.get('pdf')

    if manual_symptoms and pdf_file:
        flash("Please provide symptoms either manually or via PDF, not both.", category="error")
    elif manual_symptoms:
        diagnosis_result = generate_diagnosis_from_symptoms(manual_symptoms)

        if not diagnosis_result: 
            flash("No diagnosis found. Please check the symptoms input.", category="error")
        else:
            flash("Diagnosis generated successfully.", category="success")
    elif pdf_file:
        extracted_symptoms = extract_symptoms_from_pdf(pdf_file)
        if extracted_symptoms:
            combined_symptoms = ", ".join(extracted_symptoms)
            diagnosis_result = generate_diagnosis_from_symptoms(combined_symptoms)
            if diagnosis_result:
                flash("Diagnosis generated successfully.", category="success")
            else:
                flash("No diagnosis found. Please refine the symptoms extracted from the PDF.", category="error")
        else:
            flash("No symptoms could be extracted from the uploaded PDF.", category="error")

    return render_template('diagnosis.html', diagnosis=diagnosis_result, symptoms=extracted_symptoms)