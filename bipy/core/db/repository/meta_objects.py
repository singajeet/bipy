"""
 Contains metamodels of various db objects that will be stored in repository and will be used by
 OLAP engine
 Author: Ajeet Singh
 Date: 5/13/2019
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Sequence, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy.orm import relationship
from bipy.core.db.repository.types import DataTypes, ViewTypes



Base = declarative_base()


class AbstractWarehouseObject(AbstractConcreteBase, Base):
    """ Class to represent an abstract warehouse object
    """

    id = Column(Integer, Sequence('repo_warehouse_id_seq'), primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))
    created_by = Column(String(255))
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(String(255))
    modified_on = Column(DateTime)

    """def __repr__(self):
        Returns the string representation of this class
        repr_str = ("Abstract Warehouse [Name = %s]") % (
            self.name)
        return repr_str
    """

class WarehouseDatabase(AbstractWarehouseObject):
    """ Represents an warehouse database
    """
    __tablename__ = 'repository_warehouse_databases'

    db_type = Column(String(255))
    connection_string = Column(String(255))
    username = Column(String(255))
    password = Column(String(255))
    schemas = relationship("WarehouseSchema", backref="repository_warehouse_databases")

    def __repr__(self):
        """String representation
        """
        return ("Warehouse [Name=%s, Type=%s]") % (self.name, self.db_type)

class WarehouseSchema(AbstractWarehouseObject):
    """ Represents an warehouse schema available in target database"
    """
    __tablename__ = 'repository_warehouse_schemas'

    can_use_as_prefix = Column(Boolean, default=True)
    is_temp_schema = Column(Boolean, default=False)
    tables = relationship("WarehouseTable", backref="repository_warehouse_schemas")
    views = relationship("WarehouseView", backref="repository_warehouse_schemas")
    mviews = relationship("WarehouseMaterializedView", backref="repository_warehouse_schemas")
    procedures = relationship("WarehouseProcedure", backref="repository_warehouse_schemas")
    functions = relationship("WarehouseFunction", backref="repository_warehouse_schemas")
    packages = relationship("WarehousePackage", backref="repository_warehouse_schemas")
    database_id = Column(Integer, ForeignKey("repository_warehouse_databases.id"))

    def __repr__(self):
        """String representation
        """
        return ("Warehouse Schema [Name=%s]") % (self.name)

class WarehouseTable(AbstractWarehouseObject):
    """Represents an table in the target warehouse database
    """
    __tablename__ = 'repository_warehouse_tables'

    number_of_columns = Column(Integer, default=0)
    number_of_rows = Column(Integer, default=0)
    contains_numeric_column = Column(Boolean, default=True)
    columns = relationship("WarehouseColumn", backref="repository_warehouse_tables")
    schema_id = Column(Integer, ForeignKey("repository_warehouse_schemas.id"))

    def __repr__(self):
        """String representation
        """
        return "Warehouse Table [Name=%s, SchemaId=%d]" % (self.name,
                                                           self.schema_id
                                                           if self.schema_id != None
                                                           else -1)

class WarehouseView(AbstractWarehouseObject):
    """Represents an view in the target warehouse database
    """
    __tablename__ = 'repository_warehouse_views'

    number_of_columns = Column(Integer, default=0)
    number_of_rows = Column(Integer, default=0)
    contains_numeric_column = Column(Boolean, default=True)
    columns = relationship("WarehouseColumn", backref="repository_warehouse_views")
    sql = Column(String(4000))
    schema_id = Column(Integer, ForeignKey("repository_warehouse_schemas.id"))

    def __repr__(self):
        """String representation
        """
        return "Warehouse View [Name=%s, SchemaId=%d]" % (self.name
                                                          , self.schema_id
                                                          if self.schema_id != None
                                                          else -1)

class WarehouseMaterializedView(AbstractWarehouseObject):
    """Represents an materialized view in the target database
    """
    __tablename__ = 'repository_warehouse_mviews'

    number_of_columns = Column(Integer, default=0)
    number_of_rows = Column(Integer, default=0)
    contains_numeric_column = Column(Boolean, default=True)
    columns = relationship("WarehouseColumn", backref="repository_warehouse_mviews")
    sql = Column(String(4000))
    is_stale = Column(Boolean, default=False)
    last_refreshed_at = Column(DateTime)
    schema_id = Column(Integer, ForeignKey("repository_warehouse_schemas.id"))

    def __repr__(self):
        """String representation
        """
        return "Warehouse Materialized View [Name=%s, SchemaId=%d]" % (self.name,
                                                                       self.schema_id
                                                                       if self.schema_id != None
                                                                       else -1)


class WarehouseColumn(AbstractWarehouseObject):
    """Represents an column of a table in the target warehouse database
    """
    __tablename__ = 'repository_warehouse_columns'

    column_type = Column(Integer, default=DataTypes.STRING.value)
    scale = Column(String(255))
    is_primary_key = Column(Boolean, default=False)
    is_foreign_key = Column(Boolean, default=False)
    is_fact_candidate = Column(Boolean, default=False)
    is_dim_candidate = Column(Boolean, default=False)
    belongs_to_view = Column(Boolean, default=False)
    view_type = Column(Integer, default=ViewTypes.VIEW.value)
    table_id = Column(Integer, ForeignKey("repository_warehouse_tables.id"))
    view_id = Column(Integer, ForeignKey("repository_warehouse_views.id"))
    mview_id = Column(Integer, ForeignKey("repository_warehouse_mviews.id"))

    def __repr__(self):
        """String representation
        """
        return ("Warehouse Column [Name=%s, TypeId=%d, TableId=%d, ViewId=%d, MViewId=%d]") % (
            self.name, self.column_type, self.table_id if self.table_id != None else -1
            , self.view_id if self.view_id != None else -1
            , self.mview_id if self.mview_id != None else -1)


class WarehousePackage(AbstractWarehouseObject):
    """Represents an SQL package in the target warehouse
    """
    __tablename__ = 'repository_warehouse_packages'

    number_of_procedures = Column(Integer, default=0)
    number_of_functions = Column(Integer, default=0)
    procedures = relationship("WarehouseProcedure", backref="repository_warehouse_packages")
    functions = relationship("WarehouseFunction", backref="repository_warehouse_packages")
    schema_id = Column(Integer, ForeignKey("repository_warehouse_schemas.id"))

    def __repr__(self):
        """String representation
        """
        return ("Warehouse Package [Name=%s]") % (self.name)

class WarehouseProcedure(AbstractWarehouseObject):
    """Maintains information about an procedure in the Warehouse
    """
    __tablename__ = 'repository_warehouse_procedures'

    number_of_parameters = Column(Integer, default=0)
    parameters = Column(String(1000))
    is_valid = Column(Boolean, default=True)
    sql = Column(String(4000))
    schema_id = Column(Integer, ForeignKey("repository_warehouse_schemas.id"))
    belongs_to_package = Column(Boolean, default=False)
    package_id = Column(Integer, ForeignKey("repository_warehouse_packages.id"))

    def __repr__(self):
        """Provides string representation
        """
        return ("Warehouse Procedure [Name=%s, SchemaId=%d, PackageId=%d]") % (
            self.name, self.schema_id if self.schema_id != None else -1,
            self.package_id if self.package_id != None else -1)


class WarehouseFunction(AbstractWarehouseObject):
    """Represents an SQL function in the target warehouse
    """
    __tablename__ = 'repository_warehouse_functions'

    number_of_parameters = Column(Integer, default=0)
    parameters = Column(String(1000))
    return_type = Column(String)
    is_valid = Column(Boolean, default=True)
    sql = Column(String(4000))
    belongs_to_package = Column(Boolean, default=False)
    schema_id = Column(Integer, ForeignKey("repository_warehouse_schemas.id"))
    package_id = Column(Integer, ForeignKey("repository_warehouse_packages.id"))

    def __repr__(self):
        """Provides string representation
        """
        return ("Warehouse Function [Name=%s, SchemaId=%d, PackageId=%d]") % (
            self.name, self.schema_id if self.schema_id != None else -1,
            self.package_id if self.package_id != None else -1)
