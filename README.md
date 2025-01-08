# Telemedix 🏥💻

Acest repository conține implementarea unei **Platforme de Telemedicină** care îmbunătățește accesul la îngrijire medicală prin consultații online, recomandări bazate pe inteligență artificială și extragerea simptomelor din fișiere PDF.

## Funcționalități 🚀

- **Consultații Online** 🩺💬
- **Sugestii AI pentru Specializări Medicale** 🤖💡
- **Extragerea Simptomelor din PDF** 📄🔍
- **Gestionarea Programărilor** 📅📈

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

## Instalare 🛠️

### 1. Clonează **repository-ul** 📥

```bash
git clone https://github.com/ioanaghergu/TeleMedix.git
```

### 2. Instalează Dependențele 📦

```bash
cd TeleMedix
pip install -r requirements.txt
```

### 3. Configurarea Parametrilor AI 🤖

#### Unzip:

```powershell
.\setup_pull.ps1
```

#### Zip:

```powershell
.\setup_push.ps1
```

---

După acești pași, platforma este gata de utilizare! 🚀
```