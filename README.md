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

1. **Workflow Diagram** - Diagrama Generala:
   ![Workflow Diagram](diagrams/Diagrama%20Workflow.jpg)

2. **Activity Diagram - Appointment Management** - Melania Ion:
   ![Activity Diagram - Appointment Management](diagrams/Activity%20Diagram%20Appointments%20Management.png)

3. **Authentication Sequence Diagram** - Ioana Ghergu:
   ![Authentication Sequence Diagram](diagrams/Login%20and%20Sign%20up%20Sequence%20Diagram.png)

4. **Database Diagram** - Balc Larisa:
   ![Database Diagram](diagrams/Diagrama%20baza%20de%20date.jpg)

5. **Use Case Diagram** - Balc Larisa:
   ![Use Case Diagram](diagrams/Diagrama%20UML%20UseCase.jpg)

6. **Class Diagram** - Bianca Andrei:
   ![Class Diagram](diagrams/Diagrama%20clase.jpg)

7. **Consultation State Diagram** - Bianca Andrei:
   ![Consultation State Diagram](diagrams/Diagrama%20stari%20consultatii.jpg)

8. **Package Diagram** - Andrei Horceag:
   ![Package Diagram](diagrams/Package%20Diagram.jpg)

9. **Deployment Diagram** - Andrei Horceag:
   ![Deployment Diagram](diagrams/Deployment%20Diagram.jpg)

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

### 3. Instalează Dependențele pentru aplicația de consultări online 📦

Aceasta a fost realizată utilizând node.js(v20.13.1). Node poate fi descărcat și instalat de aici: https://nodejs.org/en/download/current.
După instalare, vom rula următoarele comenzi:

```bash
cd videoCall
npm install mkcert -g
mkcert create-ca
mkcert create-cert
npm init -y
Get-Content dependencies.txt | ForEach-Object { npm install --save $_ }
```
Pentru a rula aplicația vom folosi comanda:

```bash
node ./signalingServer.js
```
### 4. Configurarea Parametrilor AI 🤖

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
