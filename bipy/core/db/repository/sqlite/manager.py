"""
    An repository manager used to manage warehouse objects stored in repository
    Author: Ajeet Singh
    Date: 05/31/2019
"""
from bipy.core.db import categories
from bipy.core.db.repository.objects import WarehouseDatabase, WarehouseSchema
from bipy.core.db.repository.objects import WarehouseTable, WarehouseColumn


class RepositoryManager(categories.SQLite):
    """
        An manager class to manage repo objects
    """

    __instance = None
    __connection = None
    __session = None

    def __new__(cls):
        """ Method to create singleton instance
        """
        if RepositoryManager.__instance is None:
            RepositoryManager.__instance = object.__new__(cls)
        return RepositoryManager.__instance

    def __init__(self):
        """ Default constructor
        """
        categories.SQLite.__init__(self)

    def connect(self, conn):
        """ Init connection with meta repo db

            Args:
                conn(ConnectionManager): An connection instance to DB

        """
        self.__connection = conn
        self.__session = self.__connection.get_session()

    def save(self, repo_obj):
        """ Saves the repo object to database

            Args:
                repo_obj(AbstractWarehouseObject): An instance of warehouse
                object
        """
        self.__session.add(repo_obj)
        self.__session.commit()

    def save_all(self, repo_objs):
        """ Save all repo objects passed as list

            Args:
                repo_objs(List): An list of `AbstractWarehouseObject` objects
        """
        self.__session.add_all(repo_objs)
        self.__session.commit()

    def update(self):
        """ Updates all objects associated with current session
        """
        self.__session.commit()

    def delete(self, repo_obj):
        """Delete an repo object from db

            Args:
                repo_obj(AbstractWarehouseObject): An instance of warehouse
                item
        """
        repo_obj.delete()
        self.__session.commit()

    def get_database(self, param):
        """ Returns an instance of `WarehouseDatabase` class

            Args:
                param (int/str): An id or name of the database
        """
        if isinstance(param, int):
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.id == param).first()
        elif isinstance(param, str):
            return self.__session.query(WarehouseDatabase)\
                    .filter(WarehouseDatabase.name == param).first()
        return None

    def get_all_databases(self):
        """ Returns an list of all `WarehouseDatabase` objects
        """
        return self.__session.query(WarehouseDatabase).all()

    def get_database_names(self):
        """ Returns an list of names of all databases
        """
        _names = []
        dbs = self.__session.query(WarehouseDatabase).all()
        for _db in dbs:
            _names.append(_db.name)
        return _names

    def get_schema(self, param, database=None):
        """ Returns an instance of `WarehouseSchema` class stored in database based on
            id or name. If database parameter is passed, it will return schemas
            available under that database only

            Args:
                param(int/str): An Id or name of the schema
                database(WarehouseDatabase): An instance of WarehouseDatabase class
        """
        if database is None:
            if isinstance(param, int):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.id == param).first()
            elif isinstance(param, str):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.name == param).first()
        else:
            if isinstance(param, int):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.id == param \
                                and WarehouseSchema.database_id == database.id).first()
            elif isinstance(param, str):
                return self.__session.query(WarehouseSchema)\
                        .filter(WarehouseSchema.name == param \
                               and WarehouseSchema.database_id == database.id).first()
        return None

    def get_all_schemas(self, database=None):
        """ Returns instances of all schemas available under an database passed as
            parameter else returns all schemas available under all databases

            Args:
                database(WarehouseDatabase): An instance of WarehouseDatabase class
        """
        if database is None:
            return self.__session.query(WarehouseSchema).all()

        return self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.database_id == database.id).all()

    def get_all_schema_names(self, database=None):
        """Returns names of all available schemas under an passed database or
            all schemas under all database

            Args:
                database(WarehouseDatabase): An instance of WarehouseDatabase class
        """
        _names = []
        _schemas = None
        if database is None:
            _schemas = self.__session.query(WarehouseSchema).all()
        else:
            _schemas = self.__session.query(WarehouseSchema)\
                    .filter(WarehouseSchema.database_id == database.id).all()
        for sch in _schemas:
            _names.append(sch.name)
        return _names

    def get_table(self, param, schema=None):
        """ Returns an instance of `WarehouseTable` available under an schema passed
            as parameter else returns instances of all tables matching the table name or
            id passed as parameter(param)

            Args:
                param(int/str): An id or name of the table
                schema(WarehouseSchema): An instance of schema class
        """
        if schema is None:
            if isinstance(param, str):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param).first()
            elif isinstance(param, int):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.id == param).first()
        else:
            if isinstance(param, str):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param and\
                                WarehouseTable.schema_id == schema.id)\
                        .first()
            elif isinstance(param, int):
                return self.__session.query(WarehouseTable)\
                        .filter(WarehouseTable.name == param\
                                and WarehouseTable.schema_id == schema.id)\
                        .first()
        return None

    def get_all_tables(self, schema=None):
        """ Returns instances of all tables available under an schema passed
            as parameter else returns all tables from all schemas and
            databases

            Args:
                schema(WarehouseSchema): An instance of schema class
        """
        if schema is None:
            return self.__session.query(WarehouseTable).all()

        return self.__session.query(WarehouseTable)\
                    .filter(WarehouseTable.schema_id == schema.id).all()

    def get_all_table_names(self, schema=None):
        """ Returns name of all tables available under an schema passed as
            parameter else return name of all tables available under all
            schemas and databases

            Args:
                schema(WarehouseSchema): An instance of schema class
        """
        _tables = None
        _names = []
        if schema is None:
            _tables = self.__session.query(WarehouseTable).all()
        else:
            _tables = self.__session.query(WarehouseTable)\
                    .filter(WarehouseTable.schema_id == schema.id).all()
        for tab in _tables:
            _names.append(tab.name)

        return _names

    def get_column(self, column, table):
        """ Returns an instance of `WarehouseColumn` under an table
            passed as argument to this method

            Args:
                column(int/str): Name of the column or id
                table(WarehouseTable): An instance of table
        """
        if isinstance(column, str):
            return self.__session.query(WarehouseColumn)\
                .filter(WarehouseColumn.table_id == table.id\
                        and WarehouseColumn.name == column)\
                .first()
        elif isinstance(column, int):
            return self.__session.query(WarehouseColumn)\
                .filter(WarehouseColumn.id == column and\
                        WarehouseColumn.table_id == table.id)\
                .first()
        return None

    def get_all_columns(self, table):
        """ Returns instance list of all columns available
            under an table passed as argument

            Args:
                table(WarehouseTable): An instance of table
        """
        return self.__session.query(WarehouseColumn)\
            .filter(WarehouseColumn.table_id == table.id)\
            .all()

    def get_all_column_names(self, table):
        _names = []
        _columns = self.__session.query(WarehouseColumn)\
            .filter(WarehouseColumn.table_id == table.id)\
            .all()
        for col in _columns:
            _names.append(col.name)
        return _names

    def add_schema_to_db(self, schema, db):
        """ Add an schema passed as argument to the db passed
            as well

            Args:
                schema(WarehouseSchema): An instance of schema
                db(WarehouseDatabase): An instance of db
        """
        db_exists = self.get_database(db.name)\
            .__len__() != 0
        schema_exists = self.get_schema(schema.name, db)\
            .__len__() != 0
        if not db_exists:
            self.save(db)
        if not schema_exists:
            self.save(schema)
        db.schemas.append(schema)
        self.__session.commit()

    def add_schemas_to_db(self, schemas, db):
        """ Same as add_schema_to_db but this adds an list of
            schemas to db

            Args:
                schemas(List): An list of schema objects
                db(WarehouseDatabase): An db object
        """
        for schema in schemas:
            self.add_schema_to_db(schema, db)

    def add_table_to_schema(self, table, schema):
        """ Add's an table to provided schema. It also saves the
            table and schema objects if not already saved

            Args:
                table(WarehouseTable): An table object
                schema(WarehouseSchema): An schema object
        """
        schema_exists = self.get_schema(schema.name)\
            .__len__() != 0
        table_exists = self.get_table(table.name, schema)\
            .__len__() != 0
        if not schema_exists:
            self.save(schema)
        if not table_exists:
            self.save(table)
        schema.tables.append(table)
        self.__session.commit()

    def add_tables_to_schema(self, tables, schema):
        """ Add's a list of tables under the provided
            schema. It is similar to add_table_to_schema

            Args:
                tables(List): A list of table instances
                schema(WarehouseSchema): An instance of schema objects
        """
        for tab in tables:
            self.add_table_to_schema(tab, schema)

    def add_column_to_table(self, column, table):
        """ Add's an column instance to the table provided as
            parameter

            Args:
                column(WarehouseColumn): An instance of column
                table(WarehouseTable): An instance of table
        """
        table_exists = self.get_table(table.name)\
            .__len__() != 0
        column_exists = self.get_column(column.name, table)\
            .__len__() != 0
        if not table_exists:
            self.save(table)
        if not column_exists:
            self.save(column)
        table.columns.append(column)
        self.__session.commit()

    def add_columns_to_table(self, columns, table):
        """ Add columns from provided list to table ppassed as
            argument

            Args:
                columns(List): A list of columns to be added to DB
                table(WarehouseTable): An instance of table class
        """
        for col in columns:
            self.add_column_to_table(col, table)

    def remove_schema_from_db(self, schema, db):
        """ Removes provided schema from list of schemas available
            under db passed as argument

            Args:
                schema(WarehouseSchema): Schema object to be removed
                table(WarehouseTable): Table containing the schema object
        """
        for sch in db.schemas:
            if sch.id == schema.id:
                db.schemas.remove(sch)

    def remove_table_from_schema(self, table, schema):
        """ Removes the provided table from list of tables available
            under passed schema

            Args:
                table(WarehouseTable): Table object that needs to be
                    removed
                    schema(WarehouseSchema): Schema object that contains
                        the tables
        """
        for tb in schema.tables:
            if tb.id == table.id:
                schema.tables.remove(tb)
