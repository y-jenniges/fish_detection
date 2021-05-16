import enum
import os
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui
import Helpers

# constants for initalizing data models
IMAGE_REMARKS= ["", "Low turbidity", "Medium turbidity", "High turbidity", 
                "Wrong illumination", "Without flashlight"]

ANIMAL_REMARKS = ["", "Not determined",  "Animal incomplete"]

GROUP_ICON_LIST = [":/animal_markings/animal_markings/square_blue.png", 
                   ":/animal_markings/animal_markings/square_red.png", 
                   ":/animal_markings/animal_markings/square_orange.png", 
                   ":/animal_markings/animal_markings/square_black.png", 
                   ":/animal_markings/animal_markings/square_gray.png"]


class AnimalGroup(enum.Enum):
    """ 
    Enum for possible animal groups.
    """   
    FISH = 1,  
    CRUSTACEA = 2, 
    CHAETOGNATHA = 3, 
    JELLYFISH = 4, 
    UNIDENTIFIED = 5


class AnimalSpecies(enum.Enum):
    """
    Enum for initally possible animal species.
    """
    
    UNIDENTIFIED = 0
    
    
class Models():
    """
    This class wraps up all data models necessary for the application.
    
    Attributes
    ----------
    model_group : QStandardItemModel
        Model for the possible groups an animal can belong to
    model_species : QStandardItemModel
        Model for the possible species an animal can belong to
    model_animal_remarks : QStandardItemModel
        Model for the possible remarks for animals
    model_image_remarks : QStandardItemModel
        Model for the possible remarks for images
    model_animals : TableModel
        Model for the underlying data, i.e. the table containing information
        about animals on images
    """
    
    def __init__ (self):  
        # data model for the animal groups
        self.model_group = QtGui.QStandardItemModel()
        index = 0
        for group in AnimalGroup:
            # icon showing the colour of the respective group
            icon = QtGui.QIcon(GROUP_ICON_LIST[index]) 
            item = QtGui.QStandardItem(str(group.name.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            item.setIcon(icon)
            self.model_group.appendRow(item)
            index += 1

        # data model for the animal species
        self._dict_species = [] # dict to map title and image path
        self.model_species = QtGui.QStandardItemModel()
        for species in AnimalSpecies:
            icon = QtGui.QIcon()
            item = QtGui.QStandardItem(str(species.name.title()))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            item.setIcon(icon)
            self._dict_species.append({"title": str(species.name.title()), 
                                       "image_path": ""})
            self.model_species.appendRow(item)
        
        # data model for animal remarks
        self.model_animal_remarks = QtGui.QStandardItemModel()
        for remark in ANIMAL_REMARKS:
            item = QtGui.QStandardItem(str(remark))
            item.setTextAlignment(QtCore.Qt.AlignRight)
            self.model_animal_remarks.appendRow(item)
            
        # data model for the image remarks
        self.model_image_remarks = QtGui.QStandardItemModel()
        for remark in IMAGE_REMARKS:
            item = QtGui.QStandardItem(str(remark))
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            self.model_image_remarks.appendRow(item)
            
        # data model for all animal information
        self.model_animals = TableModel(None)
    
    def addImageRemark(self, remark):
        """
        Add a remark to the image remark model.

        Parameters
        ----------
        remark : string
            Remark to add
        """
        if remark is not None and str(remark).lower() != "nan":
            same_remarks = self.model_image_remarks.findItems(str(remark))
            
            # add the remark if it is not already in the model
            if len(same_remarks) == 0:
                item = QtGui.QStandardItem(str(remark))
                item.setTextAlignment(QtCore.Qt.AlignLeft)
                self.model_image_remarks.appendRow(item)
        
    def addAnimalRemark(self, remark):
        """
        Add a remark to the animal remark model.

        Parameters
        ----------
        remark : string
            Remark to add
        """
        if remark is not None and str(remark).lower() != "nan":
            same_remarks = self.model_animal_remarks.findItems(str(remark))
            
            # add the remark if it is not already in the model
            if len(same_remarks) == 0:
                item = QtGui.QStandardItem(str(remark))
                item.setTextAlignment(QtCore.Qt.AlignRight)
                self.model_animal_remarks.appendRow(item)

    def addSpecies(self, species, image_path=""):
        """
        Add a species to the species model.

        Parameters
        ----------
        species : string
            Species to add
        image_path: string
            Path to the image showing the species. Default is ""
        """
        if species is not None and str(species).lower() != "nan" and species != "":
            same_species = self.model_species.findItems(str(species))
            
            # add species if it is not already in the model
            if len(same_species) == 0:     
                title = str(species)
                item = QtGui.QStandardItem(title)
                item.setTextAlignment(QtCore.Qt.AlignRight)
                icon = QtGui.QIcon(image_path)
                item.setIcon(icon)
                self._dict_species.append({"title": title, 
                                           "image_path": image_path})
                self.model_species.appendRow(item)
            else:
                # if there are multiple entries with same title, 
                # add the one wich has an image
                if same_species[0].icon().isNull() and image_path is not None and image_path != "":
                    row = self.model_species.indexFromItem(same_species[0]).row()
                    self.removeSpecies(row)
                    self.addSpecies(species, image_path)
                    
    def removeSpecies(self, row):
        """
        Removes a row from the species model.

        Parameters
        ----------
        row : int
            Row to remove
        """
        title = self.model_species.item(row).text()

        # only remove species if no animal in the table has this species
        if (self.model_animals.data["species"] == title).any():
            text = "Error: Cannot remove species"
            information = "The species to be deleted is assigned to at least \
            one animal. Hence, it cannot be removed."
            window_title = "Species not removable"
            Helpers.displayErrorMsg(text, information, window_title)
            return

        # update dictionary and model
        self._dict_species = [i for i in self._dict_species 
                              if not (i['title'] == title)] 
        self.model_species.removeRow(row)
                
# --- functions for saving and restoring options ---------------------------- # 
    def saveCurrentValues(self, settings):
        """
        Save current values, i.e. the species dictionary mapping species names
        to their image paths.

        Parameters
        ----------
        settings : QSettings
            Settings variable to store the values in
        """
        settings.setValue("dictSpecies", self._dict_species)       

    def restoreValues(self, settings):
        """
        Restore saved values, i.e. the species dictionary mapping species names
        to their image paths.

        Parameters
        ----------
        settings : QSettings
            Settings variable to restore the values from
        """
        species = settings.value("dictSpecies")
        if species is not None:
            self._dict_species = species
            for i in self._dict_species:
                self.addSpecies(i["title"], i["image_path"])
    
    
class TableModel(QtCore.QAbstractTableModel): 
    """
    A custom data model for tables in the pandas DataFrame format.
    
    Adapted from: 
    https://stackoverflow.com/questions/17697352/pyqt-implement-a-qabstracttablemodel-for-display-in-qtableview
    (last access: 07.09.2020)
    
    Attributes
    ----------
    data : DataFrame
        The current data table
    """
    
    def __init__(self, data, parent=None):
        """
        Init function. It sets the data of the model.

        Parameters
        ----------
        data : DataFrame
            The data to initalize the model with
        parent : optional
            The default is None
        """
        super(TableModel, self).__init__()
        self.update(data)

    def update(self, new_data):
        """
        Function to update the complete data to a new table.
        
        Parameters
        ----------
        new_data : DataFrame
            Data table to override the old data
        """
        self.data = new_data
        
        if self.data is not None:
            # make sure that the remarks columns are string
            self.data["object_remarks"] = self.data["object_remarks"].astype(np.unicode_)
            self.data["image_remarks"] = self.data["image_remarks"].astype(np.unicode_)
            
            # make sure, the remarks columns have empty strings instead of nan
            self.data["object_remarks"] = self.data["object_remarks"].str.lower().replace("nan", "")
            self.data["image_remarks"] = self.data["image_remarks"].str.lower().replace("nan", "")
        
        # adapt layout according to new table structure
        self.layoutChanged.emit() 

    def rowCount(self, parent=QtCore.QModelIndex()):
        """
        Implements the function of abstract base class. 
        It returns the number of rows.

        Parameters
        ----------
        parent : optional
            The default is QtCore.QModelIndex()

        Returns
        -------
        int
            Number of rows
        """
        if self.data is not None:
            return len(self.data.index) 
        else:
            return 0

    def columnCount(self, parent=QtCore.QModelIndex()):
        """
        Implements the function of abstract base class. 
        It returns the number of columns.

        Parameters
        ----------
        parent : optional
            The default is QtCore.QModelIndex()

        Returns
        -------
        int
            Number of columns
        """
        if self.data is not None:
            return len(self.data.columns.values) 
        else:
            return 0

    def data(self, index, role=QtCore.Qt.DisplayRole):
        """
        Returns the data (for the given role) at a specified index.

        Parameters
        ----------
        index : QModelIndex
            Index of the data to be obtained
        role : int, optional
            The default is QtCore.Qt.DisplayRole

        Returns
        -------
        object
            Requested data chunk
        """
        if role == QtCore.Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return '{0}'.format(self.data.iat[i, j])
        else:
            return QtCore.QVariant()
    
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        """
        Implements the function of abstract base class. 
        It returns the data for the table header, i.e. the column names, for
        the given role, section and orientation.

        Parameters
        ----------
        section : int
            Column/row number for horizontal/vertical headers
        orientation : Orientation
            The orientation of the table, i.e. horizontal or vertical
        role : int, optional
            The default is QtCore.Qt.DisplayRole

        Returns
        -------
        columns : list<string>
            List of the column/row names (depending on the orienation)
        """
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                columns = str(self.data.columns[section])

            elif orientation == QtCore.Qt.Vertical:
                columns = str(self.data.index[section])
            else:
                columns = QtCore.QAbstractTableModel.headerData(
                    self, section, orientation, role) 
        else:
            columns = QtCore.QAbstractTableModel.headerData(
                self, section, orientation, role) 

        return columns
    
    def insertRows(self, row, count, animals, image_path, image_remark, 
                   experiment_id, user_id, image_spec, parent=QtCore.QModelIndex()):
        """
        Inserts count rows into the dataframe before the given row. The rows
        are filled using the image path, remarks, experiment ID, user ID 
        and with the data from the list of animals.

        Parameters
        ----------
        row : int
            Insert new rows before this one
        count : int
            Number of rows to be inserted
        animals : list<Animal>
            Animal information to be stored in the CSV file
        image_path : string
            Path to the current image
        image_remark : string
            Remark for the current image
        experiment_id : string
            ID of the experiment the current image belongs to
        user_id : string
            ID of the currently working user
        parent : TYPE, optional
            Parent object. The default is QtCore.QModelIndex().
        image_spec: list of strings
            Specifies if the animals are drawn on left or right image. Use "L" 
            for left image, "R" for right image
            
        Returns
        -------
        bool
            Returns True when rows are inserted
        """
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count - 1)
        for i in range(count):
            new_row = self._create_row(animals[i], image_path, image_remark, 
                                       experiment_id, user_id, image_spec[i])
            self.data = self.data.append(new_row)    
        self.endInsertRows()

        # sort data        
        self.sort("file_id")
        return True

    def insertDfRows(self, row, count, df, image_path, image_remark, 
                   experiment_id, user_id, parent=QtCore.QModelIndex()):
        """
        Inserts count rows into the dataframe before the given row. The rows
        are filled using the image path, remarks, experiment ID, user ID 
        and with the data from a dataframe.

        Parameters
        ----------
        row : int
            insert new rows before this one
        count : int
            number of rows to be inserted
        df : DataFrame
            animal information to be stored in the CSV file
        image_path : string
            path to the current image
        image_remark : string
            remark for the current image
        experiment_id : string
            ID of the experiment the current image belongs to
        user_id : string
            ID of the currently working user
        parent : TYPE, optional
            Parent object. The default is QtCore.QModelIndex().

        Returns
        -------
        bool
            Returns True when rows are inserted
        """
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count - 1)
        for i in range(count):
            # check if columns are a subset of desired columns
            if df.columns.isin(self.data.columns).all():
                self.data = self.data.append(df.iloc[i], ignore_index=True)    
        self.endInsertRows()

        # sort data        
        self.sort("file_id")
        return True
    
    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        """
        Removes count rows starting with the given row.

        Parameters
        ----------
        row : int
            First row to be removed
        count : int
            Number of rows to be removed
        parent : optional
            The default is QtCore.QModelIndex()
        """
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + count - 1)
        for i in range(count):
            self.data = self.data.drop(self.data.index[row])
        self.endRemoveRows()
        return True

    def sort(self, column, order=QtCore.Qt.AscendingOrder):
        """
        Sorts the data according to column in the given order.

        Parameters
        ----------
        column : string
            Column name
        order: SortOrder, optional
            Order to sort by. The default it AscendingOrder.
        """
        asc = True if order==QtCore.Qt.AscendingOrder else False
        self.data = self.data.sort_values(by=[column], ascending=asc)
        
    def exportToCsv(self, output_dir, filename, file_id=None):
        """
        Exports the data table to a CSV file in the specified output directory. 
        If the outfile already exists, only the current image is 
        updated in the file. If the result file does not exists and/or the 
        model data is None, create new file/empty dataframe.

        Parameters
        ----------
        output_dir : string
            Path to the output directory
        filename : string
            Name of the output file.
        file_id : string, optional
            ID of the current image. The default is None.
        """
        # create the output file path
        path = os.path.join(output_dir, filename)
        
        # if the path exists and a file_id is given, only replace the current
        # image data
        if os.path.isfile(path) and file_id is not None:
            current_output = pd.read_csv(path, sep=",")
            
            if self.data is not None:
                # drop old rows of current image
                current_output.drop(current_output[
                current_output["file_id"] == file_id].index, inplace=True)
            
                # insert new rows of current image
                current_output = current_output.append(
                    self.data[self.data["file_id"] == file_id])
            
                # sort according to file_id
                current_output.sort_values(
                    by="file_id", ignore_index=True, inplace=True)
            
                # save the new CSV file
                try:
                    current_output.to_csv(path, sep=",", index=False)
                except:
                    print("Models: Could not write CSV file. Please close all open tables.")
            else:
                columns = []
                self.data = pd.DataFrame(columns=columns)
        else:
            # if there is no data, create empty dataframe
            if self.data is None:
                self.data = pd.DataFrame(columns=self.getColumns())
            
            # write a completely new file (if a path was selected)
            try:
                if path != "":
                    self.data.to_csv(path, sep=",", index=False)
            except:
                print("Models: Could not write CSV file. Please close all open tables.")
    
    def getColumns(self):
        """ Returns a list of the column names. """
        return ["file_id", "object_remarks", "group", "species", 
                "LX1", "LY1", "LX2", "LY2", "LX3", "LY3", "LX4", "LY4", 
                "RX1", "RY1", "RX2", "RY2", "RX3", "RY3", "RX4", "RY4",
                "length", "height", "image_remarks", "status",
                "manually_corrected", "experiment_id", "user_id"]
    
    def loadFile(self, path):
        """ Reads data from a file and updates the data model with it. """
        if os.path.isfile(path):
            data = pd.read_csv(path, sep=",")
            if (data.columns == self.getColumns()).all():
                self.update(data)
            else:
                print("TableModel: Cannot load file due to incorrect columns.")
                
    def isEmpty(self):
        """ Displays an error message if data model is empty. """
        if self.data is None:
            Helpers.displayErrorMsg("No output directory or file", 
                            "Please select an output directory on data page.", 
                            "Error")
            return True
        else:
            return False
    
    def _create_row(self, animal, image_path, image_remark, experiment_id, 
                    user_id, image_spec="L"): 
        """
        Creates a new row for the dataframe given the arguments of this 
        function.

        Parameters
        ----------
        animal : Animal
            Animal described in the new dataframe row
        image_path : string
            Path to the image on which the animal is found
        image_remark : string
            Remark to the image on which the animal is found
        experiment_id : string
            ID of the experiment during which the image was created
        user_id : string
            ID of the user who worked on the given image
        image_spec: string
            Specifies if the animal is drawn on left or right image. Default
            is "L" for left image (use "R" for right image)

        Returns
        -------
        new_row: DataFrame
            New row for the data
        """
        # get file ID
        file_id = os.path.basename(image_path).rstrip(".jpg").rstrip(".png").rstrip("_L").rstrip("_R")
        
        # get animal group
        if isinstance(animal.group, AnimalGroup):
            group = animal.group.name.title()
        else:
            group = animal.group.title()
            
        # get animal species
        if isinstance(animal.species, AnimalSpecies):
            species = animal.species.name.title()
        else:
            species = animal.species.title()

        # create a new row (depending on whether the animal is on the left or 
        # right image)
        if image_spec == "L":
            new_row = pd.DataFrame({"file_id": file_id, 
                                    "object_remarks": animal.remark, 
                                    "group": group, 
                                    "species": species,
                                    "LX1": animal.original_pos_head.x(),
                                    "LY1": animal.original_pos_head.y(),
                                    "LX2": animal.original_pos_tail.x(),
                                    "LY2": animal.original_pos_tail.y(),
                                    "LX3": -1, 
                                    "LY3": -1,
                                    "LX4": -1,
                                    "LY4": -1,
                                    "RX1": -1,
                                    "RY1": -1,
                                    "RX2": -1,
                                    "RY2": -1,
                                    "RX3": -1, 
                                    "RY3": -1,
                                    "RX4": -1,
                                    "RY4": -1,
                                    "length": -1,
                                    "height": -1,
                                    "image_remarks": image_remark,
                                    "status": "checked",
                                    "manually_corrected": "True",
                                    "experiment_id": experiment_id,
                                    "user_id": user_id
                                    }, index=[animal.row_index])
        elif image_spec=="R":
            new_row = pd.DataFrame({"file_id": file_id, 
                                    "object_remarks": animal.remark, 
                                    "group": group, 
                                    "species": species,
                                    "LX1": -1,
                                    "LY1": -1,
                                    "LX2": -1,
                                    "LY2": -1,
                                    "LX3": -1, 
                                    "LY3": -1,
                                    "LX4": -1,
                                    "LY4": -1,
                                    "RX1": animal.original_pos_head.x(),
                                    "RY1": animal.original_pos_head.y(),
                                    "RX2": animal.original_pos_tail.x(),
                                    "RY2": animal.original_pos_tail.y(),
                                    "RX3": -1, 
                                    "RY3": -1,
                                    "RX4": -1,
                                    "RY4": -1,
                                    "length": -1,
                                    "height": -1,
                                    "image_remarks": image_remark,
                                    "status": "checked",
                                    "manually_corrected": "True",
                                    "experiment_id": experiment_id,
                                    "user_id": user_id
                                    }, index=[animal.row_index])        
        else: 
            print("TableModel: Could not insert current animal due to invalid \
                  image specification. Either use 'L' or 'R'.")
                  
        return new_row