from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    xh = StringField('学号', validators=[DataRequired()])
    pwd = PasswordField('密码', validators=[DataRequired()])
    auth = StringField('验证码', validators=[DataRequired()])
    xk_csrf = HiddenField()
    xk_cookies = HiddenField()
    submit = SubmitField('查询')


class ClassForm(FlaskForm):
    year_range = [("20{0:d}-20{1:d}".format(i, i+1), "20{0:d}-20{1:d}".format(i, i+1)) for i in range(15, 19)]
    term_range = [(i, i) for i in range(1, 4)]
    year = SelectField(
        "学年",
        choices=year_range
    )
    term = SelectField(
        "学期",
        choices=term_range
    )
    submit = SubmitField('查看课程表')
