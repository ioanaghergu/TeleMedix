from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from modules.ai_diagnosis_prediction.DiagnosisClassifier import DiagnosisClassifier
import PyPDF2
import spacy
import re
import csv

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

def get_suggested_doctors(diagnosis):
    diagnosis_to_specialization = {}

    try:
        with open('Doctor_Versus_Disease.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    diagnosis_to_specialization[row[0].strip()] = row[1].strip()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

    specialization = diagnosis_to_specialization.get(diagnosis)
    if not specialization:
        print(f"No specialization found for diagnosis: {diagnosis}")
        return []

    try:
        conn = current_app.db 
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT medicID, s.specializationID, u.username AS doctor_name, s.specialization_name AS specialization_name
            FROM Medic m
            INNER JOIN Specialization s ON m.specializationID = s.specializationID
            INNER JOIN [User] u ON m.medicID = u.userID
            WHERE s.specialization_name = ? 
        """, (specialization,))
        
        doctors = cursor.fetchall()
        
        if not doctors:
            print(f"No doctors found for specialization: {specialization}")
            return []

        doctor_list = [
            {"medicID":doctor[0], "specializationID": doctor[1], "name": doctor[2], "specialization": doctor[3]} for doctor in doctors
        ]
        
        return doctor_list

    except Exception as e:
        print(f"Error querying the database: {e}")
        return []

@diagnosis.route('/suggest-doctors', methods=['POST'])
@login_required
def suggest_doctors():
    diagnosis_name = request.form.get('diagnosis')
    print(diagnosis_name)
    if not diagnosis_name:
        flash("No diagnosis provided to suggest doctors.", category="error")
        return redirect(url_for('diagnosis.generate_diagnosis'))

    doctors = get_suggested_doctors(diagnosis_name)
    print(doctors)

    if not doctors:
        flash("No doctors found for the given diagnosis.", category="error")
    return render_template('diagnosis.html', doctors=doctors, diagnosis=diagnosis_name)
