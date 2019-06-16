""" Manager class to manager project objects and interact with other
    services for this purpose
    Author: Ajeet Singh
    Date: 6/14/2019
"""
import os
from datetime import datetime
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
        if name is not None and id is not None:
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
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

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
        if name is not None and id is not None:
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
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

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
        if name is not None and id is not None:
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
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

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
        if name is not None and id is not None:
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
        else:
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

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
        if name is not None and id is not None:
            LOGGER.debug("Creating new dataset: %s" % (name))
            ds = ProjectDataSet()
            ds.name = name
            ds.analysis_dataset_id = id
            ds.description = desc
            self.__SESSION.add(ds)
            self.__SESSION.commit()
            LOGGER.debug("Dataset created successfully!")
            return ds
        else:
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

    def create_fact(self, id, name, desc=None):
        """Creates a representation of dataset to be shown in project

            Args:
                id (int): Id of the Analysis fact object
                name (String): Name of the fact
                desc(String): OPTIONAL! Description of the fact

            Return:
                fact (ProjectFact): A fact object
        """
        if name is not None and id is not None:
            LOGGER.debug("Creating new Fact: %s" % (name))
            fact = ProjectFact()
            fact.analysis_fact_id = id
            fact.name = name
            fact.description = desc
            self.__SESSION.add(fact)
            self.__SESSION.commit()
            LOGGER.debug("Fact created successfully!")
            return fact
        else:
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

    def create_dimension(self, id, name, desc=None):
        """Creates a new dimension to be shown under an project

            Args:
                id (int): Id of the analysis dimension object
                name (String): Name of the dimension
                desc (String): OPTIONAL! Description of the dimension

            Returns:
                dim (ProjectDimension): Returns an dim object
        """
        if name is not None and id is not None:
            LOGGER.debug("Creating a new dimension: %s" % (name))
            dim = ProjectDimension()
            dim.analysis_dimension_id = id
            dim.name = name
            dim.description = desc
            self.__SESSION.add(dim)
            self.__SESSION.commit()
            LOGGER.debug("Dimension created successfully!")
            return dim
        else:
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

    def create_metric(self, id, name, desc=None):
        """Creates a new metric to be shown under a project

            Args:
                id (int): Id of the analysis metric object
                name (String): Name of the metric
                desc (String): OPTIONAL! Description of the metric

            Returns:
                metric (ProjectMetric): Returns an metric object
        """
        if name is not None and id is not None:
            LOGGER.debug("Creating a new metric: %s" % (name))
            metric = ProjectMetric()
            metric.analysis_metric_id = id
            metric.name = name
            metric.description = desc
            self.__SESSION.add(metric)
            self.__SESSION.commit()
            LOGGER.debug("Metric created successfully!")
            return metric
        else:
            raise ValueError("Value of parameter 'name' and 'id' can't be None")

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
        if name is not None:
            LOGGER.debug("Creating an property: '%s'" % (name))
            prop = Property()
            prop.name = name
            prop.value = value
            prop.description = desc
            self.__SESSION.add(prop)
            self.__SESSION.commit()
            LOGGER.debug("Property created successfully!")
            return prop
        else:
            raise ValueError("Value of parameter 'name' can't be None")

    def add_item_to_project(self, item, project):
        """Adds an passed item to the list of items in a project

            Args:
                item (ProjectItem): Item that needs to be added to project
                project(Project): A project under which item will be added
        """
        if project is not None and item is not None:
            LOGGER.debug("Adding item '%s' to project '%s'" % (item.name,
                                                               project.name))
            project.items.append(item)
            self.__SESSION.commit()
            LOGGER.debug("Item added to project successfully!")
        else:
            raise ValueError("Value of parameter 'item' and 'project'\
                             can't be None")

    def add_file_to_project(self, file, project):
        """Adds an project fie to project's file list

            Args:
                file (ProjectFile): File that needs to be added to project
                project (Project): Project under which file will be added
        """
        if project is not None and file is not None:
            LOGGER.debug("Adding item '%s' to project '%s'" % (file.name,
                                                               project.name))
            project.files.append(file)
            self.__SESSION.commit()
            LOGGER.debug("File has been added to project successfully!")
        else:
            raise ValueError("Value of parameter 'file' and 'project'\
                             can't be None")

    def add_folder_to_project(self, folder, project):
        """Adds an project folder to project's folder list

            Args:
                folder (ProjectFolder): Folder that needs to be added to
                project
                project (Project): Project under which folder will be added
        """
        if project is not None and folder is not None:
            LOGGER.debug("Adding item '%s' to project '%s'" % (folder.name,
                                                               project.name))
            project.folders.append(folder)
            self.__SESSION.commit()
            LOGGER.debug("Folder has been added to project successfully!")
        else:
            raise ValueError("Value of parameter 'folder' and 'project'\
                             can't be None")

    def add_property_to_project(self, property, project):
        """Adds an project property to project's properties list

            Args:
                folder (Property): Property that needs to be added to
                project
                project (Project): Project under which property will be added
        """
        if project is not None and property is not None:
            LOGGER.debug("Adding property '%s' to project '%s'" % (property.name,
                                                                   project.name))
            project.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to project successfully!")
        else:
            raise ValueError("Value of parameter 'property' and 'project'\
                             can't be None")

    def add_file_to_folder(self, file, folder):
        """Adds an project fie to a folder

            Args:
                file (ProjectFile): File that needs to be added to project
                project (ProjectFolder): ProjectFolder under which file
                                        will be added
        """
        if folder is not None and file is not None:
            LOGGER.debug("Adding item '%s' to folder '%s'" % (file.name,
                                                              folder.name))
            folder.files.append(file)
            self.__SESSION.commit()
            LOGGER.debug("File has been added to folder successfully!")
        else:
            raise ValueError("Value of 'folder' and 'file' parameters can't be None")

    def add_folder_to_folder(self, s_folder, t_folder):
        """Adds a project folder to an another folder's list

            Args:
                s_folder (ProjectFolder): Folder that needs to be added to
                target folder
                t_folder (ProjectFolder): Target Folder under which
                                        source folder will be added
        """
        if t_folder is not None and s_folder is not None:
            LOGGER.debug("Adding folder '%s' to folder '%s'" % (s_folder.name,
                                                                t_folder.name))
            t_folder.folders.append(s_folder)
            self.__SESSION.commit()
            LOGGER.debug("Folder has been added to another folder\
                         successfully!")
        else:
            raise ValueError("Value of 'target' and 'source' folder\
                             parameters can't be None")

    def add_property_to_folder(self, property, folder):
        """Adds an property to folder's properties list

            Args:
                folder (Property): Property that needs to be added to
                project
                folder (ProjectFolder): Folder under which property
                                        will be added
        """
        if folder is not None and property is not None:
            LOGGER.debug("Adding property '%s' to folder '%s'" % (property.name,
                                                                  folder.name))
            folder.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to folder successfully!")
        else:
            raise ValueError("Value of 'folder' and 'property' parameter can't be None")

    def add_dataset_to_folder(self, dataset, folder):
        """Adds an dataset used in project to the folder
            passed as argument

            Args:
                dataset (ProjectDataSet): DataSet that needs to be added
                to project
                folder (ProjectFolder): Folder under which dataset wiill
                be added
        """
        if folder is not None and dataset is not None:
            LOGGER.debug("Adding dataset '%s' to folder '%s'" % (dataset.name,
                                                                 folder.name))
            folder.datasets.append(dataset)
            self.__SESSION.commit()
            LOGGER.debug("DataSet has been added to project successfully!")
        else:
            raise ValueError("Value of parameter 'folder' and 'dataset' can't be None")

    def add_fact_to_folder(self, fact, folder):
        """Adds an fact to folder passed as parameter

            Args:
                fact (ProjectFact): Fact that needs to be added
                folder (ProjectFolder): Folder under which fact will be
                added
        """
        if folder is not None and fact is not None:
            LOGGER.debug("Adding fact '%s' to folder '%s'" % (fact.name,
                                                              folder.name))
            folder.facts.append(fact)
            self.__SESSION.commit()
            LOGGER.debug("Fact has been added to folder successfully")
        else:
            raise ValueError("The value of parameter 'folder' and 'fact' can't be None")

    def add_dimension_to_folder(self, dim, folder):
        """Adds an dimension to a folder passed as param

            Args:
                dim (ProjectDimension): Dimension that needs to be added
                folder (ProjectFolder): Folder under which dim needs to be
                added
        """
        if folder is not None and dim is not None:
            LOGGER.debug("Adding dimension '%s' to folder '%s'" % (dim.name,
                                                                   folder.name))
            folder.dimensions.append(dim)
            self.__SESSION.commit()
            LOGGER.debug("Dimension has been added to folder successfully!")
        else:
            raise ValueError("The value of 'folder' and 'dim' parameter can't be None")

    def add_metric_to_folder(self, metric, folder):
        """Adds an metric to a folder passed as
            param

            Args:
                metric (ProjectMetric): Metric that needs to be added
                folder (ProjectFolder): Folder under which metric needs to be
                                        added
        """
        if folder is not None and metric is not None:
            LOGGER.debug("Adding metric '%s' to folder '%s'" % (metric.name,
                                                                folder.name))
            folder.metrices.append(metric)
            self.__SESSION.commit()
            LOGGER.debug("Metric has been added successfully!")
        else:
            raise ValueError("The value of 'folder' and 'metric' parameters\
                             shouldn't be None")

    def add_property_to_item(self, property, item):
        """Adds an property to item object passed as param

            Args:
                property (Prepoerty): An property to be added
                item (ProjectItem): An item object to which property will be added
        """
        if property is not None and item is not None:
            LOGGER.debug("Adding property '%s' to item '%s'" % (property.name,
                                                                item.name))
            item.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to item successfully!")
        else:
            raise ValueError("Value of 'property' and 'item' parameter can't be None")

    def add_property_to_file(self, property, file):
        """Adds an property to file object passed as param

            Args:
                property (Prepoerty): An property to be added
                file (ProjectFile): An file object to which property will be added
        """
        if property is not None and file is not None:
            LOGGER.debug("Adding property '%s' to file '%s'" % (property.name,
                                                                file.name))
            file.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to file successfully!")
        else:
            raise ValueError("Value of 'property' and 'file' parameter can't be None")

    def add_fact_to_dataset(self, fact, dataset):
        """Adds an fact to datset passed as parameter

            Args:
                fact (ProjectFact): Fact that needs to be added
                dataset (ProjectDataSet): DataSet under which fact will be
                added
        """
        if dataset is not None and fact is not None:
            LOGGER.debug("Adding fact '%s' to dataset '%s'" % (fact.name,
                                                               dataset.name))
            dataset.facts.append(fact)
            self.__SESSION.commit()
            LOGGER.debug("Fact has been added to dataset successfully")
        else:
            raise ValueError("The value of parameter 'dataset' and 'fact' can't be None")

    def add_dimension_to_dataset(self, dim, dataset):
        """Adds an dimension to a dataset passed as param

            Args:
                dim (ProjectDimension): Dimension that needs to be added
                dataset (ProjectDataSet): DataSet under which dim needs to be
                added
        """
        if dataset is not None and dim is not None:
            LOGGER.debug("Adding dimension '%s' to dataset '%s'" % (dim.name,
                                                                    dataset.name))
            dataset.dimensions.append(dim)
            self.__SESSION.commit()
            LOGGER.debug("Dimension has been added to dataset successfully!")
        else:
            raise ValueError("The value of 'dataset' and 'dim' parameter can't be None")

    def add_metric_to_dataset(self, metric, dataset):
        """Adds an metric to a dataset passed as param

            Args:
                metric (ProjectMetric): Metric that needs to be added
                dataset (ProjectDataSet): DataSet under which metric needs to be
                                        added
        """
        if dataset is not None and metric is not None:
            LOGGER.debug("Adding metric '%s' to dataset '%s'" % (metric.name,
                                                                 dataset.name))
            dataset.metrices.append(metric)
            self.__SESSION.commit()
            LOGGER.debug("Metric has been added successfully!")
        else:
            raise ValueError("The value of 'dataset' and 'metric' parameters\
                             shouldn't be None")

    def add_property_to_dataset(self, property, dataset):
        """Adds an property to dataset object passed as param

            Args:
                property (Prepoerty): An property to be added
                dataset (ProjectDataSet): An dataset object to which property will
                be added
        """
        if property is not None and dataset is not None:
            LOGGER.debug("Adding property '%s' to dataset '%s'" % (property.name,
                                                                   dataset.name))
            dataset.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to dataset successfully!")
        else:
            raise ValueError("Value of 'property' and 'dataset' parameter can't be None")

    def add_property_to_fact(self, property, fact):
        """Adds an property to fact object passed as param

            Args:
                property (Prepoerty): An property to be added
                fact (ProjectFact): An fact object to which property will be added
        """
        if property is not None and fact is not None:
            LOGGER.debug("Adding property '%s' to fact '%s'" % (property.name,
                                                                fact.name))
            fact.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to fact successfully!")
        else:
            raise ValueError("Value of 'property' and 'fact' parameter can't be None")

    def add_property_to_dimension(self, property, dim):
        """Adds an property to dim object passed as param

            Args:
                property (Prepoerty): An property to be added
                dim (ProjectDimension): An dim object to which property will be added
        """
        if property is not None and dim is not None:
            LOGGER.debug("Adding property '%s' to dim '%s'" % (property.name,
                                                               dim.name))
            dim.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to Dimension successfully!")
        else:
            raise ValueError("Value of 'property' and 'dim' parameter can't be None")

    def add_property_to_metric(self, property, metric):
        """Adds an property to metric object passed as param

            Args:
                property (Prepoerty): An property to be added
                metric (ProjectMetric): An metric object to which property will be added
        """
        if property is not None and metric is not None:
            LOGGER.debug("Adding property '%s' to metric '%s'" % (property.name,
                                                                  metric.name))
            metric.properties.append(property)
            self.__SESSION.commit()
            LOGGER.debug("Property has been added to metric successfully!")
        else:
            raise ValueError("Value of 'property' and 'metric' parameter can't be\
                               None")

    def update(self, proj_obj):
        """ Method to update the project object and save back to database

            Args:
                proj_obj (ProjectXXX): An object of type ProjectXXX which needs to be
                                        updated
        """
        if proj_obj is not None:
            LOGGER.debug("Updating object with name: '%s'" % (proj_obj.name if
                                                              proj_obj.name is not
                                                              None else "Unknown"))
            proj_obj.modified_on = datetime.utcnow()
            self.__SESSION.commit()
            LOGGER.debug("Project object update successfully!")
        else:
            raise ValueError("Parameter 'proj_obj' can't be None")

    def remove_item_from_project(self, project, item):
        """Removes an item from the project

            Args:
                project (Project): Project from which item needs to be removed
                item (ProjectItem): An item object that needs to be removed
        """
        if project is not None and item is not None:
            LOGGER.debug("Removing item '%s' from project '%s'" %
                         (item.name, project.name))
            project.items.remove(item)
            LOGGER.debug("Item removed from the project successfully")
        else:
            raise ValueError("Parameter 'item' and 'project' can't be None")

    def remove_file_from_project(self, project, file):
        """ Removes an file from the project

            Args:
                project (Project): project from which file needs to be removed
                file (ProjectFile): file that needs to be removed from the project
        """
        if project is not None and file is not None:
            LOGGER.debug("Removing file '%s' from project '%s'" %
                         (file.name, project.name))
            project.files.remove(file)
            LOGGER.debug("File removed from project successfully")
        else:
            raise ValueError("Parameter 'file' and 'project' can't be None")

    def remove_folder_from_project(self, project, folder):
        """ Removes an folder from the project

            Args:
                project (Project): project from which folder needs to be removed
                folder (ProjectFolder): folder that needs to be removed from the project
        """
        if project is not None and folder is not None:
            LOGGER.debug("Removing folder '%s' from project '%s'" %
                         (folder.name, project.name))
            project.folders.remove(folder)
            LOGGER.debug("Folder removed from project successfully")
        else:
            raise ValueError("Parameter 'folder' and 'project' can't be None")

    def remove_property_from_project(self, project, property):
        """ Removes an property from the project

            Args:
                project (Project): project from which property needs to be removed
                property (Property): property that needs to be removed from the project
        """
        if project is not None and property is not None:
            LOGGER.debug("Removing property '%s' from project '%s'" %
                         (property.name, project.name))
            project.properties.remove(property)
            LOGGER.debug("Property removed from project successfully")
        else:
            raise ValueError("Parameter 'property' and 'project' can't be None")

    def remove_property_from_item(self, item, property):
        """ Removes an property from the item

            Args:
                item (ProjectItem): item from which property needs to be removed
                property (Property): property that needs to be removed from the item
        """
        if item is not None and property is not None:
            LOGGER.debug("Removing property '%s' from item '%s'" %
                         (property.name, item.name))
            item.properties.remove(property)
            LOGGER.debug("Property removed from item successfully")
        else:
            raise ValueError("Parameter 'property' and 'item' can't be None")

    def remove_file_from_folder(self, folder, file):
        """ Removes an file from the folder

            Args:
                folder (ProjectFolder): folder from which file needs to be removed
                file (ProjectFile): file that needs to be removed from the folder
        """
        if folder is not None and file is not None:
            LOGGER.debug("Removing file '%s' from folder '%s'" %
                         (file.name, folder.name))
            folder.files.remove(file)
            LOGGER.debug("File removed from folder successfully")
        else:
            raise ValueError("Parameter 'file' and 'folder' can't be None")

    def remove_folder_from_folder(self, s_folder, t_folder):
        """ Removes an folder from the folder

            Args:
                s_folder (Project): folder from which folder needs to be removed
                t_folder (ProjectFolder): folder that needs to be removed from the folder
        """
        if s_folder is not None and t_folder is not None:
            LOGGER.debug("Removing folder '%s' from folder '%s'" %
                         (s_folder.name, t_folder.name))
            s_folder.folders.remove(t_folder)
            LOGGER.debug("Folder removed from folder successfully")
        else:
            raise ValueError("Parameter 's_folder' and 't_folder' can't be None")

    def remove_property_from_folder(self, folder, property):
        """ Removes an property from the folder

            Args:
                folder (ProjectFolder): folder from which property needs to be removed
                property (Property): property that needs to be removed from the folder
        """
        if folder is not None and property is not None:
            LOGGER.debug("Removing property '%s' from folder '%s'" %
                         (property.name, folder.name))
            folder.properties.remove(property)
            LOGGER.debug("Property removed from folder successfully")
        else:
            raise ValueError("Parameter 'property' and 'folder' can't be None")

    def remove_dataset_from_folder(self, folder, dataset):
        """ Removes an dataset from the folder

            Args:
                folder (ProjectFolder): folder from which dataset needs to be removed
                dataset (ProjectDataSet): dataset that needs to be removed
                                            from the folder
        """
        if folder is not None and dataset is not None:
            LOGGER.debug("Removing dataset '%s' from folder '%s'" %
                         (dataset.name, folder.name))
            folder.datasets.remove(dataset)
            LOGGER.debug("Dataset removed from folder successfully")
        else:
            raise ValueError("Parameter 'dataset' and 'folder' can't be None")

    def remove_fact_from_folder(self, folder, fact):
        """ Removes an fact from the folder

            Args:
                folder (ProjectFolder): folder from which fact needs to be removed
                fact (ProjectFact): fact that needs to be removed
                                            from the folder
        """
        if folder is not None and fact is not None:
            LOGGER.debug("Removing fact '%s' from folder '%s'" %
                         (fact.name, folder.name))
            folder.facts.remove(fact)
            LOGGER.debug("Fact removed from folder successfully")
        else:
            raise ValueError("Parameter 'fact' and 'folder' can't be None")

    def remove_dimension_from_folder(self, folder, dimension):
        """ Removes an dimension from the folder

            Args:
                folder (ProjectFolder): folder from which dimension needs to be removed
                dimension (ProjectDimension): dimension that needs to be removed
                                            from the folder
        """
        if folder is not None and dimension is not None:
            LOGGER.debug("Removing dimension '%s' from folder '%s'" %
                         (dimension.name, folder.name))
            folder.dimensions.remove(dimension)
            LOGGER.debug("Dimension removed from folder successfully")
        else:
            raise ValueError("Parameter 'dimension' and 'folder' can't be None")

    def remove_metric_from_folder(self, folder, metric):
        """ Removes an metric from the folder

            Args:
                folder (ProjectFolder): folder from which metric needs to be removed
                metric (ProjectMetric): metric that needs to be removed
                                            from the folder
        """
        if folder is not None and metric is not None:
            LOGGER.debug("Removing metric '%s' from folder '%s'" %
                         (metric.name, folder.name))
            folder.metrices.remove(metric)
            LOGGER.debug("Metric removed from folder successfully")
        else:
            raise ValueError("Parameter 'metric' and 'folder' can't be None")

    def remove_property_from_file(self, file, property):
        """ Removes an property from the file

            Args:
                file (ProjectFile): file from which property needs to be removed
                property (Property): property that needs to be removed from the file
        """
        if file is not None and property is not None:
            LOGGER.debug("Removing property '%s' from file '%s'" %
                         (property.name, file.name))
            file.properties.remove(property)
            LOGGER.debug("Property removed from file successfully")
        else:
            raise ValueError("Parameter 'property' and 'file' can't be None")

    def remove_property_from_dataset(self, dataset, property):
        """ Removes an property from the dataset

            Args:
                dataset (ProjectDataSet): dataset from which property needs to be removed
                property (Property): property that needs to be removed from the dataset
        """
        if dataset is not None and property is not None:
            LOGGER.debug("Removing property '%s' from dataset '%s'" %
                         (property.name, dataset.name))
            dataset.properties.remove(property)
            LOGGER.debug("Property removed from dataset successfully")
        else:
            raise ValueError("Parameter 'property' and 'dataset' can't be None")

    def remove_property_from_fact(self, fact, property):
        """ Removes an property from the fact

            Args:
                fact (ProjectFact): fact from which property needs to be removed
                property (Property): property that needs to be removed from the fact
        """
        if fact is not None and property is not None:
            LOGGER.debug("Removing property '%s' from fact '%s'" %
                         (property.name, fact.name))
            fact.properties.remove(property)
            LOGGER.debug("Property removed from fact successfully")
        else:
            raise ValueError("Parameter 'property' and 'fact' can't be None")

    def remove_property_from_dimension(self, dimension, property):
        """ Removes an property from the dimension

            Args:
                dimension (ProjectFolder): dimension from which property needs
                                            to be removed
                property (Property): property that needs to be removed from the dimension
        """
        if dimension is not None and property is not None:
            LOGGER.debug("Removing property '%s' from dimension '%s'" %
                         (property.name, dimension.name))
            dimension.properties.remove(property)
            LOGGER.debug("Property removed from dimension successfully")
        else:
            raise ValueError("Parameter 'property' and 'dimension' can't be None")

    def remove_property_from_metric(self, metric, property):
        """ Removes an property from the metric

            Args:
                metric (ProjectMetric): metric from which property needs to be removed
                property (Property): property that needs to be removed from the metric
        """
        if metric is not None and property is not None:
            LOGGER.debug("Removing property '%s' from metric '%s'" %
                         (property.name, metric.name))
            metric.properties.remove(property)
            LOGGER.debug("Property removed from metric successfully")
        else:
            raise ValueError("Parameter 'property' and 'metric' can't be None")
