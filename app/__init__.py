#!/usr/bin/env python
# coding=utf-8
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from config import config


bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)

    #在蓝本中附加路由和自定义错误页面
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
