# run.py

from app import create_app, db

app = create_app()

# Enable Flask shell context for easy access to models and DB
@app.shell_context_processor
def make_shell_context():
    from app.models import User, Patient, Appointment
    return {
        "db": db,
        "User": User,
        "Patient": Patient,
        "Appointment": Appointment,
    }

if __name__ == "__main__":
    # Don't use debug=True in production
    app.run()
