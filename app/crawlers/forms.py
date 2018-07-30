from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    name = StringField('姓名：', validators=[DataRequired()])
    xh = StringField('学号：', validators=[DataRequired()])
    pwd = PasswordField('密码：', validators=[DataRequired()])
    auth = StringField('验证码：', validators=[DataRequired()])
    xk_csrf = HiddenField()
    xk_cookies = HiddenField()
    submit = SubmitField('查询')