from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange

class ReviewForm(FlaskForm):
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Review')