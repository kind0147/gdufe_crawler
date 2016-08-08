#!/usr/bin/env python
# coding=utf-8
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:516211@127.0.0.1/student'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:516211@127.0.0.1/student'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:516211@127.0.0.1/student'

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        
        'default': DevelopmentConfig
        }


