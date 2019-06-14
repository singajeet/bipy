"""
    Project management related model objects to hold information of
    all project items
    Author: Ajeet Singh
    Date: 6/14/2019
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Sequence, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy.orm import relationship
from bipy.logging import logger


Base = declarative_base()
LOGGER = logger.get_logger(__name__)


class BaseProjectObject(AbstractConcreteBase, Base):
    """ Base class containing common attributes"""

    id = Column(Integer, Sequence('project_seq_id'), primary_key=True)
    name = Column(String(255))
    deascription = Column(String(255))
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime)
    created_by = Column(String(255))
    modified_by = Column(String(255))


class Project(BaseProjectObject):
    """ An class representing a project"""
    __tablename__ = 'project_projects'

    analysis_project_id = Column(Integer)
    project_type = Column(String(255))
    items = relationship('ProjectItem',
                         backref='project_projects')
    folders = relationship('ProjectFolder', backref='project_projects')
    files = relationship('ProjectFile', backref='project_projects')
    properties = relationship('Property', backref='project_projects')


class ProjectItem(BaseProjectObject):
    """ An standard object which can be saves under an object
        Use this object of type of project item is not known
    """
    __tablename__ = 'project_items'

    project_id = Column(Integer, ForeignKey('project_projects.id'))
    item_type = Column(String(255))
    properties = relationship('Property', backref='project_items')


class ProjectFolder(BaseProjectObject):
    """ Represents an folder in a project """
    __tablename__ = 'project_folders'

    project_id = Column(Integer, ForeignKey('project_projects.id'))
    folder_path = Column(String(1000))
    folder_icon = Column(String(1000))
    files = relationship('ProjectFile', backref='project_folders')
    folders = relationship('ProjectFolder')
    parent_folder_id = Column(Integer, ForeignKey('project_folders.id'))
    datasets = relationship('ProjectDataSet', backref='project_folders')
    properties = relationship('Property', backref='project_folders')
    facts = relationship('ProjectFact', backref='project_folders')
    dimensions = relationship('ProjectDimension', backref='project_folders')
    metrices = relationship('ProjectMetric', backref='project_folders')


class ProjectFile(BaseProjectObject):
    """ Represents an file under an project"""
    __tablename__ = 'project_files'

    project_id = Column(Integer, ForeignKey('project_projects.id'))
    file_type = Column(String(255))
    file_path = Column(String(1000))
    file_icon = Column(String(1000))
    folder_id = Column(Integer, ForeignKey('project_folders.id'))
    properties = relationship('Property', backref='project_files')


class ProjectDataSet(BaseProjectObject):
    """ Represents an dataset in the project """
    __tablename__ = 'project_datasets'

    folder_id = Column(Integer, ForeignKey("project_folders.id"))
    analysis_dataset_id = Column(Integer)
    properties = relationship('Property', backref='project_datasets')
    facts = relationship('ProjectFact', backref='project_datasets')
    dimensions = relationship('ProjectDimension', backref='project_datasets')
    metrices = relationship('ProjectMetric', backref='project_datasets')


class ProjectFact(BaseProjectObject):
    """ Represents an Fact in the project hierrarchy
    """
    __tablename__ = 'project_facts'

    folder_id = Column(Integer, ForeignKey('project_folders.id'))
    dataset_id = Column(Integer, ForeignKey('project_datasets.id'))
    analysis_fact_id = Column(Integer)
    properties = relationship('Property', backref='project_facts')


class ProjectDimension(BaseProjectObject):
    """ Represents an dimension in the project hierrarchy
    """
    __tablename__ = 'project_dimensions'

    folder_id = Column(Integer, ForeignKey('project_folders.id'))
    dataset_id = Column(Integer, ForeignKey('project_datasets.id'))
    analysis_dimension_id = Column(Integer)
    properties = relationship('Property', backref='project_dimensions')


class ProjectMetric(BaseProjectObject):
    """ Represents an metric in the project hierrarchy
    """
    __tablename__ = 'project_metrices'

    folder_id = Column(Integer, ForeignKey('project_folders.id'))
    dataset_id = Column(Integer, ForeignKey('project_datasets.id'))
    analysis_metric_id = Column(Integer)
    properties = relationship('Property', backref='project_metrices')


class Property(BaseProjectObject):
    """ An property class for project & items
    """
    __tablename__ = 'properties'

    value = Column(String(1000))
    project_id = Column(Integer, ForeignKey('project_projects.id'))
    item_id = Column(Integer, ForeignKey('project_items.id'))
    file_id = Column(Integer, ForeignKey('project_files.id'))
    folder_id = Column(Integer, ForeignKey('project_folders.id'))
    dataset_id = Column(Integer, ForeignKey('project_datasets.id'))
    fact_id = Column(Integer, ForeignKey('project_facts.id'))
    dimension_id = Column(Integer, ForeignKey('project_dimensions.id'))
    metric_id = Column(Integer, ForeignKey('project_metrices.id'))
