# -*- coding: utf-8 -*-
"""
Created on Tue May 15 11:12:02 2018

@author: Tanner Lee
"""
from __future__ import print_function

import os
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem

from .layerFieldGetter import LayerFieldGetter
from .fs3Stats import FS3NumericalStatistics, removeEmptyCells

# pylint: disable=fixme

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'fs3.ui'))

class FS3MainWindow(QMainWindow, FORM_CLASS):
    """
    FS3MainWindow
    Handles the creation and display of the window.
    Makes use of the fs3.ui QT ui file.
    """
    def __init__(self, parent=None):
        super(FS3MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.mainWindowSplitter.setStretchFactor(1, 10)
        self.setWindowTitle('FS3 -- FieldStats3')

        self.fieldGetterInst = LayerFieldGetter()
        self.currentLayer = None
        self.fields = None
        self.numericalStatistics = None
        ### Tabs
        # Data Table
        self.dataTableLayout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        self.statisticLayout = QVBoxLayout()
        self.statisticTable = QTableWidget()


        #Refresh for the connecters
        self.refresh()

        ### pyqtSlot connectors (BUTTONS)
        # Percentile
        self.percentile25.clicked.connect(self.percentile25Update)
        self.percentile10.clicked.connect(self.percentile10Update)
        self.percentile5.clicked.connect(self.percentile5Update)
        self.percentileHighEnd.clicked.connect(self.percentileHighEndUpdate)
        # Limit to Selected
        self.limitToSelected.stateChanged.connect(self.handleLimitSelected)
        # Next/Prev
        self.nextButton.clicked.connect(self.setNextField)
        self.previousButton.clicked.connect(self.setPrevField)

        ### Layer and Field Combo Boxes
        self.selectLayerComboBox.currentIndexChanged \
                        .connect(self.refreshFields)
        # TODO if this is a QListWidget or QListView we will be able to select multiple fields
        self.selectFieldComboBox.currentIndexChanged \
                        .connect(self.refreshTable)


    def refresh(self):
        """
        Reload data
        """
        self.refreshLayers()
        self.refreshFields()
        self.refreshTable()


    ### Fill LineEdit with percentile numbers when the buttons are pressed
    @pyqtSlot()
    def percentile25Update(self):
        self.percentilesLineEdit.setText("25, 50, 75, 100")

    @pyqtSlot()
    def percentile10Update(self):
        percentile10Str = ", ".join(str(x * 10) for x in range(1, 11))
        self.percentilesLineEdit.setText(percentile10Str)

    @pyqtSlot()
    def percentile5Update(self):
        percentile5Str = ", ".join(str(x * 5) for x in range(1, 21))
        self.percentilesLineEdit.setText(percentile5Str)

    @pyqtSlot()
    def percentileHighEndUpdate(self):
        self.percentilesLineEdit.setText("50, 80, 95")


    ### Limit to Selected Checkbox
    @pyqtSlot()
    def handleLimitSelected(self):
        #If there are selected layers in QGIS
        if not self.currentLayer.getSelectedFeatures().isClosed():
            #Update the table
            self.refreshTable()


    ### Next/Previous
    @pyqtSlot()
    def setNextField(self):
        """
        Method implements next field when Next button is clicked
        """
        index = self.selectFieldComboBox.currentIndex()
        try:
            index = (index + 1) % self.selectFieldComboBox.count()
        except ZeroDivisionError:
            # TODO not sure what it should do here...
            index = 0
        self.selectFieldComboBox.setCurrentIndex(index)

    @pyqtSlot()
    def setPrevField(self):
        """
        Method implements pevious field when Previous button is clicked
        """
        index = self.selectFieldComboBox.currentIndex()
        try:
            index = (index - 1) % self.selectFieldComboBox.count()
        except ZeroDivisionError:
            index = 0
        self.selectFieldComboBox.setCurrentIndex(index)

    def refreshLayers(self):
        """
        Reload the layers coboBox with the current content of the layers list
        """
        self.selectLayerComboBox.clear()

        layers = self.fieldGetterInst.getVectorLayers()
        self.selectLayerComboBox.insertItems(0, layers)

    @pyqtSlot()
    def refreshFields(self):
        """
        Reload the fields coboBox with the current content of the field lists
        """
        self.selectFieldComboBox.clear()

        layer = self.fieldGetterInst.getSingleLayer \
                (self.selectLayerComboBox.currentText())
        if layer != None:
            self.currentLayer = layer
            self.fields = self.currentLayer.fields()
            self.selectFieldComboBox.insertItem(0, "All")
            self.selectFieldComboBox.insertItems \
                (1, self.fieldGetterInst.getAllFields(layer))

    @pyqtSlot()
    def refreshTable(self):
        """
        Refresh the table content with coresponding Layer & field selection
        """
        self.tableWidget.clear()
        self.tableWidget.setSortingEnabled(False)

        # Get selected field
        field = self.selectFieldComboBox.currentText()
        # If the field is not set yet (Layer was swapped)
        # Return until the refresh is ready
        if field == '':
            return
        if self.currentLayer:
            if self.limitToSelected.isChecked():
                features = self.currentLayer.getSelectedFeatures()
            else:
                features = self.currentLayer.getFeatures()
            # Determine length
            total = 0
            for feature in features:
                total += 1

            self.tableWidget.setRowCount(total)

            row = 0
            if self.limitToSelected.isChecked():
                features = self.currentLayer.getSelectedFeatures()
            else:
                features = self.currentLayer.getFeatures()
            names = []

            #Create an index and a list to track Column content
            fieldIndex = 2
            columnValues = []


            # for each row
            for feature in features:
                if field == 'All':
                    attributes = feature.attributes()
                    self.tableWidget.setColumnCount(len(attributes))
                    col = 0

                    # for each column value
                    for attribute in attributes:
                        self.tableWidget.setItem(row, col, MyTableWidgetItem(str(attribute)))
                        col += 1

                else:
                    self.tableWidget.setColumnCount(1) # TODO not 1 if we are selecting multiple...
                    fieldIndex = feature.fieldNameIndex(field)
                    columnValues.append(feature.attributes()[fieldIndex])
                    self.tableWidget.setItem(row, 0, MyTableWidgetItem(str(feature.attributes()[fieldIndex])))

                row += 1

                # Add
                try:
                    # Not all data has a "name"
                    # TODO look through other datasets and find what else this might be called
                    names.append(feature["name"])
                except KeyError:
                    names.append(str(row))

            if field == 'All' or field == '':
                fields = self.fieldGetterInst.getAllFields(self.currentLayer)
                self.tableWidget.setHorizontalHeaderLabels(fields)
            else:
                print('field : ' + field)
                self.tableWidget.setHorizontalHeaderLabels([field])
                if self.fields.at(fieldIndex).isNumeric():
                    print(self.fields.at(fieldIndex).isNumeric())
                    self.createStatistics(columnValues)
                    self.refreshStatistics(field)
                else:
                    #TODO: remove when char statistic method is DONE
                    self.statisticTable.clear()
            self.tableWidget.setVerticalHeaderLabels(names)

        else:
            # TODO display this in the gui or a pop up
            print("Please select a layer to look at it's data")

        self.dataTableLayout.addWidget(self.tableWidget)
        self.dataTab.setLayout(self.dataTableLayout)


    def refreshStatistics(self, field):
        """
        refreshStatistics
        Method that updates the statistic table
        """
        self.statisticTable.clear()
        self.statisticTable.setRowCount(self.numericalStatistics.statCount)
        self.statisticTable.setColumnCount(1) # TODO not 1 if we are selecting multiple...
        self.statisticTable.setVerticalHeaderLabels(self.numericalStatistics.statName)
        self.statisticTable.setHorizontalHeaderLabels([field])

        self.statisticTable.setItem(0, 0, QTableWidgetItem(str(self.numericalStatistics.itemCount)))
        self.statisticTable.setItem(1, 0, QTableWidgetItem(str(self.numericalStatistics.maxValue)))
        self.statisticTable.setItem(2, 0, QTableWidgetItem(str(self.numericalStatistics.minValue)))
        self.statisticTable.setItem(3, 0, QTableWidgetItem(str(self.numericalStatistics.meanValue)))
        self.statisticTable.setItem(4, 0, QTableWidgetItem(str(self.numericalStatistics.medianValue)))
        self.statisticTable.setItem(5, 0, QTableWidgetItem(str(self.numericalStatistics.sumValue)))
        self.statisticTable.setItem(6, 0, QTableWidgetItem(str(self.numericalStatistics.stdDevValue)))
        self.statisticTable.setItem(7, 0, QTableWidgetItem(str(self.numericalStatistics.coeffVarValue)))

        #self.statisticTable.move(0,0)
        self.statisticLayout.addWidget(self.statisticTable)
        self.statisticsTab.setLayout(self.statisticLayout)
        self.tableWidget.setSortingEnabled(True)

    def sortVerticalHeaders(self):
        """
        Will reorder the vertical headers to match
        their sorted data
        """
        pass
        # TODO how do i do this without caching all the data

        # for item in sorted column
            # find it's feature
            # find the feature's name
            # append to names
        # self.tableWidget.setVerticalHeaderLabels(names)

    def createStatistics(self, inputArray):
        """
        createStatistics
        Methods that instantiates both Statistics classes and initializes them
        """
        emptyCellsRemoved = removeEmptyCells(inputArray)
        self.numericalStatistics = FS3NumericalStatistics()
        self.numericalStatistics.initialize(emptyCellsRemoved)


class MyTableWidgetItem(QTableWidgetItem):
    """
    Use to overload < operator so that the table will
    sort both numerically and then alphanumerically where appropriate
    """
    def __init__(self, parent=None):
        super(MyTableWidgetItem, self).__init__(parent)

    def __lt__(self, other):
        try:
            return float(self.text()) < float(other.text())
        except ValueError:
            return self.text() < other.text()
