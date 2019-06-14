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
    __tablename__ = 'project_project'

    project_type = Column(String(255))
    items = relationship('ProjectItem',
                         backref='project_project',
                         enable_typechecks=False)


class ProjectItem(BaseProjectObject):
    """ An standard object which can be saves under an object
        Use this object of type of project item is not known
    """
    __tablename__ = 'project_item'

    project_id = Column(Integer, ForeignKey('project_project.id'))
    item_type = Column(String(255))
    items = relationship('ProjectItem', enable_typechecks=False)
    parent_id = Column(Integer, ForeignKey('project_item.id'))


class ProjectFile(ProjectItem):
    """ Represents an file under an project"""

    # item_type = Column(String(255), default='FILE')
    file_type = Column(String(255))
    file_path = Column(String(1000))
    file_icon = Column(String(1000))
