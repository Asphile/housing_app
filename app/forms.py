from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange, Regexp
from app.models.user import User

# 1. Account Registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=2, max=20)
    ])
    email = StringField('Institutional Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        # Local Database Check
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please log in instead.')

        # Domain Restriction Check
        allowed_domains = ['dut4life.ac.za', 'dut.ac.za']
        try:
            domain = email.data.split('@')[1].lower()
        except IndexError:
            raise ValidationError('Invalid email format.')

        if domain not in allowed_domains:
            raise ValidationError('Registration is restricted to @dut4life.ac.za or @dut.ac.za addresses.')

# 2. Login
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RequestResetForm(FlaskForm):
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm New Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# 3. Roommate Preferences
class PreferenceForm(FlaskForm):
    cleanliness_level = SelectField('Cleanliness Level', choices=[
        ('tidy', 'Very Tidy'), ('average', 'Average'), ('messy', 'Relaxed')
    ], validators=[DataRequired()])
    
    noise_tolerance = SelectField('Noise Tolerance', choices=[
        ('low', 'Quiet environment'), ('medium', 'Normal noise'), ('high', 'Loud/Social')
    ], validators=[DataRequired()])
    
    sleep_schedule = SelectField('Sleep Schedule', choices=[
        ('early', 'Early Bird'), ('night', 'Night Owl'), ('flexible', 'Flexible')
    ], validators=[DataRequired()])
    
    study_habits = SelectField('Study Habits', choices=[
        ('quiet', 'Prefer Quiet Study'), ('group', 'Prefer Group Study'), ('mixed', 'Flexible')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Update Preferences')

# 4. Residence Application (Student Side)
class ResidenceForm(FlaskForm):
    # Validated against official document lengths 
    student_number = StringField('Student Number', validators=[
        DataRequired(), 
        Length(min=8, max=8), 
        Regexp(r'^\d{8}$', message="Student number must be exactly 8 digits")
    ])
    student_id = StringField('Identity Number', validators=[
        DataRequired(), 
        Length(min=13, max=13), 
        Regexp(r'^\d{13}$', message="ID number must be exactly 13 digits")
    ])
    surname = StringField('Surname', validators=[DataRequired()])
    full_names = StringField('Full Names', validators=[DataRequired()])
    
    cell_number = StringField('Student Cell Number', validators=[
        DataRequired(), 
        Length(min=10, max=10), 
        Regexp(r'^0\d{9}$', message="Must be a valid 10-digit number starting with 0")
    ])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=16, max=99)])

    # Emergency Contact
    nok_name = StringField('Next of Kin Full Name', validators=[DataRequired()])
    nok_relationship = StringField('Relationship', validators=[DataRequired()])
    nok_cell = StringField('Next of Kin Cell Number', validators=[
        DataRequired(), 
        Length(min=10, max=10), 
        Regexp(r'^0\d{9}$', message="Must be a valid 10-digit number")
    ])

# Section 3: Location (The missing piece!)
    home_address = StringField('Home Address', validators=[DataRequired()])
    province = SelectField('Province', choices=[
        ('', '--- Select Province ---'),
        ('EC', 'Eastern Cape'), ('FS', 'Free State'), ('GP', 'Gauteng'),
        ('KZN', 'KwaZulu-Natal'), ('LP', 'Limpopo'), ('MP', 'Mpumalanga'),
        ('NW', 'North West'), ('NC', 'Northern Cape'), ('WC', 'Western Cape')
    ], validators=[DataRequired()])

    campus = RadioField('Preferred Campus', choices=[
        ('Steve Biko', 'Steve Biko'),
        ('ML Sultan', 'ML Sultan'),
        ('Ritson', 'Ritson'),
        ('Indumiso', 'Indumiso'),
        ('Riverside', 'Riverside'),
        ('Brickfield', 'Brickfield'),
        ('City Campus', 'City Campus')
    ], validators=[DataRequired()])

    faculty = SelectField('Faculty', choices=[
        ('', 'Select Faculty...'),
        ('accounting', 'Accounting and Informatics'),
        ('applied', 'Applied Sciences'),
        ('arts', 'Arts and Design'),
        ('engineering', 'Engineering and the Built Environment'),
        ('health', 'Health Sciences'),
        ('management', 'Management Sciences')
    ], validators=[DataRequired()])
    
    qualification = StringField('Qualification', validators=[DataRequired()])
    level_of_study = SelectField('Level of Study', choices=[
        ('1st', 'First Year'), ('2nd', 'Second Year'), ('3rd', 'Third Year'), 
        ('4th', 'Fourth Year'), ('PG', 'Postgraduate')
    ], validators=[DataRequired()])

    profile_picture = FileField('Upload Identification Photo', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Image formats only (JPG, PNG)!')
    ])

    submit = SubmitField('Submit Application')

# 5. Admin Housing Management
class HousingForm(FlaskForm):
    name = StringField('Residence Name', validators=[DataRequired()])
    region = SelectField('Primary Campus', choices=[
        ('Steve Biko', 'Steve Biko'), ('ML Sultan', 'ML Sultan'), ('Ritson', 'Ritson'),
        ('Indumiso', 'Indumiso'), ('Riverside', 'Riverside'), ('City Campus', 'City Campus')
    ], validators=[DataRequired()])

    # RE-NAMED TO 'gender' to fix the UndefinedError crash
    gender = SelectField('Gender Configuration', choices=[
        ('Mixed', 'Mixed Residence'), 
        ('Male Only', 'Male Only'), 
        ('Female Only', 'Female Only')
    ], validators=[DataRequired()])
    
    address = StringField('Physical Address', validators=[DataRequired()])
    capacity = IntegerField('Total Bed Capacity', validators=[DataRequired()])
    description = TextAreaField('Facilities & Amenities')
    image = FileField('Residence Display Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Save Residence Details')