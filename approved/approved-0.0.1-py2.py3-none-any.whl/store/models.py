# -*- coding: utf-8 -*-
from datetime import datetime
import json

from alchy import ModelBase, make_declarative_base
from sqlalchemy import Column, types, orm, ForeignKey


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError('Type not serializable')


class JsonModel(ModelBase):

    def to_json(self, pretty=False):
        """Serialize to JSON.

        Handle DateTime objects.
        """
        kwargs = dict(indent=4, sort_keys=True) if pretty else dict()
        return json.dumps(self.to_dict(), default=json_serial, **kwargs)


Model = make_declarative_base(Base=JsonModel)


class Sample(Model):

    """Sample level QC metrics from an anlaysis."""

    id = Column(types.String(32), primary_key=True)
    analysis_id = Column(types.String(64), ForeignKey('analysis.id'))
    sequencing_type = Column(types.Enum('exomes', 'genomes'))
    sex_predicted = Column(types.Enum('male', 'female', 'unknown'))

    # mapping/alignment
    reads = Column(types.Integer)
    mapped_percent = Column(types.Float)
    duplicates_percent = Column(types.Float)
    strand_balance = Column(types.Float)

    # coverage
    capture_kit = Column(types.String(32))
    coverage_target = Column(types.Float)
    completeness_target_10 = Column(types.Float)
    completeness_target_20 = Column(types.Float)
    completeness_target_50 = Column(types.Float)
    completeness_target_100 = Column(types.Float)

    # variant calling
    variants = Column(types.Integer)  # WHERE?
    indels = Column(types.Integer)
    snps = Column(types.Integer)
    novel_sites = Column(types.Integer)  # WHERE?
    concordant_rate = Column(types.Float)
    hethom_ratio = Column(types.Float)
    titv_ratio = Column(types.Float)

    @property
    def read_pairs(self):
        return self.reads / 2


class Analysis(Model):

    """Meta-data class to group samples from the same analysis."""

    # composed from "{customer_id}-{name}"
    id = Column(types.String(64), primary_key=True)
    pipeline = Column(types.String(32))
    pipeline_version = Column(types.String(32))
    analyzed_at = Column(types.DateTime)
    _program_versions = Column(types.Text)

    @property
    def program_versions(self):
        return json.loads(self._program_versions) if self._program_versions else {}

    @program_versions.setter
    def program_versions(self, value):
        self._program_versions = json.dumps(value)

    samples = orm.relationship('Sample', cascade='all,delete',
                               backref='analysis')
