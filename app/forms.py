from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    SelectField,
    DateField,
    IntegerField,
    FloatField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Regexp, Optional
from app.models import User, Vehicle


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(),
            Regexp(r"^\d{10}$", message="Invalid phone number. Must be 10 digits."),
        ],
    )  # Add validators to ensure 10 digit number
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken. Please choose a different one.")

    def validate_phone(self, phone):
        user = User.query.filter_by(
            phone=f"+91{phone.data}"
        ).first()  # check to avoid duplicates
        if user:
            raise ValidationError("This phone number is already registered.")

    def validate_on_submit(self):
        rv = super(RegistrationForm, self).validate_on_submit()
        if rv:
            # Prepend +91 to phone numbers
            self.phone.data = f"+91{self.phone.data}"
        return rv


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password")
    submit = SubmitField("Login")
    request_otp = SubmitField("Request OTP")


class OTPForm(FlaskForm):
    otp = IntegerField("OTP", validators=[DataRequired()])
    submit = SubmitField("Verify OTP")


class PasswordRecoveryForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Send Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")


class VehicleForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    vehicle_number = StringField("Vehicle Number", validators=[DataRequired()])
    submit = SubmitField("Add Vehicle")

    def validate_vehicle_number(self, vehicle_number):
        vehicle = Vehicle.query.filter_by(vehicle_number=vehicle_number.data).first()
        if vehicle:
            raise ValidationError(
                "This vehicle number is already registered. Please choose a different one."
            )


class DocumentForm(FlaskForm):
    document_type = SelectField(
        "Document Type",
        choices=[
            ("Insurance", "Insurance"),
            ("Emission Certificate", "Emission Certificate"),
            ("Registration Certificate", "Registration Certificate"),
            ("Permit", "Permit"),
            ("Vehicle Registration", "Vehicle Registration"),
            ("Annual Inspection", "Annual Inspection"),
            ("Road Tax Receipt", "Road Tax Receipt"),
        ],
        validators=[DataRequired()],
    )
    serial_number = StringField("Serial Number", validators=[Optional()])
    start_date = DateField("Start Date", format="%Y-%m-%d", validators=[Optional()])
    end_date = DateField("End Date", format="%Y-%m-%d", validators=[Optional()])
    insurance_policy_number = StringField("Policy Number", validators=[Optional()])
    insurance_company_name = StringField("Insurance Company Name", validators=[Optional()])
    policy_coverage_amount = FloatField("Policy Coverage Amount", validators=[Optional()])
    policy_start_date = DateField("Policy Start Date", format="%Y-%m-%d", validators=[Optional()])
    policy_expiry_date = DateField("Policy Expiry Date", format="%Y-%m-%d", validators=[Optional()])
    submit = SubmitField("Add Document")
    
    def update_fields(self, document_type):
        if document_type == 'Insurance':
            self.serial_number.validators = [Optional()]
            self.start_date.validators = [Optional()]
            self.end_date.validators = [Optional()]
            self.insurance_policy_number.validators = [DataRequired(), Regexp(r'^\d{16}$', message="Policy number must be 16 digits.")]
            self.insurance_company_name.validators = [DataRequired()]
            self.policy_coverage_amount.validators = [DataRequired()]
            self.policy_start_date.validators = [DataRequired()]
            self.policy_expiry_date.validators = [DataRequired()]
        else:
            self.serial_number.validators = [DataRequired()]
            self.start_date.validators = [DataRequired()]
            self.end_date.validators = [DataRequired()]
            self.insurance_policy_number.validators = [Optional()]
            self.insurance_company_name.validators = [Optional()]
            self.policy_coverage_amount.validators = [Optional()]
            self.policy_start_date.validators = [Optional()]
            self.policy_expiry_date.validators = [Optional()]


class RenewalForm(FlaskForm):
    start_date = DateField(
        "New Start Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    end_date = DateField("New End Date", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("Renew Document")


class OTPForm(FlaskForm):
    otp = IntegerField("OTP", validators=[DataRequired()])
    submit = SubmitField("Verify OTP")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
