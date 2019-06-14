"""Manager class to manager project objects and interact with other
    services for this purpose
    Author: Ajeet Singh
    Date: 6/14/2019
"""
import os
from bipy.services.project_management.objects import Project, ProjectItem, ProjectFile
from bipy.services.project_management.objects import ProjectFolder, ProjectDataSet, ProjectFact
from bipy.services.project_management.objects import ProjectDimension, ProjectMetric, Property
from bipy.services.db.categories import AbstractCategory
from bipy.services.utils import Utility
from bipy.logging import logger


LOGGER = logger.get_logger(__name__)


class ProjectManager(AbstractCategory):
    """Class to manager project and interact with other UI services """

    __INSTANCE = None
    __CONF = None
    __UTIL = None
    __CONNECTION = None
    __SESSION = None

    def __new__(cls):
        """Method to create singleton object"""
        if ProjectManager.__INSTANCE is None:
            ProjectManager.__INSTANCE = object.__new__(cls)
        return ProjectManager.__INSTANCE

    def __init__(self):
        """Default constructor"""
        AbstractCategory.__init__(self)
        self.__UTIL = Utility()
        self.__CONF = self.__UTIL.CONFIG
        LOGGER.debug("Project Manager instance created")

    def connect(self, conn):
        """Connects the project manager to database through passed connection object

            Args:
                conn(WarehouseConnection): Connection to an existing database
        """
        LOGGER.debug("Connecting to the database...")
        __CONNECTION = conn
        __SESSION = conn.get_session()
        LOGGER.debug("Connected to database successfully!")

    def create_project(self, id, name, proj_type, path, desc=None):
        """Creates a new project for visual purpose in the GUI. This is a
            proxy to analysis project.

            Args:
                id (int): An id of Analysis project
                name (String): Name of the project
                proj_type(String): Type of project we are creating
                path(String): An absolute path to the project on file system
                desc (String): Description of the project
        """
        LOGGER.debug("Creating new project: %s" % (name))
        project = Project()
        project.name = name
        project.description = desc
        project.analysis_project_id = id
        project.project_type = proj_type
        project.path = path
        self.__SESSION.add(project)
        self.__SESSION.commit()
        LOGGER.debug("Projected created successfully!")

    def create_item(self, id, name, desc=None):
        """Creates an item in the project and assign the corresponding
            analysis items id to it

            Args:
                id (int): An id of the correspoding analysis item
                name (string): Name of the item
                desc (String): Description of the item
        """
        LOGGER.debug("Creating new item: %s" % (name))
        item = ProjectItem()
        item.name = name
        item.description = desc
        item.analysis_item_id = id
        self.__SESSION.add(item)
        self.__SESSION.commit()
        LOGGER.debug("Item created successfully!")

    def create_file(self, name, path, desc=None, icon=None):
        """Creates a file object within a project

            Args:
                name (String): Name of the file with extension
                path (String): Path to the file on the file system
                desc (Strign): OPTIONAL! Description of the file
                icon (String): OPTIONAL! Path to the icon used for this file
        """
        LOGGER.debug("Creating new file: %s" % (name))
        file = ProjectFile()
        file.name = name
        file.file_path = path
        file.description = desc
        file.file_type = os.path.splitext(name)
        file.file_icon = icon
        self.__SESSION.add(file)
        self.__SESSION.commit()
        LOGGER.debug("File created successfully!")

    def create_folder(self, name, path, desc=None, icon=None):
        """Creates a new folder object within a project

            Auth:
                name (String): Name of the folder
                path (String): Path to the folder on the file system
                desc (String): OPTIONAL! Description of the folder
                icon (String): OPTIONAL! Path to the icon file if one is required
        """
        LOGGER.debug("Creating a new folder: %s" % (name))
        folder = ProjectFolder()
        folder.name = name
        folder.folder_path = path
        folder.description = desc
        folder.folder_icon = icon
        self.__SESSION.add(folder)
        self.__SESSION.commit()
        LOGGER.debug("Folder created successfully!")

    def create_dataset(self, id, name, desc=None):
        """Creates a dataset representation in the project to be show in GUI

            Args:
                id (int): Analysis id of the dataset
                name (String): Name of the dataset
                desc (String): OPTIONAL! Description of dataset if its available
        """
        LOGGER.debug("Creating new dataset: %s" % (name))
        ds = ProjectDataSet()
        ds.name = name
        ds.analysis_dataset_id = id
        ds.description = desc
        self.__SESSION.add(ds)
        self.__SESSION.commit()
        LOGGER.debug("Dataset created successfully!")

    def create_fact(self, id, name, desc=None):
        """Creates a representation of dataset to be shown in project

            Args:
                id (int): Id of the Analysis fact object
                name (String): Name of the fact
                desc(String): OPTIONAL! Description of the fact
        """
        LOGGER.debug("Creating new Fact: %s" % (name))
        fact = ProjectFact()
        fact.analysis_fact_id = id
        fact.name = name
        fact.description = desc
        self.__SESSION.add(fact)
        self.__SESSION.commit()
        LOGGER.debug("Fact created successfully!")

    def create_dimension(self, id, name, desc=None):
        """Creates a new dimension to be shown under an project

            Args:
                id (int): Id of the analysis fact object
                name (String): Name of the dimension
                desc (String): OPTIONAL! Description of the dimension
        """
        LOGGER.debug("Creates a new dimension: %s" % (name))
        dim = ProjectDimension()
        dim.analysis_dimension_id = id
        dim.name = name
        dim.description = desc
        self.__SESSION.add(dim)
        self.__SESSION.commit()
        LOGGER.debug("Dimension created successfully!")
        """
