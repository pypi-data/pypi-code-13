'''
Created on Jul 25, 2016

@author: t_songr
'''

import xml.etree.cElementTree as ET
from collections import OrderedDict
from BuildingObjects import *
import csv

class gbXMLparser():
    def __init__(self, file_path):
        self._root = ET.parse(file_path).getroot()  
        self.results_dict = OrderedDict()
        
        # the unit of the project is here
        self.get_basic_info(self._root)
        
        # get the window type dictionary
        self.windowTypeDict = {}
        self.get_supporting_info(self._root)
#         
        self.get_surface_info(self._root)
        self.get_roof_info(self._root)
        self.get_raised_floor_info(self._root)
        self.get_interior_floor_info(self._root)
        self.get_slab_on_grade_info(self._root)
        self.get_shade_info(self._root)
        self.get_lighting_info(self._root)
        
        self.get_results_info(self._root)
    
    def get_supporting_info(self,_root):
        '''
        get the supporting information for this project
        e.g. the window type dictionary that contains the UV value and SHGC
        '''
        window_type_all = _root.findall('{http://www.gbxml.org/schema}WindowType')
        
        for each_window_type in window_type_all:
            thisID = each_window_type.attrib['id']
            thisUV = float(each_window_type.find('{http://www.gbxml.org/schema}U-value').text)
            thisSHGC = float(each_window_type.find('{http://www.gbxml.org/schema}SolarHeatGainCoeff').text)
            
            # converting square meter to square foot for UV-value
            thisUV = thisUV / (3.28084 * 3.28084)
            self.windowTypeDict[thisID] = {'U-Value':thisUV,'SHGC':thisSHGC}
            
    def get_basic_info(self, _root):
        '''
        Get the basic information of the building XML file:
        Unit, BuildingType, Latitude, Longitude, City and Country,
        designHeatWeathIdRef and designCoolWeathIdRef
        
        Input: Root, the root of the xml file
        Output: update the self.results_dict
        '''
        # getting sub-roots:
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _building = _campus.find('{http://www.gbxml.org/schema}Building')
        _location = _campus.find('{http://www.gbxml.org/schema}Location')
        
        # The unit that users used for the project
        Unit = _root.attrib['lengthUnit']
        if Unit == 'Feet':
            Unit = 'IP'
            self.unit = Unit
        elif Unit == 'Meters':
            Unit = 'SI'
            self.unit = Unit
        self.results_dict['Unit'] = Unit

        # Building Type:
        BuildingType = _building.attrib['buildingType']
        self.results_dict['BuildingType'] = BuildingType

        # Latitude and Longitude:
        Longitude = _location.find('{http://www.gbxml.org/schema}Longitude').text
        Latitude = _location.find('{http://www.gbxml.org/schema}Latitude').text
        self.results_dict['Latitude'] = Latitude
        self.results_dict['Longitude'] = Longitude

        # City and County:
        CityAndCountry = _location.find('{http://www.gbxml.org/schema}Name').text
        self.results_dict['CityAndCountry'] = CityAndCountry

        # Climate Zone:
        designHeatWeathIdRef = _campus.attrib['designHeatWeathIdRef']
        designCoolWeathIdRef = _campus.attrib['designCoolWeathIdRef']
        self.results_dict['designHeatWeathIdRef'] = designHeatWeathIdRef
        self.results_dict['designCoolWeathIdRef'] = designCoolWeathIdRef
    
    def get_surface_info(self, _root):
        '''
        Get the Information of Exterior Wall
        '''
        def safe_division(n, d):
            '''
            handle the case when window area is zero
            '''
            return n / d if d else 0
        # Get the sub-roots:
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        
        TotalWallArea = 0 # Total Wall Area for the entire building
        TotalWindowArea = 0 # Total Window Area for the entire building
        TotalWallAreaHeight = 0 # The total area times the level of the floor
        TotalWindowAreaHeight = 0 # The total area times the level of the floor
        
        WallAreaNorth = 0
        WallAreaNorthHeight = 0
        WindowAreaNorth = 0
        WindowAreaNorthHeight = 0
        WindowUVWeightedNorth = 0
        WindowSHGCWeightedNorth = 0
        _UV_area_north = 0
        _SHGC_area_north = 0
        
        WallAreaNorthEast = 0
        WallAreaNorthEastHeight = 0
        WindowAreaNorthEast = 0
        WindowAreaNorthEastHeight = 0
        WindowUVWeightedNorthEast = 0
        WindowSHGCWeightedNorthEast = 0
        _UV_area_northeast = 0
        _SHGC_area_northeast = 0
        
        WallAreaEast = 0
        WallAreaEastHeight = 0
        WindowAreaEast = 0
        WindowAreaEastHeight = 0
        WindowUVWeightedEast = 0
        WindowSHGCWeightedEast = 0
        _UV_area_east = 0
        _SHGC_area_east = 0
        
        WallAreaSouthEast = 0
        WallAreaSouthEastHeight = 0
        WindowAreaSouthEast = 0
        WindowAreaSouthEastHeight = 0
        WindowUVWeightedSouthEast = 0
        WindowSHGCWeightedSouthEast = 0
        _UV_area_southeast = 0
        _SHGC_area_southeast = 0
        
        WallAreaSouth = 0
        WallAreaSouthHeight = 0
        WindowAreaSouth = 0
        WindowAreaSouthHeight = 0
        WindowUVWeightedSouth = 0
        WindowSHGCWeightedSouth = 0
        _UV_area_south = 0
        _SHGC_area_south = 0
        
        WallAreaSouthWest = 0 
        WallAreaSouthWestHeight = 0
        WindowAreaSouthWest = 0
        WindowAreaSouthWestHeight = 0
        WindowUVWeightedSouthWest = 0
        WindowSHGCWeightedSouthWest = 0
        _UV_area_southwest = 0
        _SHGC_area_southwest = 0
                
        WallAreaWest = 0
        WallAreaWestHeight = 0
        WindowAreaWest = 0
        WindowAreaWestHeight = 0
        WindowUVWeightedWest = 0
        WindowSHGCWeightedWest = 0
        _UV_area_west = 0
        _SHGC_area_west = 0
        
        WallAreaNorthWest = 0
        WallAreaNorthWestHeight = 0
        WindowAreaNorthWest = 0
        WindowAreaNorthWestHeight = 0
        WindowUVWeightedNorthWest = 0
        WindowSHGCWeightedNorthWest = 0
        _UV_area_northwest = 0
        _SHGC_area_northwest = 0
        
        TotalOtherOpeningArea = 0
        TotalOtherOpeningAreaHeight = 0
        
        for eachSurface in _surface_all:   
            if eachSurface.attrib['surfaceType'] == 'ExteriorWall':
                this_wall_area = 0 # Total Wall Area for this Surface (surface area - window area)
                
                # For each surface            
                ThisSurface = ExteriorWall(eachSurface, self.unit)
            
                this_surface_area = ThisSurface.Area # Total Surface Area for this Surface
                this_angle = ThisSurface.angle # The direction of this surface in degree
                this_area_height = ThisSurface.AreaHeight # the area * level for this surface
                this_surface_level = ThisSurface.level
 
                # For every window on this surface
                ThisWindow = Window(eachSurface, this_surface_level, self.windowTypeDict, self.unit)
                this_window_area = ThisWindow.WindowArea # Total Window Area for this Surface
                this_window_area_height = ThisWindow.WindowAreaHeight # the area of the window * level for this surface
                
                # Calculate the area of the wall by minus the area of the windows and the area of other opening from the wall
                this_wall_area = ThisSurface.Area - ThisWindow.WindowArea - ThisWindow.OtherArea
                this_wall_area_height = this_area_height - this_window_area_height - ThisWindow.OtherAreaHeight

                TotalWallArea += this_wall_area
                TotalWindowArea += this_window_area
                
                TotalWallAreaHeight += this_wall_area_height
                TotalWindowAreaHeight += this_window_area_height
                
                TotalOtherOpeningArea += ThisWindow.OtherArea
                TotalOtherOpeningAreaHeight += ThisWindow.OtherAreaHeight
                
                if (this_angle >= 0 and this_angle < 22.5) or (this_angle <= 360 and this_angle >= 337.5):
                    WallAreaNorth += this_wall_area
                    WallAreaNorthHeight += this_wall_area_height
                    WindowAreaNorth += this_window_area
                    WindowAreaNorthHeight += this_window_area_height
                    _UV_area_north += ThisWindow.WindowUVArea
                    _SHGC_area_north += ThisWindow.WindowSHGCArea 
                
                elif (this_angle >= 22.5 and this_angle < 67.5):
                    WallAreaNorthEast += this_wall_area
                    WallAreaNorthEastHeight += this_wall_area_height
                    WindowAreaNorthEast += this_window_area
                    WindowAreaNorthEastHeight += this_window_area_height
                    _UV_area_northeast += ThisWindow.WindowUVArea
                    _UV_area_northeast += ThisWindow.WindowSHGCArea
                
                elif (this_angle >= 67.5 and this_angle < 112.5):
                    WallAreaEast += this_wall_area
                    WallAreaEastHeight += this_wall_area_height
                    WindowAreaEast += this_window_area
                    WindowAreaEastHeight += this_window_area_height
                    _UV_area_east += ThisWindow.WindowUVArea
                    _SHGC_area_east += ThisWindow.WindowSHGCArea
                    
                elif (this_angle >= 112.5 and this_angle < 157.5):
                    WallAreaSouthEast += this_wall_area
                    WallAreaSouthEastHeight += this_wall_area_height
                    WindowAreaSouthEast += this_window_area
                    WindowAreaSouthEastHeight += this_window_area_height
                    _UV_area_southeast += ThisWindow.WindowUVArea
                    _SHGC_area_southeast += ThisWindow.WindowSHGCArea
                
                elif (this_angle >= 157.5 and this_angle < 202.5):
                    WallAreaSouth += this_wall_area
                    WallAreaSouthHeight += this_wall_area_height
                    WindowAreaSouth += this_window_area
                    WindowAreaSouthHeight += this_window_area_height
                    _UV_area_south += ThisWindow.WindowUVArea
                    _SHGC_area_south += ThisWindow.WindowSHGCArea
                
                elif (this_angle >= 202.5 and this_angle < 247.5):
                    WallAreaSouthWest += this_wall_area
                    WallAreaSouthWestHeight += this_wall_area_height
                    WindowAreaSouthWest += this_window_area
                    WindowAreaSouthWestHeight += this_window_area_height
                    _UV_area_southwest += ThisWindow.WindowUVArea
                    _SHGC_area_southwest += ThisWindow.WindowSHGCArea
                    
                elif (this_angle >= 247.5 and this_angle < 292.5):
                    WallAreaWest += this_wall_area
                    WallAreaWestHeight += this_wall_area_height
                    WindowAreaWest += this_window_area
                    WindowAreaWestHeight += this_window_area_height
                    _UV_area_west += ThisWindow.WindowUVArea
                    _SHGC_area_west += ThisWindow.WindowSHGCArea
                    
                elif (this_angle >= 292.5 and this_angle < 337.5):
                    WallAreaNorthWest += this_wall_area
                    WallAreaNorthWestHeight += this_wall_area_height
                    WindowAreaNorthWest += this_window_area
                    WindowAreaNorthWestHeight += this_window_area_height   
                    _UV_area_northwest += ThisWindow.WindowUVArea
                    _SHGC_area_northwest += ThisWindow.WindowSHGCArea 
                    
                else: raise ValueError("Azimuth's range is wrong")
            
            # Calculate the weighted UV and SHGC for each direction
            WindowUVWeightedNorth = safe_division(_UV_area_north , WindowAreaNorth)
            WindowSHGCWeightedNorth = safe_division(_SHGC_area_north , WindowAreaNorth)
            
            WindowUVWeightedNorthEast = safe_division(_UV_area_northeast , WindowAreaNorthEast)
            WindowSHGCWeightedNorthEast = safe_division(_SHGC_area_northeast , WindowAreaNorthEast)
            
            WindowUVWeightedEast = safe_division(_UV_area_east , WindowAreaEast)
            WindowSHGCWeightedEast = safe_division(_SHGC_area_east , WindowAreaEast)
            
            WindowUVWeightedSouthEast = safe_division(_UV_area_southeast , WindowAreaSouthEast)
            WindowSHGCWeightedSouthEast = safe_division(_SHGC_area_southeast , WindowAreaSouthEast)
            
            WindowUVWeightedSouth = safe_division(_UV_area_south , WindowAreaSouth)
            WindowSHGCWeightedSouth = safe_division(_SHGC_area_south , WindowAreaSouth)
            
            WindowUVWeightedSouthWest = safe_division(_UV_area_southwest , WindowAreaSouthWest)
            WindowSHGCWeightedSouthWest = safe_division(_SHGC_area_southwest , WindowAreaSouthWest)
            
            WindowUVWeightedWest = safe_division(_UV_area_west , WindowAreaWest)
            WindowSHGCWeightedWest = safe_division(_SHGC_area_west , WindowAreaWest)
            
            WindowUVWeightedNorthWest = safe_division(_UV_area_northwest , WindowAreaNorthWest)
            WindowSHGCWeightedNorthWest = safe_division(_SHGC_area_northwest , WindowAreaNorthWest)
            
            # Dump Data    
            self.results_dict['TotalWallArea'] = TotalWallArea
            self.results_dict['TotalWallAreaHeight'] = TotalWallAreaHeight
            
            self.results_dict['WallAreaNorth'] = WallAreaNorth
            self.results_dict['WallAreaNorthHeight'] = WallAreaNorthHeight
            self.results_dict['WallAreaNorthEast'] = WallAreaNorthEast
            self.results_dict['WallAreaNorthEastHeight'] = WallAreaNorthEastHeight
            self.results_dict['WallAreaEast'] = WallAreaEast
            self.results_dict['WallAreaEastHeight'] = WallAreaEastHeight
            self.results_dict['WallAreaSouthEast'] = WallAreaSouthEast
            self.results_dict['WallAreaSouthEastHeight'] = WallAreaSouthEastHeight
            self.results_dict['WallAreaSouth'] = WallAreaSouth
            self.results_dict['WallAreaSouthHeight'] = WallAreaSouthHeight
            self.results_dict['WallAreaSouthWest'] = WallAreaSouthWest
            self.results_dict['WallAreaSouthWestHeight'] = WallAreaSouthWestHeight
            self.results_dict['WallAreaWest'] = WallAreaWest
            self.results_dict['WallAreaWestHeight'] = WallAreaWestHeight
            self.results_dict['WallAreaNorthWest'] = WallAreaNorthWest
            self.results_dict['WallAreaNorthWestHeight'] = WallAreaNorthWestHeight
            
            self.results_dict['TotalWindowArea'] = TotalWindowArea
            self.results_dict['TotalWindowAreaHeight'] = TotalWindowAreaHeight
            
            self.results_dict['WindowAreaNorth'] = WindowAreaNorth
            self.results_dict['WindowAreaNorthHeight'] = WindowAreaNorthHeight
            self.results_dict['WindowUVWeightedNorth'] = WindowUVWeightedNorth
            self.results_dict['WindowSHGCWeightedNorth'] = WindowSHGCWeightedNorth
            
            self.results_dict['WindowAreaNorthEast'] = WindowAreaNorthEast
            self.results_dict['WindowAreaNorthEastHeight'] = WindowAreaNorthEastHeight
            self.results_dict['WindowUVWeightedNorthEast'] = WindowUVWeightedNorthEast
            self.results_dict['WindowSHGCWeightedNorthEast'] = WindowSHGCWeightedNorthEast
            
            self.results_dict['WindowAreaEast'] = WindowAreaEast
            self.results_dict['WindowAreaEastHeight'] = WindowAreaEastHeight
            self.results_dict['WindowUVWeightedEast'] = WindowUVWeightedEast
            self.results_dict['WindowSHGCWeightedEast'] = WindowSHGCWeightedEast
            
            self.results_dict['WindowAreaSouthEast'] = WindowAreaSouthEast
            self.results_dict['WindowAreaSouthEastHeight'] = WindowAreaSouthEastHeight
            self.results_dict['WindowUVWeightedSouthEast'] = WindowUVWeightedSouthEast
            self.results_dict['WindowSHGCWeightedSouthEast'] = WindowSHGCWeightedSouthEast
            
            self.results_dict['WindowAreaSouth'] = WindowAreaSouth
            self.results_dict['WindowAreaSouthHeight'] = WindowAreaSouthHeight
            self.results_dict['WindowUVWeightedSouth'] = WindowUVWeightedSouth
            self.results_dict['WindowSHGCWeightedSouth'] = WindowSHGCWeightedSouth
            
            self.results_dict['WindowAreaSouthWest'] = WindowAreaSouthWest
            self.results_dict['WindowAreaSouthWestHeight'] = WindowAreaSouthWestHeight
            self.results_dict['WindowUVWeightedSouthWest'] = WindowUVWeightedSouthWest
            self.results_dict['WindowSHGCWeightedSouthWest'] = WindowSHGCWeightedSouthWest
            
            self.results_dict['WindowAreaWest'] = WindowAreaWest
            self.results_dict['WindowAreaWestHeight'] = WindowAreaWestHeight
            self.results_dict['WindowUVWeightedWest'] = WindowUVWeightedWest
            self.results_dict['WindowSHGCWeightedWest'] = WindowSHGCWeightedWest
            
            self.results_dict['WindowAreaNorthWest'] = WindowAreaNorthWest
            self.results_dict['WindowAreaNorthWestHeight'] = WindowAreaNorthWestHeight
            self.results_dict['WindowUVWeightedNorthWest'] = WindowUVWeightedNorthWest
            self.results_dict['WindowSHGCWeightedNorthWest'] = WindowSHGCWeightedNorthWest
            
            self.results_dict['TotalOtherOpeningArea'] = TotalOtherOpeningArea
            self.results_dict['TotalOtherOpeningAreaHeight'] = TotalOtherOpeningAreaHeight
            
    def get_roof_info(self, _root):
        '''
        Get the geometry information for roof
        '''
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        
        TotalRoofArea = 0
        TotalRoofAreaHeight = 0 
        
        for eachSurface in _surface_all:
            if eachSurface.attrib['surfaceType'] == 'Roof':
                thisRoof = Roof(eachSurface, self.unit)
                
                TotalRoofArea += thisRoof.RoofArea
                TotalRoofAreaHeight += thisRoof.heightArea   
        # Dump
        self.results_dict['TotalRoofArea'] = TotalRoofArea
        self.results_dict['TotalRoofAreaHeight'] = TotalRoofAreaHeight
        
    def get_raised_floor_info(self,_root):  
        ''' 
        get the raised floor area info
        '''  
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        
        TotalRaiseFloorArea = 0
        TotalRaisedFloorAreaHeight = 0
        
        for eachSurface in _surface_all:
            if eachSurface.attrib['surfaceType'] == 'RaisedFloor':
                thisRaisedFloor = RaisedFloor(eachSurface,self.unit)
                TotalRaiseFloorArea += thisRaisedFloor.Area
                TotalRaisedFloorAreaHeight += thisRaisedFloor.heightArea
        
        # Dump data
        self.results_dict['TotalRaiseFloorArea'] = TotalRaiseFloorArea
        self.results_dict['TotalRaisedFloorAreaHeight'] = TotalRaisedFloorAreaHeight
         
    def get_interior_floor_info(self,_root):
        '''
        get the interior floor information
        '''
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        
        TotalInteriorFloorArea = 0
        TotalInteriorFloorAreaHeight = 0
        
        for eachSurface in _surface_all:
            if eachSurface.attrib['surfaceType'] == 'InteriorFloor':
                thisInteriorFloor = InteriorFloor(eachSurface,self.unit)
                TotalInteriorFloorArea += thisInteriorFloor.Area
                TotalInteriorFloorAreaHeight += thisInteriorFloor.heightArea
        
        # Dump data
        self.results_dict['TotalInteriorFloorArea'] = TotalInteriorFloorArea
        self.results_dict['TotalInteriorFloorAreaHeight'] = TotalInteriorFloorAreaHeight
    
    def get_slab_on_grade_info(self,_root):   
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        
        TotalSlabOnGradeArea = 0
        
        for eachSurface in _surface_all:
            if eachSurface.attrib['surfaceType'] == 'SlabOnGrade':
                thisSlabOnGrade = SlabOnGrade(eachSurface, self.unit)
                TotalSlabOnGradeArea += thisSlabOnGrade.Area
                
        # Dump data
        self.results_dict['TotalSlabOnGradeArea'] = TotalSlabOnGradeArea
    
    def get_shade_info(self,_root):
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _surface_all = _campus.findall('{http://www.gbxml.org/schema}Surface')
        
        TotalShadeArea = 0
        TotalVerticalShadeArea = 0
        TotalHorizontalShadeArea = 0
        TotalSouthShadeArea = 0
        TotalNorthShadeArea = 0
        TotalWestShadeArea = 0
        TotalEastShadeArea = 0
        
        for eachSurface in _surface_all:
            if eachSurface.attrib['surfaceType'] == 'Shade' :
                thisShade = Shade(eachSurface,self.unit)
                TotalShadeArea += thisShade.Area
        
        # Dump data
        self.results_dict['TotalShadeArea'] = TotalShadeArea
    
    def get_lighting_info(self,_root):
        '''
        getting the lighting efficiency information for each space
        '''
        _campus = _root.find('{http://www.gbxml.org/schema}Campus')
        _building = _campus.find('{http://www.gbxml.org/schema}Building')
        _space_all = _building.findall('{http://www.gbxml.org/schema}Space')
        
        TotalSpaceArea = 0
        TotalLightingEfficiencybySpaceArea = 0
        
        WeightedLightingEfficiency = 0
        
        for eachSpace in _space_all:
            thisLighting = LightingEfficiency(eachSpace, self.unit)
            TotalSpaceArea += thisLighting.SpaceArea
            TotalLightingEfficiencybySpaceArea += thisLighting.LightingPowerbySpaceArea
           
        WeightedLightingEfficiency = TotalLightingEfficiencybySpaceArea / TotalSpaceArea

        #Dump data
        self.results_dict['WeightedLightingEfficiency'] = WeightedLightingEfficiency
            
    def get_results_info(self, _root):
        _results = _root.findall('{http://www.gbxml.org/schema}Results')
        
        for eachResults in _results:
            if eachResults.attrib['id'] == 'Campus-2305001-1':
                # Electricity, kBtu
                thisElectricity = ElectricityResults(eachResults, self.unit)
                annualElectricity = thisElectricity.AnnualElectricity
                
                # Dump data
                self.results_dict['Electric Energy Use (KBtu)'] = annualElectricity
                
            elif eachResults.attrib['id'] == 'Campus-2306001-1':
                # Nature Gas, kBtu
                thisFuel = FuelResults(eachResults, self.unit)
                annualFuel = thisFuel.AnnualFuel
            
                # Dump data
                self.results_dict['Fuel Energy Use (KBtu)'] = annualFuel
                
    def dump_to_csv(self, file_name):
        '''
        Save to file
        '''
        with open(file_name, 'wb') as myfile:
            thisWriter = csv.writer(myfile)
            thisWriter.writerow(self.results_dict.keys())
            thisWriter.writerow(self.results_dict.values())
            
if __name__ == '__main__':
    # Example:
    file = './data/gbXMLStandard4.xml'
    thisParser = gbXMLparser(file)
    thisParser.dump_to_csv('test.csv')
    
    # Batch Example:
#     folder_path = './gbXML_all/'
    
    
    
    
    
    
    