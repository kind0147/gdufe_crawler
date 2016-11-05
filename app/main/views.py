#!/usr/bin/env python
# coding=utf-8
from flask import render_template, session, redirect, url_for, flash

from . import main
from .forms import PostForm, SelectForm
from .. import db
from .. import spider
from ..models import Score
import time

@main.route('/', methods=['GET', 'POST'])
def index():
    postform = PostForm()
    selectform = SelectForm()
    if postform.validate_on_submit():
        score = spider.CJScrap(postform.studentID.data, postform.password.data)
        score_tank = Score.query.filter_by(studentid=postform.studentID.data).first()
        if score_tank is None:
            try:
                isok = score.getScore()
            except Exception, e:
                #flash('error')
                return redirect(url_for('.index'))
        else:
            score_tank = Score.query.filter_by(studentid=postform.studentID.data, year=u'2015-2016', term=u'2').all()
            gpa = 0.0
            score_sum = 0.0
            credit_sum = 0.0
            for tank in score_tank:
                score_sum = score_sum + (float(tank.fin_score) * float(tank.credit))
                credit_sum = float(credit_sum) + float(tank.credit)
            gpa = float("%0.2f"%((score_sum/credit_sum-50.0)/10.0))
            return render_template('scoretable.html', studentID=score_tank[0].studentid, score_tank=score_tank, gpa=gpa, form=selectform)
    
    
    if selectform.validate_on_submit():
        if selectform.year.data=='0' or selectform.term.data=='0':
            if selectform.year.data=='0' and selectform.term.data!='0':
                #
                score_tank = Score.query.filter_by(studentid=selectform.studentID.data, term=selectform.term.data).all()

            elif selectform.year.data!='0' and selectform.term.data=='0':
                #
                score_tank = Score.query.filter_by(studentid=selectform.studentID.data, year=selectform.year.data).all()

            else :
                #
                score_tank = Score.query.filter_by(studentid=selectform.studentID.data).all()

        else :
            score_tank = Score.query.filter_by(studentid=selectform.studentID.data, year=selectform.year.data, term=selectform.term.data).all()
        gpa = 0.0

        if score_tank:
            score_sum = 0.0
            credit_sum = 0.0
            for tank in score_tank:
                score_sum = score_sum + (float(tank.fin_score) * float(tank.credit))
                credit_sum = float(credit_sum) + float(tank.credit)
            gpa = float("%0.2f"%(((score_sum/credit_sum)-50.0)/10.0))

            return render_template('scoretable.html', studentID=score_tank[0].studentid, score_tank=score_tank, gpa=gpa, form=selectform)
        else :
            return render_template('emptytable.html', form=selectform)

    return render_template('index.html', form=postform)

