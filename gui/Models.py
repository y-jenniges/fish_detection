import enum
import os
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtGui
import Helpers
from Predicter import Predicter

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
        model for the possible groups an animal can belong to
    model_species : QStandardItemModel
        model for the possible species an animal can belong to
    model_animal_remarks : QStandardItemModel
        model for the possible reamrks for animals
    model_image_remarks : QStandardItemModel
        model for the possible remarks for images
    model_animals : TableModel
        model for the underlying data, i.e. the table containing information
        about animals on images

    Methods
    -------
    addImageRemark(remark):
        add a renark to the image remark model
    addAnimalRemark(remark):
        add a remark to the animal remark model
    addSpecies(species, page_settings):
        add a species to the species model and adapt the species list on the
        settings page
    removeSpecies(row):
        removes a row from the species model
    saveCurrentValues(settings):
        save some values in settings for restorage on program restart
    restoreValues(settings):
        restore the previously saved settings
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
            remark to add
        """
        if remark is not None and str(remark) != "nan":
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
            remark to add
        """
        if remark is not None and str(remark) != "nan":
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
            species to add
        image_path: string
            path to the image showing the species. Default is ""
        """
        if species is not None and str(species) != "nan":
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
                if same_species[0].icon() is None and image_path is not None:
                    self.removeSpecies(self.model_species.indexFromIcon(
                        same_species[0]))
                    self.addSpecies(species, image_path)
                    
                
    def removeSpecies(self, row):
        """
        Removes a row from the species model.

        Parameters
        ----------
        row : int
            row to remove
        """
        title = self.model_species.item(row).text()

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
            settings variable to store the values in
        """
        settings.setValue("dictSpecies", self._dict_species)       

    def restoreValues(self, settings):
        """
        Restore saved values, i.e. the species dictionary mapping species names
        to their image paths.

        Parameters
        ----------
        settings : QSettings
            settings variable to restore the values from
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
        the current data table

    Methods
    -------
    update(new_data):
        sets the data to new_data
    rowCount(parent=QModelIndex()):
        returns the number of rows of the current data table
    columnCount(parent=QModelIndex()):
        returns the number of columns of the current data table
    data(index, role=DisplayRole):
        returns data at index for the given role
    headerData(section, orientation, role=DisplayRole):
        returns the names in the header of the table
    insertRows(row, count, animals, image_path, image_remark, experiment_id, 
               user_id, parent=QModelIndex()):
        inserts count rows into the table before the given row
    removeRows(row, count, parent=QModelIndex()):
        removes count rows from the table starting with the given row
    sort(column, order=AscendingOrder):
        sorts the data by column in the given order
    exportToCsv(output_dir, file_id=None, out_file_path=None):
        exports the data to a CSV file
    """
    
    def __init__(self, data, parent=None):
        """
        Init function. It sets the data of the model.

        Parameters
        ----------
        data : DataFrame
            the data to initalize the model with
        parent : optional
            the default is None
        """
        super(TableModel, self).__init__()
        self.data = data

    def update(self, new_data):
        """
        Function to update the complete data to a new table.
        
        Parameters
        ----------
        new_data : DataFrame
            data table to override the old data
        """
        self.data = new_data
        
        # adapt layout according to new table structure
        self.layoutChanged.emit() 

    def rowCount(self, parent=QtCore.QModelIndex()):
        """
        Implements the function of abstract base class. 
        It returns the number of rows.

        Parameters
        ----------
        parent : optional
            the default is QtCore.QModelIndex()

        Returns
        -------
        int
            number of rows
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
            the default is QtCore.QModelIndex()

        Returns
        -------
        int
            number of columns
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
            index of the data to be obtained
        role : int, optional
            the default is QtCore.Qt.DisplayRole

        Returns
        -------
        object
            requested data chunk
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
            column/row number for horizontal/vertical headers
        orientation : Orientation
            the orientation of the table, i.e. horizontal or vertical
        role : int, optional
            the default is QtCore.Qt.DisplayRole

        Returns
        -------
        columns : list<string>
            list of the column/row names (depending on the orienation)
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
                   experiment_id, user_id, parent=QtCore.QModelIndex()):
        """
        Inserts count rows into the dataframe before the given row. The rows
        are filled using the image path, remarks, experiment ID, user ID 
        and with the data from the list of animals.

        Parameters
        ----------
        row : int
            insert new rows before this one
        count : int
            number of rows to be inserted
        animals : list<Animal>
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
            DESCRIPTION. The default is QtCore.QModelIndex().

        Returns
        -------
        bool
            returns True when rows are inserted
        """
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count - 1)
        for i in range(count):
            new_row = self._create_row(animals[i], image_path, image_remark, 
                                       experiment_id, user_id)
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
            DESCRIPTION. The default is QtCore.QModelIndex().

        Returns
        -------
        bool
            returns True when rows are inserted
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
            first row to be removed
        count : int
            number of rows to be removed
        parent : optional
            the default is QtCore.QModelIndex()
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
            column name
        order: SortOrder, optional
            order to sort by. The default it AscendingOrder.
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
            path to the output directory
        filename : string
            name of the output file.
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
                current_output.to_csv(path, sep=",", index=False)
            else:
                columns = []
                self.data = pd.DataFrame(columns=columns)
        else:
            # if there is no data, create empty dataframe
            if self.data is None:
                self.data = pd.DataFrame(columns=self.getColumns())
            
            # write a completely new file
            self.data.to_csv(path, sep=",", index=False)
    
    def getColumns(self):
        return ["file_id", "object_remarks", "group", "species", 
                "LX1", "LY1", "LX2", "LY2", "LX3", "LY3", "LX4", "LY4", 
                "RX1", "RY1", "RX2", "RY2", "RX3", "RY3", "RX4", "RY4",
                "length", "height", "image_remarks", "status",
                "manually_corrected", "experiment_id", "user_id"]
    
    def loadFile(self, path):
        if os.path.isfile(path):
            data = pd.read_csv(path, sep=",")
            if (data.columns == self.getColumns()).all():
                self.update(data)
            else:
                print("TableModel: Cannot load file due to incorrect columns.")
                
    def isEmpty(self):
        if self.data is None:
            Helpers.displayErrorMsg("No output directory or file", 
                            "Please select an output directory on data page.", 
                            "Error")
            return True
        else:
            return False
    
    def _create_row(self, animal, image_path, image_remark, experiment_id, 
                    user_id): 
        """
        Creates a new row for the dataframe given the arguments of this 
        function.

        Parameters
        ----------
        animal : Animal
            animal described in the new dataframe row
        image_path : string
            path to the image on which the animal is found
        image_remark : string
            remark to the image on which the animal is found
        experiment_id : string
            ID of the experiment during which the image was created
        user_id : string
            ID of the user who worked on the given image

        Returns
        -------
        new_row: DataFrame
            new row for the data
        """
        # get file ID
        file_id = os.path.basename(image_path)[:-6]
        
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
                                "manually_corrected": "yes",
                                "experiment_id": experiment_id,
                                "user_id": user_id
                                }, index=[animal.row_index])
        return new_row