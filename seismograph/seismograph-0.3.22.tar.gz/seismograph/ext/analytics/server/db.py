# -*- coding: utf-8 -*-

import sqlalchemy
from datetime import datetime

from ...alchemy.orm import BaseModel


class BuildModel(BaseModel):

    __tablename__ = 'build'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text(), nullable=False, default='')


class CaseModel(BaseModel):

    __tablename__ = 'case'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text(), nullable=False, default='')


class BuildResultModel(BaseModel):

    __tablename__ = 'build_result'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    build_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('build.id'), nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False, default=datetime.now)
    was_success = sqlalchemy.Column(sqlalchemy.Boolean(), nullable=False)


class CaseResultModel(BaseModel):

    __tablename__ = 'case_result'

    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    case_id = sqlalchemy.Column(sqlalchemy.String(), sqlalchemy.ForeignKey('case.id'), nullable=False)
    build_result_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('build_result.id'), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DateTime(), nullable=False, default=datetime.now)
    reason = sqlalchemy.Column(sqlalchemy.Text(), nullable=False, default='')
    status = sqlalchemy.Column(sqlalchemy.Enum('passed', 'skipped', 'failed', 'error'), nullable=False)
