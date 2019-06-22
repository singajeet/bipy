"""This module contains all model objects used in the analysis application

    Author: Ajeet Singh
    Date: 06/21/2019
"""
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase
from sqlalchemy import Column, Integer, String, Sequence, Boolean, ForeignKey, DateTime
from datetime import datetime


Base = declarative_base()


class AnalysisAbstractModel(AbstractConcreteBase, Base):
    """An abstract class with common attributes used by all
    classes in this module
    """

    id = Column(Integer, Sequence('analysis_id_seq'), primary_key=True)
    name = Column(String(255))
    description = Column(String(1000))
    created_by = Column(String(255))
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_by = Column(String(255))
    modified_on = Column(DateTime)


class DataSet(AnalysisAbstractModel):
    """Represents an logical view of a table having columns, where condition,
    aggregation requirement and having claue defined. This will server as the
    base for creating dimensions and facts/metrics on it.

    Attributes:
        schema_id (int): Schema id from the 'repository_warehouse_schemas' table
                            or from WarehouseSchema in repository module
        table_id (int): Table id from the 'repository_warehouse_tables' table
                            or from WarehouseTable in repository module
        column_ids (String): A list of comma separated id's of columns from
                                WarehouseColumn or 'repository_warehouse_columns'
        where_condition (String): An SQL condition defined on the table if required
        is_aggregated (Boolean): Tells whether the data in table is aggregated or not,
                                    if yes, following attributes should have value
        group_by (String): A comma separated list of column names from the table
        having_condition (String): A comma separated list of column names from table
    """

    __tablename__ = "analysis_dataset"

    schema_id = Column(Integer, nullable=False)
    table_id = Column(Integer, nullable=False)
    column_ids = Column(String(1000), nullable=False)
    where_codition = Column(String(1000))
    is_aggregated = Column(Boolean)
    group_by = Column(String(255))
    having_condition = Column(String(1000))
