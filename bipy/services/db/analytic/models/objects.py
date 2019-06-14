from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, Boolean, \
    ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy.orm import relationship


Base = declarative_base()


class AbstractProjectObject(AbstractConcreteBase, Base):
    """ Class to represent an abstract warehouse object
    """
    id = Column(Integer, Sequence('project_id_seq'),
                primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))
    created_by = Column(String(255))
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(String(255))
    modified_on = Column(DateTime)

    def __repr__(self):
        """
        Returns the string representation of this class
        """
        repr_str = ("Abstract Warehouse [Name = %s]") % (
            self.name)
        return repr_str


class Project(AbstractProjectObject):
    """Project class to contain its metadata
    """
    __tablename__ = 'project_metadata'

    path = Column(String(1000))
    is_active = Column(Boolean)
    keywords = Column(String(255))
    applications = relationship('Application', backref="project_metadata")


class PRJ_Application(AbstractProjectObject):
    """ Represents an datasource which points to an database and
        schema in warehouse
    """
    __tablename__ = 'project_applications'

    project_id = Column(Integer, ForeignKey("project_metadata.id"))
    datasets = relationship('DataSet', backref="project_applications")


class PRJ_DataSet(AbstractProjectObject):
    """Represents an table in the datasource
    """
    __tablename__ = 'project_datasets'

    application_id = Column(Integer, ForeignKey("project_applications.id"))
    tables = relationship('Table', backref="project_datasets")
    # consider this dataset as virtual table if it contains 2 or
    # more physical tables which will be joined in this dataset
    # else it shouldn't be virtual since 1 table is used is
    # accessible as-is (1 to 1, no special logic required)
    is_virtual = Column(Boolean, default=False)
    relation = relationship('Relation', backref="project_datasets")


class PRJ_Table(AbstractProjectObject):
    """ Represents a physical table in warehouse. Values are populated from
        Metadata repository
    """
    __tablename__ = 'project_tables'

    dataset_id = Column(Integer, ForeignKey("project_datasets.id"))
    meta_database_id = Column(Integer)
    meta_schema_id = Column(Integer)
    meta_table_id = Column(Integer)
    is_db_link_req = Column(Boolean)
    db_link_name = Column(String(255))
    columns = relationship('Column', backref="project_tables")
    relation = relationship('Relation', backref="project_tables")


class PRJ_Column(AbstractProjectObject):
    """ Represents an physical column in warehous. Metadata repo is
        used to fill in the details
    """
    __tablename__ = 'project_columns'

    table_id = Column(Integer, ForeignKey("project_tables.id"))
    meta_database_id = Column(Integer)
    meta_schema_id = Column(Integer)
    meta_table_id = Column(Integer)
    meta_column_id = Column(Integer)
    relation = relationship('Relation', backref="project_columns")


class PRJ_Relation(AbstractProjectObject):
    """ Defines a relation or join between 2 or more tables
    """
    dataset_id = Column(Integer, ForeignKey("project_datasets.id"))
    source_table_id = Column(Integer, ForeignKey("project_tables.id"))
    source_column_id = Column(Integer, ForeignKey("project_columns.id"))
    target_table_id = Column(Integer, ForeignKey("project_tables.id"))
    target_column_id = Column(Integer, ForeignKey("project_columns.id"))
    join_type = Column(String(255))
