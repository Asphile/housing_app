from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message  
from app import db, bcrypt, mail 
from app.models.user import User
from app.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm

auth = Blueprint('auth', __name__)

# --- Helper Function: Send Reset Email ---
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender=current_app.config.get('MAIL_USERNAME'),
                  recipients=[user.email])
    # _external=True is CRITICAL to generate a full URL (http://...) instead of a relative path (/...)
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)

# --- Route: Registration ---
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()

        # Welcome Email Notification
        try:
            msg = Message(
                subject='Welcome to the DUT Student Housing Portal',
                sender=current_app.config.get('MAIL_USERNAME'),
                recipients=[user.email]
            )
            msg.body = f"Hello {user.username},\n\nYour account has been successfully created!"
            mail.send(msg)
        except Exception as e:
            print(f"Welcome Email failed: {e}")

        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', title='Register', form=form)

# --- Route: Login ---
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.email == 'studenthousing@dut4life.ac.za':
            return redirect(url_for('main.admin_dashboard'))
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        # 1. Admin Override
        if form.email.data == 'studenthousing@dut4life.ac.za' and form.password.data == 'duthouse003':
            admin_user = User.query.filter_by(email=form.email.data).first()
            if not admin_user:
                hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                admin_user = User(username='System Admin', email=form.email.data, password_hash=hashed_pw)
                db.session.add(admin_user)
                db.session.commit()
            
            login_user(admin_user, remember=form.remember.data)
            flash('Admin access granted.', 'success')
            return redirect(url_for('main.admin_dashboard'))

        # 2. Student Login
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            
    return render_template('login.html', title='Login', form=form)

# --- Route: Request Password Reset (Email Entry) ---
@auth.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        except Exception as e:
            print(f"SMTP Error: {e}")
            flash('Could not send email. Please check your internet or MAIL_PASSWORD.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

# --- Route: Reset Password (New Password Entry) ---
@auth.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

# --- Route: Logout ---
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))