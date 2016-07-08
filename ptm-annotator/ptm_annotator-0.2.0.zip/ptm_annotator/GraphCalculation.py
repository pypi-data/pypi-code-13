
""" This class helps perform calculations associated with 
	drawing feature within  a digram 
	
	To recompile .pyc code
	python -m py_compile fileA.py fileB.py fileC.py
	"""
## Def to get the tick postion
def tickPosition(graphLenth,molLength,featurePosition):
	newPosition = (float(graphLenth)/float(molLength))*float(featurePosition)
	return int(newPosition)

## Def to adjust tick postion base on the length of the protein sequence
def finalTickPosition(graphLenth,molLength,featurePosition,graphX,graphY):
	finalPosition = int(tickPosition(graphLenth,molLength,featurePosition)) + int(graphX)
	return finalPosition

## Def to get the final peptide coverage coordinates
def peptideCoverageIntervals(interval,graphLenth,molLength,graphX,graphY ):
	start = int(interval[0])
	stop = int(interval[1])
	finalStart = int(tickPosition(graphLenth,molLength,start)) + int(graphX)
	finalStop = int(tickPosition(graphLenth,molLength,stop)) + int(graphX)
	return (finalStart,finalStop)

## Convert number lists to ranges 
def ranges(p):
    q = sorted(p)
    i = 0
    for j in xrange(1,len(q)):
        if q[j] > 1+q[j-1]:
            yield [q[i],q[j-1]]
            i = j
    yield [q[i], q[-1]]


## Convert the peptide coordinates to single array
def concatinatePeptidePosition(listInterval):
	## Convert intervals to set and crate a single array
	originalIntervals = listInterval
	arrayCombine = []
	
	for i in range(len(originalIntervals)):
		arrayCombine.extend(range(originalIntervals[i][0],originalIntervals[i][1]))
	
	return(arrayCombine)



 
## Def to calulate the peptide coverage range for the figure from multiple peptides
def calCulatePeptideCoverage(listInterval):
    # Convert intervals to set and crate a single array
    originalIntervals = listInterval
    arrayCombine = []
	
    for i in range(len(originalIntervals)):
        arrayCombine.extend(range(int(originalIntervals[i][0]),int(originalIntervals[i][1])))
    
    return list(ranges(arrayCombine))