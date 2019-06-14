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

    project_type = Column(String(255))
    items = relationship('ProjectItem',
                         backref='project_projects')
    folders = relationship('ProjectFolder', backref='project_projects')
    files = relationship('ProjectFile', backref='project_projects')


class ProjectItem(BaseProjectObject):
    """ An standard object which can be saves under an object
        Use this object of type of project item is not known
    """
    __tablename__ = 'project_items'

    project_id = Column(Integer, ForeignKey('project_projects.id'))
    item_type = Column(String(255))


class ProjectFolder(BaseProjectObject):
    """ Represents an folder in a project """
    __tablename__ = 'project_folders'

    project_id = Column(Integer, ForeignKey('project_projects.id'))
    folder_path = Column(String(1000))
    folder_icon = Column(String(1000))
    files = relationship('ProjectFile', backref='project_folders')
    folders = relationship('ProjectFolder')
    parent_folder_id = Column(Integer, ForeignKey('project_folders.id'))


class ProjectFile(BaseProjectObject):
    """ Represents an file under an project"""
    __tablename__ = 'project_files'

    project_id = Column(Integer, ForeignKey('project_projects.id'))
    file_type = Column(String(255))
    file_path = Column(String(1000))
    file_icon = Column(String(1000))
    folder_id = Column(Integer, ForeignKey('project_folders.id'))


