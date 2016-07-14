from pyspark import SparkConf,SparkContext
from com.yahoo.ml.caffe.RegisterContext import registerContext,registerSQLContext
from com.yahoo.ml.caffe.CaffeOnSpark import CaffeOnSpark
from com.yahoo.ml.caffe.Config import Config
from com.yahoo.ml.caffe.DataSource import DataSource
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.classification import LogisticRegressionWithLBFGS
from pyspark.sql import SQLContext
import os, inspect
from caffe import TEST
from caffe import Net
from caffe import NetSpec
from caffe import SGDSolver
from caffe import layers as L
from caffe import params as P

"""
This function calls CaffeOnSpark to train the model.  It is similar in 
structure to the LeNext example, e.g., see
https://github.com/yahoo/CaffeOnSpark/wiki/GetStarted_python
In fact, the Python interface for CaffeOnSpark currently (July 2016)
allows for very little deviation from this format. 
"""

if __name__ == '__main__':

    sparkConf = SparkConf().setAppName("BeijingTomorrow").setMaster("local")
    sc=SparkContext(conf=sparkConf)
    registerContext(sc)
    sqlContext = SQLContext(sc)
    registerSQLContext(sqlContext)
    cos=CaffeOnSpark(sc,sqlContext)
    cfg=Config(sc)
    this_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
    visualProtoFile= os.path.join(project_dir,"resources/caffe_prototxt/beijing_pollution_solver_visual.prototxt")
    visualModelFile= os.path.join(project_dir,"resources/caffe_models/beijing_pollution_model_visual.model")
    aerosolProtoFile= os.path.join(project_dir,"resources/caffe_prototxt/beijing_pollution_solver_aerosol.prototxt")
    aerosolModelFile= os.path.join(project_dir,"resources/caffe_models/beijing_pollution_model_aerosol.model")

    cfg.protoFile = visualProtoFile
    cfg.modelPath = 'file:' + visualModelFile
    cfg.devices = 1
    cfg.isFeature=True
    cfg.label='label'
    cfg.features=['ip1']
    cfg.outputFormat = 'json'
    cfg.clusterSize = 1
    cfg.lmdb_partitions=cfg.clusterSize
    
#Train
    dl_train_source = DataSource(sc).getSource(cfg,True)

    cos.train(dl_train_source)

#Extract features
    
    lr_raw_source = DataSource(sc).getSource(cfg,False)
    extracted_df = cos.features(lr_raw_source)
    extracted_df.show(365)
    squaresdf = extracted_df.map(lambda p : (p.label[0] , p.label[0]*p.label[0] , (p.label[0] - p.ip1[0]) , (p.label[0] - p.ip1[0])*(p.label[0] - p.ip1[0]) , 1 ) )
    squares = squaresdf.reduce(lambda a , b : (a[0]+b[0] , a[1]+b[1] , a[2]+b[2] , a[3]+b[3] , a[4]+b[4] ) )
    tss = float(squares[1]) - float(squares[0]*squares[0])/float(squares[4])
    rss = float(squares[3]) - float(squares[2]*squares[2])/float(squares[4])
    r2 = 1-rss/tss
    print("Test set:")
    print("Total SS: " + str(tss))
    print("Redidual SS: " + str(rss))
    print("R-Squared: " + str(r2))
    print str(squares)


    cfg.protoFile = aerosolProtoFile
    cfg.modelPath = 'file:' + aerosolModelFile

    dl_train_source = DataSource(sc).getSource(cfg,True)

    cos.train(dl_train_source)

#Extract features
    
    lr_raw_source = DataSource(sc).getSource(cfg,False)
    extracted_df = cos.features(lr_raw_source)
    extracted_df.show(365)
    squaresdf = extracted_df.map(lambda p : (p.label[0] , p.label[0]*p.label[0] , (p.label[0] - p.ip1[0]) , (p.label[0] - p.ip1[0])*(p.label[0] - p.ip1[0]) , 1 ) )
    squares = squaresdf.reduce(lambda a , b : (a[0]+b[0] , a[1]+b[1] , a[2]+b[2] , a[3]+b[3] , a[4]+b[4] ) )
    tss = float(squares[1]) - float(squares[0]*squares[0])/float(squares[4])
    rss = float(squares[3]) - float(squares[2]*squares[2])/float(squares[4])
    r2 = 1-rss/tss
    print("Test set:")
    print("Total SS: " + str(tss))
    print("Redidual SS: " + str(rss))
    print("R-Squared: " + str(r2))
    print str(squares)

    
    """
    
    Report the bug about this:
    extracted_df = cos.features(dl_train_source)
    extracted_df.show(300)
    squaresdf = extracted_df.map(lambda p : (p.label[0] , p.label[0]*p.label[0] , (p.label[0] - p.ip1[0]) , (p.label[0] - p.ip1[0])*(p.label[0] - p.ip1[0]) , 1 ) )
    squares = squaresdf.reduce(lambda a , b : (a[0]+b[0] , a[1]+b[1] , a[2]+b[2] , a[3]+b[3] , a[4]+b[4] ) )
    tss = float(squares[1]) - float(squares[0]*squares[0])/float(squares[4])
    rss = float(squares[3]) - float(squares[2]*squares[2])/float(squares[4])
    r2 = 1-rss/tss
    print("Training set:")
    print("Total SS: " + str(tss))
    print("Redidual SS: " + str(rss))
    print("R-Squared: " + str(r2))
    """
    