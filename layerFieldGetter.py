import locale

#from PyQt4.QtCore import *
#from PyQt4.QtGui import *
from PyQt4.QtCore import QVariant

from qgis.core import *
from qgis.gui import *

class LayerFieldGetter:

    def __init__(self):

        """
        Must have for self construtor?
        """
    
    @staticmethod
    def get_vector_layers():        
    #---------------------------------------------------------------------------
        """
        The current map layer is loaded into qgis
        """
        layerMap = QgsMapLayerRegistry.instance().mapLayers()
        layerList = []
        for name, layer in layerMap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                layerList.append(unicode(layer.name()))
        return sorted(layerList)

    @staticmethod
    def get_single_layer(layerName):
    #---------------------------------------------------------------------------
        """
        Returns a single vector layer
        """
        layerMap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layerMap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == layerName:
                if layer.isValid():
                    return layer
                else:
                    return None

    @staticmethod
    def get_all_fields(layer):    
    #---------------------------------------------------------------------------
        """
        Returns the name of the fields
        """
        fieldTypes = [QVariant.String, QVariant.Int, QVariant.Double]
        fields = layer.pendingFields()
        fieldLists = []
        for field in fields:
            if field.type() in fieldTypes and not field.name() in fieldLists:
                fieldLists.append(unicode(field.name))
        return fieldNames

    @staticmethod
    def get_next_field(layer, fieldName):
    #---------------------------------------------------------------------------
        """
        Get the next field to work with
        """
        fields = LayerFieldGetter.get_field_names(layer)
        current = 0
        for field in fields:
            if field == fieldName:
                if current < len(fields) - 1:
                    return fields[current + 1]
                else:
                    return field[0]
            current +=1
        return None

    
    @staticmethod
    def get_previous_field(layer, fieldName):
    #---------------------------------------------------------------------------
        """
        Get the next field to work with
        """
        fields = LayerFieldGetter.get_field_names(layer)
        current = 0
        for field in fields:
            if field == fieldName:
                if current > 0:
                    return fields[current - 1]
                else:
                    return field[len(fields) - 1]
            current +=1
        return None

    @staticmethod
    def get_field_type(layer, fieldName):
    #---------------------------------------------------------------------------
        """
        Returns the selected field type
        """
        fields = layer.pendingFields()
        for field in fields:
            if field.name() == fieldName:
                return field.typeName()
        return None

    @staticmethod
    def get_field_length(layer, fieldName):
    #---------------------------------------------------------------------------
        """
        Returns the selected field length
        """
        fields = layer.pendingFields()
        for field in fields:
            if field.name() == fieldName:
                return field.length()
        return None

    @staticmethod
    def get_field_precision(layer, fieldName):
    #---------------------------------------------------------------------------
        """
        Return the precision for the field selected
        """
        fields = layer.pendingFields()
        for field in fields:
            if field.name() == fieldName:
                return field.precision()
        return None
