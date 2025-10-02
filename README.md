# Health Appointment Booking System
A Django-based healthcare booking platform that allows patients to schedule, manage, and track appointments with doctors. Built with Django, Django REST Framework, PostgreSQL, Docker, and Adminer for easy database management.

## Features

- User authentication & role-based access (patients, doctors, admins)
- Appointment scheduling and management
- Patient profile and medical history tracking
- Admin dashboard for managing doctors, patients, and appointments
- Containerized setup with Docker & Docker Compose
- Easy DB inspection with Adminer
  
## project Structure
```
health_booking_system/
├── manage.py
├── requirements.txt
├── .env
├── health_booking_system/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/
├── appointments/
├── doctors/
├── patients/
├── medical_records/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── media/
└── templates/
    ├── base.html
    ├── accounts/
    ├── appointments/
    ├── doctors/
    └── patients/
```

## Tech Stack

- Backend: Django, Django REST Framework

- Database: PostgreSQL

- Containerization: Docker & Docker Compose

- Package Manager: uv

- DB Management: Adminer


##  Entity Relationship Diagram (EDR)

```mermaid

erDiagram
    %% User Management
    CustomUser {
        int id PK
        string username UK
        string email
        string password
        string first_name
        string last_name
        string user_type "patient|doctor|admin"
        string phone_number
        date date_of_birth
        boolean is_active
        boolean is_staff
        datetime created_at
        datetime updated_at
    }

    %% Patient Management
    Patient {
        int id PK
        int user_id FK
        string gender "M|F|O"
        string blood_group "A+|A-|B+|B-|AB+|AB-|O+|O-"
        string emergency_contact_name
        string emergency_contact_phone
        text address
        text medical_history
        text allergies
        text current_medications
        string insurance_provider
        string insurance_policy_number
        string profile_picture
        datetime created_at
        datetime updated_at
    }

    %% Doctor Management
    Specialization {
        int id PK
        string name UK
        text description
        datetime created_at
    }

    Doctor {
        int id PK
        int user_id FK
        int specialization_id FK
        string license_number UK
        int years_of_experience
        string qualification
        string hospital_affiliation
        decimal consultation_fee
        text biography
        string profile_picture
        string status "pending|approved|suspended|rejected"
        boolean is_available
        datetime created_at
        datetime updated_at
    }

    DoctorAvailability {
        int id PK
        int doctor_id FK
        string day_of_week "monday|tuesday|wednesday|thursday|friday|saturday|sunday"
        time start_time
        time end_time
        boolean is_available
        datetime created_at
    }

    %% Appointment Management
    Appointment {
        int id PK
        int patient_id FK
        int doctor_id FK
        date appointment_date
        time appointment_time
        string appointment_type "consultation|follow_up|emergency|routine_checkup"
        string status "scheduled|confirmed|completed|cancelled|no_show|rescheduled"
        text reason
        text notes
        text doctor_notes
        text prescription
        boolean follow_up_required
        date follow_up_date
        datetime created_at
        datetime updated_at
    }

    AppointmentHistory {
        int id PK
        int appointment_id FK
        int changed_by_id FK
        string old_status
        string new_status
        text change_reason
        datetime changed_at
    }

    %% Medical Records Management
    MedicalRecord {
        int id PK
        int patient_id FK
        int doctor_id FK
        int appointment_id FK
        string record_type "diagnosis|prescription|lab_result|imaging|surgery|vaccination"
        string title
        text description
        text diagnosis
        text treatment
        text medications
        string attachments
        datetime record_date
        datetime created_at
        datetime updated_at
    }

    Prescription {
        int id PK
        int medical_record_id FK
        string medication_name
        string dosage
        string frequency
        string duration
        text instructions
        datetime created_at
    }

    %% Relationships
    CustomUser ||--o| Patient : "has profile"
    CustomUser ||--o| Doctor : "has profile"
    Doctor }o--|| Specialization : "belongs to"
    Doctor ||--o{ DoctorAvailability : "has availability"
    Patient ||--o{ Appointment : "books"
    Doctor ||--o{ Appointment : "serves"
    Appointment ||--o{ AppointmentHistory : "has history"
    CustomUser ||--o{ AppointmentHistory : "changes"
    Patient ||--o{ MedicalRecord : "has records"
    Doctor ||--o{ MedicalRecord : "creates"
    Appointment ||--o| MedicalRecord : "generates"
    MedicalRecord ||--o{ Prescription : "contains"
```  
## Installation
### 1.Clone the repository
```
git clone https://github.com/aarongeb/health-booking-system.git
cd health-booking-system
```
### 2.Create and configure `.env`
```
POSTGRES_DB=health_system_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=test
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```
### 3.Build and start containers
```
docker-compose up --build
```
### 4.Run migrations
```
docker exec -it health_booking_system uv run python manage.py migrate
```
### 5.Create a superuser
```
docker exec -it health_booking_system uv run python manage.py createsuperuser
```

### Contributing
- Fork the repo
- Create your feature branch: git checkout -b feature/my-feature
- Commit changes: git commit -m "Add new feature"
- Push to branch: git push origin feature/my-feature
- Open a Pull Request
## License

This project is licensed under the MIT License. See the LICENSE
 file for details.