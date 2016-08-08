#!/usr/bin/env python
# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import Required, Length

class PostForm(Form):
    studentID = StringField(u'学号：', validators=[Required(), Length(0, 11)])
    password = PasswordField(u'密码：', validators=[Required()])
    submit = SubmitField(u'查询')

class SelectForm(Form):
    studentID = StringField(validators=[Required()])
    year = SelectField(u'学年', choices=[(u'0',u'全部'),(u'2012-2013',u'2012-2013'),(u'2013-2014',u'2013-2014'),(u'2014-2015',u'2014-2015'),(u'2015-2016',u'2015-2016'),(u'2016-2017',u'2016-2017')])
    term = SelectField(u'学期', choices=[(u'0',u'全部'),('1',u'1'),('2',u'2')])
    submit = SubmitField(u'查询')

