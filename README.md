# Telemedix 🏥💻

Acest repository conține implementarea unei **Platforme de Telemedicină** care îmbunătățește accesul la îngrijire medicală prin consultații online, recomandări bazate pe inteligență artificială și extragerea simptomelor din fișiere PDF.

**Documentație:** [Documentație](AMSS_Documentatie.pdf)

**Contribuția la proiect:** [Listă task-uri](https://unibucro0-my.sharepoint.com/:x:/r/personal/larisa-georgiana_balc_s_unibuc_ro/_layouts/15/Doc.aspx?sourcedoc=%7BCD4CECB7-5E91-423E-B6EB-DDAD785E8CC1%7D&file=TaskuriProiect.xlsx&action=default&mobileredirect=true)

## Funcționalități 🚀

- **Consultații Online** 🩺💬
- **Sugestii AI pentru Specializări Medicale** 🤖💡
- **Extragerea Simptomelor din PDF** 📄🔍
- **Gestionarea Programărilor** 📅📈

## Arhitectură și Design 🏗️

Sistemul utilizează **Patternul Strategy** pentru gestionarea componentei de inteligență artificială și **Patternul Singleton** pentru gestionarea conexiunii la baza de date, oferind o arhitectură modulară și ușor de întreținut.

### Diagrame 📊

1. **Workflow Diagram** - Diagrama Generala:
   ![Workflow Diagram](diagrams/Diagrama%20Workflow.jpg)

   Aceasta diagramă descrie fluxul unei platforme de consultații medicale online, împărțită în două categorii principale: **pacient** și **medic**.

   1. **Pacient:**
      - Se autentifică sau se înregistrează.
      - Poate programa consultații (selectare medic, confirmare dată și oră).
      - Participă la consultații video și primește diagnosticul.
      - AI analizează simptomele și oferă un diagnostic preliminar, completând dosarul medical.

   2. **Medic:**
      - Se autentifică și își gestionează profilul.
      - Intră în consultații video, vizualizează dosarul pacientului, oferă diagnosticul și actualizează dosarul medical.
      - Poate gestiona și edita programările, notificând pacienții despre modificări.

   3. **Sistem:**
      - Automatizează notificările și sincronizează calendarele utilizatorilor.
      - Folosește AI pentru a analiza datele și a îmbunătăți dosarele medicale.

   ---
   
2. **Notifications Sequence Diagram** - Melania Ion:
   ![Notifications Sequence Diagram](diagrams/Notifications%20Sequence%20Diagram.png)

   ## Diagrama de secvență pentru funcționalitatea - notificări
   ### Paricipanți
   - Utilizator (actor): Inițiază acțiuni în aplicație.
   - App UI: Interfața grafică ce preia acțiunile utilizatorului și comunică cu backend-ul.
   - Backend: Gestionează logica aplicației.
   - Database: Baza de date corespunzătoare aplicației.
   
   ### Notificările cu rolul de "reminder"
   - Se verifică dacă utilizatorul este logat (operatorul `alt` indică cele două cazuri: **logat** sau **nu**).
   - Dacă utilizatorul este logat:
   - Backend-ul caută consultații ce urmează sa aibă loc în următoarea oră.
   - Operatorul de interacțiune `opt` este utilizat pentru a reprezenta faptul că, dacă acestea există, backend-ul creează notificările cu detaliile aferente și le inserează în baza de date.
   - După acest pas, backend-ul calculează numărul notificărilor necitite (existente deja sau nou-create) și trimite această valoare către frontend pentru actualizarea clopoțelului.

   ### Creare consultație
   - Când un pacient creează o noua consultație cu succes (operatorul `alt` evidențiază cele două rezultate posibile: **validare reușită** sau **eșuată**), backend-ul creează o notificare pentru medic pentru a-l informa de acest aspect.

   ### Anulare consultație
   - Notificările sunt generate pentru celălalt utilizator în funcție de cine anulează: **pacient** sau **medic**.
   - Operatorul `alt` determină cele două ramuri pentru a determina ce tip de mesaj se creează ca notificare și cui îi este transmis.

   ### Centrul de notificări
   - La cererea utilizatorului, backend-ul returnează toate notificările (cele noi, precum si cele marcate deja ca "read"), începând cu cea mai recentă.

   ### Marcarea notificărilor ca "read"
   - Backend-ul actualizează notificarea (`isRead=true`). Trimite apoi frontend-ului numărul actualizat de notificări necitite pentru clopoțel și informarea utilizatorului.

   ### Ștergerea notificării
   - Se folosește operatorul `alt` pentru a verifica dacă notificarea este citită:
   - În caz afirmativ, este trimisă cererea pentru a fi ștearsă.
   - În caz contrar, se afișează un mesaj de eroare.

   ---

3. **Activity Diagram - Appointment Management** - Melania Ion:
   ![Activity Diagram - Appointment Management](diagrams/Activity%20Diagram%20Appointments%20Management.png)
   
   ## Diagrama de activitate pentru gestionarea consultațiilor
   ### Punctul de start
   - Se începe cu un `nod inițial`, când utilizatorul autentificat accesează secțiunea de management al consultațiilor.

   ### Extragerea și clasificarea consultațiilor
   - Consultațiile sunt preluate din baza de date, iar apoi statusul acestora este determinat pentru a fi clasificate ca:
   - Active,
   - Cancelled,
   - Attended.

   ### Afișarea listei inițiale
   - După clasificare, lista de consultații este afișată utilizatorului.

   ### Filtrare și sortare
   - Un `nod de fork` împarte fluxul în două activități:
   - Aplicarea unui filtru (în funcție de statusul consultațiilor),
   - Sortarea consultațiilor (în funcție de data consultațiilor: cele mai recente sau cele mai vechi).

   ### Reunirea fluxului
   - Un `nod de join` aduce activitățile anterioare într-un singur flux, iar lista de consultații dorite este afișată utilizatorului.

   ### Anularea sau ștergerea unei consultații
   - Utilizatorul decide ce face în continuare printr-un `nod de decizie` cu `gărzi` corespunzătoare:
   - Dacă alege să anuleze o consultație, se verifică dacă aceasta este activă și, dacă da, se finalizează procesul de anulare.
   - Dacă alege să șteargă o consultație, aceasta poate fi ștearsă doar dacă este anulată sau a avut loc deja.

   ### Finalizare
   - După aceste activități, noii pasi sunt determinați de un nou nod de decizie:
   - Fie utilizatorul se întoarce la activitatea de determinare a noilor statusuri ale consultațiilor și activitatea continuă,
   - Fie a terminat de gestionat consultațiile și avem un `nod final` care finalizează întreaga activitate.
   
   ---

4. **Database Diagram** - Balc Larisa:
   ![Database Diagram](diagrams/Diagrama%20baza%20de%20date.jpg)

   ## **Structura bazei de date**

   ### **Tabele și atribute**

   1. **User**  
      Gestionează informațiile utilizatorilor (pacienți, medici, admini).  
      - `userID`, `email`, `password`, `username`, `birth_date`, `role`.  

   2. **Patient**  
      Conține date despre pacienți.  
      - `patientID` (cheie primară și externă), `insurance_no`, `emergency_contact`.  

   3. **Medic**  
      Gestionează datele despre medici.  
      - `medicID` (cheie primară și externă), `specializationID` (cheie externă), `licence_no`.  

   4. **Specialization**  
      Definește specializările medicale.  
      - `specializationID`, `specialization_name`.  

   5. **Service**  
      Gestionează serviciile asociate cu specializările.  
      - `serviceID`, `specializationID` (cheie externă), `service_name`.  

   6. **Appointment**  
      Centralizează programările.  
      - `appointmentID`, `patientID`, `medicID`, `availabilityID`, `serviceID`, `notes`.  

   7. **Availability**  
      Gestionează intervalele orare ale medicilor.  
      - `availabilityID`, `medicID`, `date`, `start_time`, `end_time`, `availability_status`.  

   8. **MedicalRecord**  
      Stochează informații medicale.  
      - `recordID`, `medicID`, `patientID`, `symptoms`, `diagnosis`, `treatment`.  

   ### **Relații între tabele**
   1. **User** → **Patient**, **Medic**: Toți pacienții și medicii sunt utilizatori.  
   2. **Medic** → **Specialization**: Medicii au o specializare.  
   3. **Service** → **Specialization**: Serviciile sunt legate de specializări.  
   4. **Appointment** → **Patient**, **Medic**, **Service**, **Availability**: Detaliile unei programări.  
   5. **Availability** → **Medic**: Intervalele orare disponibile ale medicilor.  
   6. **MedicalRecord** → **Patient**, **Medic**: Fișe medicale asociate cu pacienți și medici.  

   ---

5. **Use Case Diagram** - Balc Larisa:
   ![Use Case Diagram](diagrams/Diagrama%20UML%20UseCase.jpg)

   ## **Actori principali**  
   1. **Pacient**: Utilizator al platformei pentru gestionarea sănătății.  
   2. **Medic**: Specialist care oferă consultații și gestionează programări.  
   3. **Sistem AI**: Componentă automată pentru analiză medicală și asistență.  

   ## **Funcționalități**  

   ### **Pentru Pacient**  
   - **Profil medici**: Căutare și vizualizare informații.  
   - **Sugestii AI**: Recomandări de medic bazate pe datele pacientului.  
   - **Documente medicale**: Încărcare PDF și extracție simptome.  
   - **Dosar medical**: Vizualizare și actualizare istoric.  
   - **Cont**: Autentificare, editare profil.  
   - **Consultații**:  
      - Programare, notificări status, anulare/reprogramare.  
      - Vizualizare consultații viitoare/anterioare.  

   ### **Pentru Medic**  
   - **Consultații**:  
      - Vizualizare viitoare/anterioare, notificări.  
   - **Program**: Stabilire orar disponibilitate.  
   - **Consultații online**: Organizare întâlniri virtuale.   

   ## **Relație cu AI**  
   - Sugestii personalizate și analiză automată a documentelor pentru recomandări și simplificarea consultațiilor.  

   ---

6. **Class Diagram** - Bianca Andrei:
   ![Class Diagram](diagrams/Diagrama%20clase.jpg)

   Diagrama de clase ilustrează structura unui sistem de gestionare a consultațiilor medicale, având clasa **User**, moștenită de **Doctor** și **Patient**. User definește atribute generale (de exemplu username, email) și metode comune (login(), edit_account()), în timp ce Doctor include funcții specifice precum set_availability(). Pacienții pot crea programări prin metoda add_consultation() și își pot gestiona fișele medicale. Clasa **Appointment** stochează detalii legate de consultații, precum data și intervalul, medicul și observațiile, iar doctorii sunt asociați cu specializările și disponibilitățile lor (Availability). Modelul evidențiază clar relațiile dintre utilizatori, programări și componentele esențiale ale sistemului.

   ---

7. **Consultation State Diagram** - Bianca Andrei:
   ![Consultation State Diagram](diagrams/Diagrama%20stari%20consultatie.jpg)

   Diagrama de stări descrie ciclul de viață al unei consultații medicale în cadrul unui sistem de gestionare a programărilor. Procesul începe în starea inițială **Idle**, unde utilizatorul poate iniția diverse acțiuni. Consultația poate trece prin mai multe stări:

      - **Creating appointment** - Pacientul completează câmpurile formularului, iar sistemul validează datele. Dacă programarea este validă, se trimite o notificare de creare; în caz contrar, pacientul solicitant va primi un mesaj de eroare.
      
      - **Editing** - Utilizatorul poate edita notele asociate consultației, actualizând informațiile.
      
      - **Cancelling appointment** - Programarea poate fi anulată, moment în care se trimite o notificare de anulare.
      
      - **Sending notification** - Starea de trimitere a notificărilor are loc pentru acțiuni precum crearea sau anularea consultației, dar și pentru a le reaminti utilizatorilor de programare cu o oră înainte de consultație.
      
      - **Deleting appointment** - O programare deja anulată sau marcată ca fiind finalizată poate fi ștearsă definitiv din sistem.

   ---

8. **Authentication Sequence Diagram** - Ioana Ghergu:
   ![Authentication Sequence Diagram](diagrams/Login%20and%20Sign%20up%20Sequence%20Diagram.png)

   ## Diagrama de secvență pentru procesul de autentificare în platformă
   ### Paricipanți
   - **Utilizator**: inițiază acțiuni în aplicație
   - **Sistem Log in**: gestionează logica de autentificare
   - **Sistem Sign up**: gestionează logica de înregistrare 
   - **App Dashboard**: interfața grafică a aplicației
   - **Database**: baza de date asociată platformei

   La accesarea platformei, utilizatorul este direcționat către pagina de autentificare, unde își va introduce credențialele de logare. Acestea sunt preluate și trimise către backend-ul funcționalității de autentificare. Baza de date va fi activată pentru a rula un query bazat pe adresa de email introdusă, apoi va răspunde sistemului de autentificare cu rezultatul găsit.

   ### Verificarea existenței utilizatorului în baza de date
      Operatorul `alt` ne permite să distingem două cazuri pe baza rezultatului trimis de către baza de date:
      - Utilizatorul este înregistrat, caz în care sistemul de autentificare va verifica validitatea parolei introduse pe baza hash-ului stocat în baza de date. Se vor distinge alte două cazuri:
         #### Verificarea corectitudinii parolei 
        - Parola este corectă, utilizatorul este autentificat și trimis către pagina de Home, utilizatorul primește ca răspuns mesajul de succes
         - Parola este greșită, caz în care utilizatorul este redirecționat către pagina de autentificare, care îi trimite ca răspuns la încercarea de conectare mesajul de eroare 

      - Utilizatorul nu este înregistrat, situație în care sistemul de autentificare face redirect către pagina de Log in, iar utilizatorului i se trimite ca răspuns mesajul corespunzător de eroare

   În urma primirii mesajului de eroare "User doesn't exist", utilizatorul poate accesa pagina de înregistrare. Sistemul de Sign up va trmite o cerere către utilizator prin afișarea formularului de înregistrare, iar utilizatorul va răspunde cu datele sale. Sistemul de înregistrare va face o cerere SQL către baza de date, iar aceasta se va activa pentru a trimite rezultatul cerut. 
   Utilizatorul va fi înregistrat în platformă pe baza situațiilor decizionale, distinse prin utilizarea operatorului `alt`.

   ### Verificarea validității credențialelor pentru înregistrare
      - Email existent în baza de date: utilizatorul este redirecționat către pagina de Sign up și primește ca răspuns pentru încercarea de a se înregistra mesajul de eroare corespunzător
      - Email valid, ceea ce înseamnă că utilizatorul se poate înregistra. Sistemul de înregistrare validează credențialele introduse, apoi analizează următoarele situații: detaliile sunt valide, detaliile sunt invalide.
      Atunci când detaliile sunt valide, sistemul de înregistrare generează un hash pentru parola introdusă pe baza funcției sha256, face o cerere către baza de date pentru inserare și redirecționează utilizatorul către pagina Home
      Atunci când credențialele sunt invalide, utilizatorul este redirecționat către pagina de Sign up și i se trimite mesajul de eroare.

   ---

9. **Deployment Diagram For Online Consultation** - Ioana Ghergu:
   ![Deployment Diagram For Online Consultation](diagrams/Deployment%20diagram%20video%20call.png)

   ## Diagrama de deployment pentru aplicația de videoconferință

   ### Noduri
   - **Client 1 Browser / Client 2 Browser**: în cadrul acestora rulează aplicația de apel video. Fiecare client are următoarele artefacte:
     - **Client Socket**: conexiune pentru comunicarea cu serverul de signaling
     - **Media Streams Fetching**: modul pentru accesarea fluxurilor media de la cameră și microfon
     - **WebRTC Connection**: gestionează conexiunea peer-to-peer pentru transferul direct al fluxurilor media
   
   - **Signaling Server**: server pentru comunicarea între clienți. Conține următoarele artefacte:
     - **Socket Endpoint**: gestionează conexiunile socket cu clienții.
     - **SDP Offer/Answer Handling**: mecanism de procesare a ofertelor și răspunsurilor SDP pentru configurarea conexiunii WebRTC
     - **ICE Candidates Exchange**: mecanism de partajare a candidaților ICE între clienți pentru stabilirea traseului optim al conexiunii
   
   - **STUN Server**: server utilizat pentru determinarea adreselor publice ale clienților și traversarea NAT-ului

   ### Fluxul: Comunicarea este bidirecțională
   - Client 1 inițiază un apel video. Browserul său accesează fluxurile media prin modulul **Media Streams Fetching**
   - Oferta SDP este trimisă către serveru-ul de signaling prin intermediul socket-ului asociat clientului 1
   - Serverul de semnalizare transferă oferta către Client 2, care trimite înapoi un răspuns SDP
   - Ambii clienți schimbă candidații ICE prin server pentru a configura conexiunea peer-to-peer
   - **STUN Server** este utilizat ca dependință pentru conexiunea WebRTC a ambilor clienți. Acesta este necesar pentru generarea de ICE candidates, care sunt de fapt posibile rute prin clienții pot comunica

   ---

11. **Package Diagram** - Andrei Horceag:
   ![Package Diagram](diagrams/Package%20Diagram.jpg)

   ## **Pachete Principale**
   ### 1. **AI Diagnosis Prediction**
   - Utilizează modele AI pentru predicții medicale.
   - Interacționează cu `Utils` și `Database Server`.
   ### 2. **Web**
   - Gestionarea logicii aplicației web:
   - **Views:** Interfața utilizatorului.
   - **Design:** Stiluri și șabloane.
   - **Routes:** Navigarea utilizatorilor.
   - Se conectează la `Utils` și `Database Server`.
   ### 3. **Utils**
   - Funcționalități suport:
   - **PDF Parsing:** Extragerea datelor din fișiere PDF.
   - **Torch:** Integrare AI.
   - **Exceptions:** Gestionarea erorilor.
   - **SocketIO:** Funcții în timp real.
   ### 4. **Database Server**
   - Gestionarea datelor:
   - **Database:** Structură de date și tabele.
   - **Authentication:** Autentificare utilizatori.
   - **Relations:** Relații între entități.
   - Conectat prin ODBC Driver 17.
   ### 5. **Tests**
   - Scripturi de testare unitară pentru validarea funcționalităților.
   
   ---

13. **Deployment Diagram** - Andrei Horceag:
   ![Deployment Diagram](diagrams/Deployment%20Diagram.jpg)
   
 # Prezentare Generală a Arhitecturii Sistemului

   ### 1. **Server Client**
   - **Descriere:** Serverul client servește ca punct de intrare pentru utilizatori pentru a accesa aplicația web.
   - **Funcționalitate Principală:** Găzduiește interfața aplicației web, permițând interacțiunea utilizatorilor cu sistemul.

   ### 2. **Load Balancer**
   - **Descriere:** Un Load Balancer este utilizat pentru a distribui uniform traficul între mai multe noduri ale aplicației.
   - **Scop:** Asigură o disponibilitate ridicată și previne supraîncărcarea unui singur nod.
   
   ### 3. **Nodurile de Aplicație**
   - **Descriere:** Nodurile (denumite `ApplicationServer1` până la `ApplicationServer4`) gestionează logica de business a aplicației. Aceste noduri funcționează independent pentru a asigura scalabilitatea și toleranța la erori.
   - **Module implementate în fiecare server de aplicație:**
   - **Sistem de Autentificare pe Bază de Roluri:** Gestionează autentificarea utilizatorilor și accesul pe baza rolurilor.
   - **Interfață Utilizator (UI):** Furnizează interfața grafică utilizatorilor.
   - **Integrare Videoconferință:** Permite consultații video în timp real.
   - **Diagnostice Generat de AI:** Utilizează inteligența artificială pentru a oferi diagnostice bazate pe datele introduse.
   - **Procesare Fișiere PDF Medicale:** Procesează documente medicale PDF pentru extragerea datelor structurate.
   
   ### 4. **Serverul de Bază de Date Azure**
   - **Descriere:** Bază de date centralizată găzduită pe Azure, servind drept depozit de date pentru întregul sistem.
   - **Scop:** Gestionează toate datele persistente, inclusiv:
   - Datele de autentificare și autorizare ale utilizatorilor.
   - Orarul consultațiilor și dosarele medicale.
   - Datele de diagnostic generate de modulul AI.
   
   ---

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
