import sys, numpy, scipy
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist

inFile = open(sys.argv[1],'r')
colHeaders = inFile.next().strip().split()[1:]
rowHeaders = []
dataMatrix = []
for line in inFile:
	data = line.strip().split()
	rowHeaders.append(data[0])
	dataMatrix.append([float(x) for x in data[1:]])

dataMatrix = numpy.array(dataMatrix)

distanceMatrix = dist.pdist(dataMatrix)
distanceSquareMatrix = dist.squareform(distanceMatrix)
linkageMatrix = hier.linkage(distanceSquareMatrix)

heatmapOrder = hier.leaves_list(linkageMatrix)

orderedDataMatrix = dataMatrix[heatmapOrder,:]

rowHeaders = numpy.array(rowHeaders)
orderedRowHeaders = rowHeaders[heatmapOrder,:]

matrixOutput = []
row = 0
for rowData in orderedDataMatrix:
	col = 0
	rowOutput = []
	for colData in rowData:
		rowOutput.append([colData, row, col])
		col += 1
	matrixOutput.append(rowOutput)
	row += 1

print 'var maxData = ' + str(numpy.amax(dataMatrix)) + ";"
print 'var minData = ' + str(numpy.amin(dataMatrix)) + ";"
print 'var data = ' + str(matrixOutput) + ";"
print 'var cols = ' + str(colHeaders) + ";"
print 'var rows = ' + str([x for x in orderedRowHeaders]) + ";"
