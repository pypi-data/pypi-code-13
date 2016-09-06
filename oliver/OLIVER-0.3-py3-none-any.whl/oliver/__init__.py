import pandas
import numpy
from py4j.java_gateway import JavaGateway
gateway = JavaGateway()
workspace = gateway.entry_point
	
def copyHeatmap( hm, title ):
    result = gateway.jvm.oliver.map.Heatmap( hm )
    result.setTitle( title )
    return result
	
def getOpenHeatmap( title ):
    results = [hm for hm in workspace.getOpenHeatmaps() if hm.getTitle() == title]
    return results[0]
	
def displayHeatmap( hm ):
    workspace.displayHeatmap( hm )
	
def getDataFrame( hm ):
    jRowLabels = hm.getRowLabels( True )
    jTimes = hm.getTimeLabels()
    jData = hm.getValueMatrix()
    jEcLabels = hm.getExtraColumnLabels().toArray()
    
    nRows = len(jRowLabels)
    nDataCols = len(jTimes)
    nExtraCols = len(jEcLabels)
    
    rowLabels = []
    for i in range( nRows ):
        rowLabels.append( jRowLabels[i] )
        
    columnHeaders = []
    for i in range( nDataCols ):
        columnHeaders.append( jTimes[i] )
        
    data = []
    for row in range( nRows ):
        dataRow = []
        for col in range( nDataCols ):
            dataRow.append( jData[row][col] )
        data.append( dataRow )
        
    for i in range( nExtraCols ):
        jEcData = hm.getExtraColumnValues( jEcLabels[i] )
        columnHeaders.append( jEcLabels[i] )
        for row in range( nRows ):
            data[row].append( jEcData[row] )
        
    df = pandas.DataFrame(data, index=rowLabels, columns=columnHeaders)
    return df