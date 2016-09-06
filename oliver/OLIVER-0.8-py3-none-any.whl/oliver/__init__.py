import pandas
import numpy
from py4j.java_gateway import JavaGateway
gateway = JavaGateway()
workspace = gateway.entry_point
	
def copyHeatmap( hm, title ):
    result = gateway.jvm.oliver.map.Heatmap( hm )
    result.setTitle( title )
    return result
	
def getOpenHeatmap( title=None ):
    openHeatmaps = workspace.getOpenHeatmaps()
    if not title or len(title)==0:
        return openHeatmaps[0]
    results = [hm for hm in openHeatmaps if hm.getTitle() == title]
    return results[0]
	
def displayHeatmap( heatmap ):
    workspace.displayHeatmap( heatmap )
	
def getHeatmap( dataframe ):
    nRows = len(dataframe.index)
    nTotalCols = len( dataframe.columns )
    nTimeCols = nTotalCols
    for i in range( nTotalCols ):
        if isinstance(dataframe.columns[i], str):
            nTimeCols = i;
            break;
    
    jRowLabels = gateway.new_array(gateway.jvm.java.lang.String,nRows)
    jData = gateway.new_array(gateway.jvm.double,nRows,nTimeCols)
    jTimes = gateway.new_array(gateway.jvm.double,nTimeCols)
    
    for row in range(nRows):
        jRowLabels[row] = dataframe.index[row]
    
    for col in range(nTimeCols):
        jTimes[col] = dataframe.columns[col]
    
    for row in range(nRows):
        for col in range(nTimeCols):
            jData[row][col] = dataframe.iat[row,col]
            
    result = gateway.jvm.oliver.map.Heatmap( jRowLabels, jTimes, jData )
    
    for col in range( nTimeCols, nTotalCols ):
        jEcVals =  gateway.new_array(gateway.jvm.java.io.Serializable,nRows)
        for row in range(nRows):
            jEcVals[row] = dataframe.iat[row,col]
        result.addExtraColumn( dataframe.columns[col], jEcVals )

    return result
            
	
def getDataFrame( heatmap ):
    jRowLabels = heatmap.getRowLabels( True )
    jTimes = heatmap.getTimeLabels()
    jData = heatmap.getValueMatrix()
    jEcLabels = heatmap.getExtraColumnLabels().toArray()
    
    nRows = len(jRowLabels)
    nTimeCols = len(jTimes)
    nExtraCols = len(jEcLabels)
    
    rowLabels = []
    for i in range( nRows ):
        rowLabels.append( jRowLabels[i] )
        
    columnHeaders = []
    for i in range( nTimeCols ):
        columnHeaders.append( jTimes[i] )
        
    data = []
    for row in range( nRows ):
        dataRow = []
        for col in range( nTimeCols ):
            dataRow.append( jData[row][col] )
        data.append( dataRow )
        
    for i in range( nExtraCols ):
        jEcData = heatmap.getExtraColumnValues( jEcLabels[i] )
        columnHeaders.append( jEcLabels[i] )
        for row in range( nRows ):
            data[row].append( jEcData[row] )
        
    df = pandas.DataFrame(data, index=rowLabels, columns=columnHeaders)
    return df