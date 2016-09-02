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