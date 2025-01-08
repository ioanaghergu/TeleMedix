# Telemedix 🏥💻

Acest repository conține implementarea unei **Platforme de Telemedicină** care îmbunătățește accesul la îngrijire medicală prin consultații online, recomandări bazate pe inteligență artificială și extragerea simptomelor din fișiere PDF.

## Funcționalități 🚀

- **Consultații Online**: Permite pacienților să programeze consultații online cu medici specializați prin video sau chat. 🩺💬
- **Sugestii AI pentru Specializări Medicale**: Utilizarea unui algoritm AI pentru a analiza simptomele și a sugera specializările medicale relevante. 🤖💡
- **Extragerea Simptomelor din PDF**: Încărcarea fișierelor PDF pentru extragerea automată a simptomelor în rapoartele medicale. 📄🔍
- **Gestionarea Programărilor**: Permite pacienților și medicilor să gestioneze programările și istoricul consultațiilor. 📅📈

## Arhitectură și Design 🏗️

Sistemul utilizează **Patternul Strategy** pentru gestionarea componentei de inteligență artificială și **Patternul Model-View-Controller (MVC)** pentru o arhitectură modulară și ușor de întreținut.

### Diagrame 📊

1. **Activity Diagram - Appointment Management**:
   ![Activity Diagram - Appointment Management](diagrams/Activity%20Diagram%20Appointments%20Management.png)

2. **Authentication Sequence Diagram**:
   ![Authentication Sequence Diagram](diagrams/Authentication%20Sequence%20Diagram.png)

3. **Deployment Diagram**:
   ![Deployment Diagram](diagrams/Deployment%20Diagram.pdf)

4. **Database Diagram**:
   ![Database Diagram](diagrams/Diagrama%20baza%20de%20date.jpg)

5. **Class Diagram**:
   ![Class Diagram](diagrams/Diagrama%20clase%20(temporara).jpg)

6. **Consultation State Diagram**:
   ![Consultation State Diagram](diagrams/Diagrama%20stari%20consultatie%20(temporara).jpg)

7. **Workflow Diagram**:
   ![Workflow Diagram](diagrams/Diagrama%20Workflow.jpg)

8. **Package Diagram**:
   ![Package Diagram](diagrams/Package%20Diagram.pdf)

Here is the **README.md** content as requested:

## Installation 🛠️

Follow the steps below to set up the **Telemedix** on your local machine:

### 1. Clone the **repository** 📥

Clone the repository to your local machine:

```bash
git clone https://github.com/ioanaghergu/TeleMedix.git
```

### 2. Install Dependencies 📦

Navigate to the project folder and install all required dependencies:

```bash
cd TeleMedix
pip install -r requirements.txt
```

### 3. AI Training Parameters Setup 🤖

This platform uses machine learning models for AI-based predictions. The model's training parameters are packaged into compressed files for easy management.

#### To unzip the AI training parameters:

Run the following PowerShell script to unzip the training parameters:

```powershell
.\setup_pull.ps1
```

#### To zip the AI training parameters:

If you need to compress the training parameters for upload or storage, use the following PowerShell script:

```powershell
.\setup_push.ps1
```

---

Once these steps are completed, your environment will be ready to use the **Telemedix** 🚀
```