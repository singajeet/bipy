"""Manager class to manager project objects and interact with other
    services for this purpose
    Author: Ajeet Singh
    Date: 6/14/2019
"""
import os
from bipy.services.project_management.objects import Project, ProjectItem,\
    ProjectFile
from bipy.services.project_management.objects import ProjectFolder,\
    ProjectDataSet, ProjectFact
from bipy.services.project_management.objects import ProjectDimension,\
    ProjectMetric, Property
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
        """Connects the project manager to database through passed
            connection object

            Args:
                conn(WarehouseConnection): Connection to an existing database
        """
        LOGGER.debug("Connecting to the database...")
        self.__CONNECTION = conn
        self.__SESSION = conn.get_session()
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

            Returns:
                project (Project): Returns an project object
        """
        if name is not None:
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
            return project
        else:
            raise ValueError("Value of parameter can't be None")

    def create_item(self, id, name, desc=None):
        """Creates an item in the project and assign the corresponding
            analysis items id to it

            Args:
                id (int): An id of the correspoding analysis item
                name (string): Name of the item
                desc (String): Description of the item

            Returns:
                item (ProjectItem): Returns an item object
        """
        if name is not None:
            LOGGER.debug("Creating new item: %s" % (name))
            item = ProjectItem()
            item.name = name
            item.description = desc
            item.analysis_item_id = id
            self.__SESSION.add(item)
            self.__SESSION.commit()
            LOGGER.debug("Item created successfully!")
            return item
        else:
            raise ValueError("Value of parameter name can't be None")

    def create_file(self, name, path, desc=None, icon=None):
        """Creates a file object within a project

            Args:
                name (String): Name of the file with extension
                path (String): Path to the file on the file system
                desc (Strign): OPTIONAL! Description of the file
                icon (String): OPTIONAL! Path to the icon used for this file

            Returns:
                file (ProjectFile): Returns an file item
        """
        if name is not None:
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
            return file
        else:
            raise ValueError("Value of parameter name can't be None")

    def create_folder(self, name, path, desc=None, icon=None):
        """Creates a new folder object within a project

            Auth:
                name (String): Name of the folder
                path (String): Path to the folder on the file system
                desc (String): OPTIONAL! Description of the folder
                icon (String): OPTIONAL! Path to the icon file
                                if one is required

            Return:
                folder (ProjectFolder): Returns an folder item
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
        return folder

    def create_dataset(self, id, name, desc=None):
        """Creates a dataset representation in the project to be show in GUI

            Args:
                id (int): Analysis id of the dataset
                name (String): Name of the dataset
                desc (String): OPTIONAL! Description of dataset if its
                                available

            Returns:
                dataaet (ProjectDataSet): An dataset object
        """
        LOGGER.debug("Creating new dataset: %s" % (name))
        ds = ProjectDataSet()
        ds.name = name
        ds.analysis_dataset_id = id
        ds.description = desc
        self.__SESSION.add(ds)
        self.__SESSION.commit()
        LOGGER.debug("Dataset created successfully!")
        return ds

    def create_fact(self, id, name, desc=None):
        """Creates a representation of dataset to be shown in project

            Args:
                id (int): Id of the Analysis fact object
                name (String): Name of the fact
                desc(String): OPTIONAL! Description of the fact

            Return:
                fact (ProjectFact): A fact object
        """
        LOGGER.debug("Creating new Fact: %s" % (name))
        fact = ProjectFact()
        fact.analysis_fact_id = id
        fact.name = name
        fact.description = desc
        self.__SESSION.add(fact)
        self.__SESSION.commit()
        LOGGER.debug("Fact created successfully!")
        return fact

    def create_dimension(self, id, name, desc=None):
        """Creates a new dimension to be shown under an project

            Args:
                id (int): Id of the analysis dimension object
                name (String): Name of the dimension
                desc (String): OPTIONAL! Description of the dimension

            Returns:
                dim (ProjectDimension): Returns an dim object
        """
        LOGGER.debug("Creating a new dimension: %s" % (name))
        dim = ProjectDimension()
        dim.analysis_dimension_id = id
        dim.name = name
        dim.description = desc
        self.__SESSION.add(dim)
        self.__SESSION.commit()
        LOGGER.debug("Dimension created successfully!")
        return dim

    def create_metric(self, id, name, desc=None):
        """Creates a new metric to be shown under a project

            Args:
                id (int): Id of the analysis metric object
                name (String): Name of the metric
                desc (String): OPTIONAL! Description of the metric

            Returns:
                metric (ProjectMetric): Returns an metric object
        """
        LOGGER.debug("Creating a new metric: %s" % (name))
        metric = ProjectMetric()
        metric.analysis_metric_id = id
        metric.name = name
        metric.description = desc
        self.__SESSION.add(metric)
        self.__SESSION.commit()
        LOGGER.debug("Metric created successfully!")
        return metric

    def create_property(self, name, value, desc=None):
        """Creates an property object and returns same,
            so that it can be associated with other objects

            Args:
                name (String): Name of the property
                value (String): Value of the property to be
                                stored
                desc (String): OPTIONAL! Description of the property


            Rrturns:
                property (Property): Returns an object of property
        """
        LOGGER.debug("Creating an property: '%s'" % (name))
        prop = Property()
        prop.name = name
        prop.value = value
        prop.description = desc
        self.__SESSION.add(prop)
        self.__SESSION.commit()
        LOGGER.debug("Property created successfully!")

    def add_item_to_project(self, item, project):
        """Adds an passed item to the list of items in a project

            Args:
                item (ProjectItem): Item that needs to be added to project
                project(Project): A project under which item will be added
        """
        LOGGER.debug("Adding item '%s' to project '%s'" % (item.name,
                                                           project.name))
        if project is not None:
            project.items.append(item)
            self.__SESSION.commit()
            LOGGER.debug("Item added to project successfully!")
        else:
            raise ValueError("Value of project parameter can't\
                             be None")

    def add_file_to_project(self, file, project):
        """Adds an project fie to project's file list

            Args:
                file (ProjectFile): File that needs to be added to project
                project (Project): Project under which file will be added
        """
        LOGGER.debug("Adding item '%s' to project '%s'" % (file.name,
                                                           project.name))
        if project is not None:
            project.files.append(file)
            self.__SESSION.commit()
            LOGGER.debug("File has been added to project successfully!")
        else:
            raise ValueError("Value of project parameter can't be None")

    def add_folder_to_project(self, folder, project):
        """Adds an project folder to project's folder list

            Args:
                folder (ProjectFolder): Folder that needs to be added to
                project
                project (Project): Project under which folder will be added
        """
        LOGGER.debug("Adding item '%s' to project '%s'" % (folder.name,
                                                           project.name))
        if project is not None:
            project.folders.append(folder)
            self.__SESSION.commit()
            LOGGER.debug("Folder has been added to project successfully!")
        else:
            raise ValueError("Value of project parameter can't be None")

    def add_property_to_project(self, property, project):
        """Adds an project property to project's properties list

            Args:
                folder (Property): Property that needs to be added to
                project
                project (Project): Project under which property will be added
        """
        LOGGER.debug("Adding property '%s' to project '%s'" % (property.name,
                                                               project.name))
        if project is not None:
            project.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to project successfully!")
        else:
            raise ValueError("Value of project parameter can't be None")

    def add_file_to_folder(self, file, folder):
        """Adds an project fie to a folder

            Args:
                file (ProjectFile): File that needs to be added to project
                project (ProjectFolder): ProjectFolder under which file
                                        will be added
        """
        LOGGER.debug("Adding item '%s' to folder '%s'" % (file.name,
                                                          folder.name))
        if folder is not None:
            folder.files.append(file)
            self.__SESSION.commit()
            LOGGER.debug("File has been added to folder successfully!")
        else:
            raise ValueError("Value of folder parameter can't be None")

    def add_folder_to_folder(self, s_folder, t_folder):
        """Adds a project folder to an another folder's list

            Args:
                s_folder (ProjectFolder): Folder that needs to be added to
                target folder
                t_folder (ProjectFolder): Target Folder under which
                                        source folder will be added
        """
        LOGGER.debug("Adding folder '%s' to folder '%s'" % (s_folder.name,
                                                            t_folder.name))
        if t_folder is not None:
            t_folder.folders.append(s_folder)
            self.__SESSION.commit()
            LOGGER.debug("Folder has been added to another folder\
                         successfully!")
        else:
            raise ValueError("Value of target folder parameter can't be None")

    def add_property_to_folder(self, property, folder):
        """Adds an property to folder's properties list

            Args:
                folder (Property): Property that needs to be added to
                project
                folder (ProjectFolder): Folder under which property
                                        will be added
        """
        LOGGER.debug("Adding property '%s' to folder '%s'" % (property.name,
                                                              folder.name))
        if folder is not None:
            folder.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to folder successfully!")
        else:
            raise ValueError("Value of folder parameter can't be None")

    def add_dataset_to_folder(self, dataset, folder):
        """Adds an dataset used in project to the folder
            passed as argument

            Args:
                dataset (ProjectDataSet): DataSet that needs to be added
                to project
                folder (ProjectFolder): Folder under which dataset wiill
                be added
        """
        LOGGER.debug("Adding dataset '%s' to folder '%s'" % (dataset.name,
                                                             folder.name))
        if folder is not None:
            folder.datasets.append(dataset)
            self.__SESSION.commit()
            LOGGER.debug("DataSet has been added to project successfully!")
        else:
            raise ValueError("Value of parameter folder can't be None")

    def add_fact_to_folder(self, fact, folder):
        """Adds an fact to folder passed as parameter

            Args:
                fact (ProjectFact): Fact that needs to be added
                folder (ProjectFolder): Folder under which fact will be
                added
        """
        LOGGER.debug("Adding fact '%s' to folder '%s'" % (fact.name,
                                                          folder.name))
        if folder is not None:
            folder.facts.append(fact)
            self.__SESSION.commit()
            LOGGER.debug("Fact has been added to folder successfully")
        else:
            raise ValueError("The value of parameter folder can't be None")

    def add_dimension_to_folder(self, dim, folder):
        """Adds an dimension to a folder passed as param

            Args:
                dim (ProjectDimension): Dimension that needs to be added
                folder (ProjectFolder): Folder under which dim needs to be
                added
        """
        LOGGER.debug("Adding dimension '%s' to folder '%s'" % (dim.name,
                                                               folder.name))
        if folder is not None:
            folder.dimensions.append(dim)
            self.__SESSION.commit()
            LOGGER.debug("Dimension has been added to folder successfully!")
        else:
            raise ValueError("The value of folder parameter can't be None")

    def add_metric_to_folder(self, metric, folder):
        """Adds an metric to a folder passed as
            param

            Args:
                metric (ProjectMetric): Metric that needs to be added
                folder (ProjectFolder): Folder under which metric needs to be
                                        added
        """
        LOGGER.debug("Adding metric '%s' to folder '%s'" % (metric.name,
                                                            folder.name))
        if folder is not None:
            folder.metrices.append(metric)
            self.__SESSION.commit()
            LOGGER.debug("Metric has been added successfully!")
        else:
            raise ValueError("The value of folder parameter\
                             shouldn't be None")
