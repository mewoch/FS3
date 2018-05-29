# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:26:25 2018

@author: Tanner Lee
https://github.com/tleecsm
"""

import statistics
import numpy

# pylint: disable=too-few-public-methods
class FS3NumericalStatistics(object):
    """
    FS3NumericStatistics
    Class that contains all of the statistics calculated for numeric fields
    Contains an initialize function to run all calculations
    Overloads print function for debugging purposes
    """

    def __init__(self):
        """ Variable definitions """
        self.itemCount = None
        self.maxValue = None
        self.minValue = None
        self.meanValue = None
        self.medianValue = None
        self.sumValue = None
        self.stdDevValue = None
        self.coeffVarValue = None
        self.statCount = 0
        self.statName = ""

    def initialize(self, inputArray, percentileArray):
        """
        initialize
        Runs all numerical analysis
        Stores the output in class self.variables
        """
        self.itemCount = itemCount(inputArray)
        self.maxValue = maxValue(inputArray)
        self.minValue = minValue(inputArray)
        self.meanValue = meanValue(inputArray)
        self.medianValue = medianValue(inputArray)
        self.sumValue = sumValue(inputArray)
        self.stdDevValue = stdDevValue(inputArray)
        self.coeffVarValue = coeffVarValue(inputArray)
        self.percentiles = percentileValues(inputArray, percentileArray)
        self.statCount = 8 + len(self.percentiles)

        self.statName = ["Item Count",
                         "Max Value",
                         "Min Value",
                         "Mean Value",
                         "Median Value",
                         "Sum Value",
                         "Standard Deviation",
                         "Coefficient of Variation"]
        for percentileNumber in percentileArray:
            self.statName.append('Percentile: ' + str(percentileNumber) + '%')

    def __repr__(self):
        printString = 'Item Count :: ' + str(self.itemCount)
        printString += '\nMax Value :: ' + str(self.maxValue)
        printString += '\nMin Value :: ' + str(self.minValue)
        printString += '\nMean Value :: ' + str(self.meanValue)
        printString += '\nMedian Value :: ' + str(self.medianValue)
        printString += '\nSum Value :: ' + str(self.sumValue)
        printString += '\nStandard Deviation :: ' + str(self.stdDevValue)
        printString += '\nCoefficient of Variation :: '
        printString += str(self.coeffVarValue)
        return printString
    
class FS3CharacterStatistics(object):
    """
    FS3CharacterStatistics
    Class that contains all of the statistics calculated for numeric fields
    Contains an initialize function to run all calculations
    Overloads print function for debugging purposes
    """

    def __init__(self):
        """ Variable definitions """
        self.itemCount = None
        self.maxLength = None
        self.minLength = None
        self.meanLength = None
        self.medianLength = None
        self.sumLength = None
        self.stdDevLength = None
        self.coeffVarLength = None
        self.statCount = 0
        self.statName = ""

    def initialize(self, inputArray, percentileArray):
        """
        initialize
        Runs all numerical analysis
        Stores the output in class self.variables
        """
        #Start by converting the inputArray to a length array of the strings
        tempArray = []
        for string in inputArray:
            tempArray.append(len(string))
        inputArray = tempArray
        self.itemCount = itemCount(inputArray)
        self.maxLength = maxValue(inputArray)
        self.minLength = minValue(inputArray)
        self.meanLength = meanValue(inputArray)
        self.medianLength = medianValue(inputArray)
        self.sumLength = sumValue(inputArray)
        self.stdDevLength = stdDevValue(inputArray)
        self.coeffVarLength = coeffVarValue(inputArray)
        self.percentiles = percentileValues(inputArray, percentileArray)
        self.statCount = 8 + len(self.percentiles)

        self.statName = ["Item Count",
                         "Max Length",
                         "Min Length",
                         "Mean Length",
                         "Median Length",
                         "Sum Length",
                         "Standard Deviation (Length)",
                         "Coefficient of Variation (Length)"]
        for percentileNumber in percentileArray:
            self.statName.append('Percentile: ' + str(percentileNumber) + 
                                 '% (Length)')

    def __repr__(self):
        printString = 'Item Count :: ' + str(self.itemCount)
        printString += '\nMax Length :: ' + str(self.maxLength)
        printString += '\nMin Length :: ' + str(self.minLength)
        printString += '\nMean Length :: ' + str(self.meanLength)
        printString += '\nMedian Length :: ' + str(self.medianLength)
        printString += '\nSum Length :: ' + str(self.sumLength)
        printString += '\nStandard Deviation (Length) :: ' 
        printString += str(self.stdDevLength)
        printString += '\nCoefficient of Variation (Length) :: '
        printString += str(self.coeffVarLength)
        return printString

def removeEmptyCells(inputArray):
    """
    removeEmptyCells
    Function used to remove empty cells from a list
    This allows our calculations to remain accurate with incomplete data
    @param inputArray Array passed for calculation
    @return outputArray Array with the empty cells removed
    """
    outputArray = []
    for string in inputArray:
        if not string is None:
            outputArray.append(string)
    return outputArray

def itemCount(inputArray):
    """
    itemCount
    Function used to calculate the number of items in an array
    @param inputArray Array passed for calculation
    @return itemCountReturn The integer value returned by the calculation
    """
    itemCountReturn = len(inputArray)
    return itemCountReturn

def maxValue(inputArray):
    """
    maxValue
    Function used to calculate the maximum value of an array
    @param inputArray Array passed for calculation
    @return maxValueReturn The integer value returned by the calculation
    """
    maxValueReturn = max(inputArray)
    return maxValueReturn

def minValue(inputArray):
    """
    minValue
    Function used to calculate the minimum value of an array
    @param inputArray Array passed for calculation
    @return minValueReturn The integer value returned by the calculation
    """
    minValueReturn = min(inputArray)
    return minValueReturn

def meanValue(inputArray):
    """
    meanValue
    Function used to calculate the mean value of an array
    @param inputArray Array passed for calculation
    @return meanValueReturn The integer value returned by the calculation
    """
    meanValueReturn = sum(inputArray)/float(len(inputArray))
    return meanValueReturn

def medianValue(inputArray):
    """
    medianValue
    Function used to calculate the median value of an array
    @param inputArray Array passed for calculation
    @return medianValueReturn The integer value returned by the calculation
    """
    medianValueReturn = statistics.median(inputArray)
    return medianValueReturn

def sumValue(inputArray):
    """
    sumValue
    Function used to calculate the sum value of an array
    @param inputArray Array passed for calculation
    @return sumValueReturn The integer value returned by the calculation
    """
    sumValueReturn = sum(inputArray)
    return sumValueReturn

def stdDevValue(inputArray):
    """
    stdDevValue
    Function used to calculate the Standard Deviation of an array
    @param inputArray Array passed for calculation
    @return stdDevValueReturn The integer value returned by the calculation
    """
    stdDevValueReturn = statistics.stdev(inputArray)
    return stdDevValueReturn

def coeffVarValue(inputArray):
    """
    coeffVarValue
    Function used to calculate the coefficient of variation of an array
    @param inputArray Array passed for calculation
    @return coeffVarReturn The integer value returned by the calculation
    """
    coeffVarReturn = statistics.variance(inputArray)
    return coeffVarReturn

def percentileValues(inputArray, percentileArray):
    """
    percentileValues
    Function used to calculate the percentiles of a given array
    @param inputArray Array passed for calculation
    @param percentileArray Array containing user selected percentiles
    @return percDict Dictionary of percentiles to values
    """
    percentiles = []
    for p in percentileArray:
        val = numpy.percentile(inputArray, p)
        percentiles.append(val)
    return percentiles
