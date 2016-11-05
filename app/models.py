#!/usr/bin/env python
# coding=utf-8
from . import db


class Score(db.Model):
    __tablename__ = 'scorepages'
    id = db.Column(db.BigInteger, primary_key=True)
    studentid = db.Column(db.Unicode(20))
    year = db.Column(db.Unicode(20))
    term = db.Column(db.Unicode(2))
    code = db.Column(db.Unicode(10))
    title = db.Column(db.Unicode(50))
    credit = db.Column(db.Float(7,2))
    #mid_score = db.Column(db.Integer)
    #end_score = db.Column(db.Integer)
    fin_score = db.Column(db.Integer)
    cour_attribute = db.Column(db.Unicode(50))
    cour_character = db.Column(db.Unicode(10))

    def __init__(self, id ,studentid, year, term, code, title, credit, fin_score, cour_attribute, cour_character):
        self.id = id
        self.studentid = studentid
        self.year = year
        self.term = term
        self.code = code
        self.title = title
        self.credit = credit
        #self.mid_score = mid_score
        #self.end_score = end_score
        self.fin_score = fin_score
        self.cour_attribute = cour_attribute
        self.cour_character = cour_character


