import numpy as np
from pyspark import SparkConf,SparkContext
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.regression import Vectors
from pyspark.mllib.tree import RandomForest, RandomForestModel
from pyspark.mllib.regression import LinearRegressionModel
from pyspark.mllib.regression import LinearRegressionWithSGD
from pyspark.mllib.util import MLUtils
from pyspark.sql import SQLContext
from beijingtomorrow.databasebuilder import loadVisualTrainingDataToArray,loadAerosolTrainingDataToArray,loadVisualTestDataToArray,loadAerosolTestDataToArray
import os, inspect

    
def averageBrightness4By4(input_image):
    """Reduces the input image to a 4x4 black-and-white"""
    vert_ones = np.ones((32,1))
    vert_zeros = np.zeros((32,1))
    reducer_top = np.concatenate((vert_ones,vert_zeros,vert_zeros,vert_zeros),axis=1)
    reducer_second = np.concatenate((vert_zeros,vert_ones,vert_zeros,vert_zeros),axis=1)
    reducer_third = np.concatenate((vert_zeros,vert_zeros,vert_ones,vert_zeros),axis=1)
    reducer_bottom = np.concatenate((vert_zeros,vert_zeros,vert_zeros,vert_ones),axis=1)
    reducer = np.concatenate((reducer_top,reducer_second,reducer_third,reducer_bottom),axis=0)
    reducer_t = reducer.swapaxes(0,1)
    halfway_red = np.dot(reducer_t,input_image[0])
    reduced_image_red = np.dot(halfway_red,reducer)
    halfway_green = np.dot(reducer_t,input_image[1])
    reduced_image_green = np.dot(halfway_green,reducer)
    halfway_blue = np.dot(reducer_t,input_image[2])
    reduced_image_blue = np.dot(halfway_blue,reducer)
    rg = np.add(reduced_image_red,reduced_image_green)
    rgb = np.add(rg,reduced_image_blue)
    avg = rgb*(1/float(3072))
    return np.ravel(avg).tolist()

def varsToLabeledPoint(input_duple):
    """For a lambda: Turns a duple of number, vector into a Spark LabeledPoint object"""
    return LabeledPoint(float(input_duple[0]),input_duple[1])

def featuresToVectors(input_list):
    return Vectors.dense(input_list)
    """For a lambda: Turns a numeric list into a Spark LabeledPoint object"""
def printline(x):
    """For a lambda: Turns the argument to a string and prints it"""
    print(str(x) + "\n")
    
    
"""
This main routine estimates a random forest model to predict tomorrow's pollution change given
today's satellite image.
"""

if __name__ == '__main__':

    this_file = os.path.abspath(inspect.getfile(inspect.currentframe()))
    project_dir = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
    visualModelFile= os.path.join(project_dir,"resources/random_forest_models/beijing_pollution_model_visual_rf")
    aerosolModelFile= os.path.join(project_dir,"resources/random_forest_models/beijing_pollution_model_aerosol_rf")
    
    sparkConf = SparkConf().setAppName("BeijingTomorrow").setMaster("local")
    sc=SparkContext(conf=sparkConf)
    sqlContext = SQLContext(sc)

    (visual_training_image_array , visual_training_outcome_array ) = loadVisualTrainingDataToArray()
    #We have to turn it into a list of observations
    visual_training_data = []
    for i in range(0,len(visual_training_outcome_array) ):
        visual_training_data.append((visual_training_outcome_array[i],visual_training_image_array[i]))
    visual_training_rdd = sc.parallelize(visual_training_data)
    visual_data_flattened = visual_training_rdd.map(lambda x : ( x[0] , averageBrightness4By4(x[1])) )
    visual_data_labeled_points = visual_data_flattened.map(lambda x : varsToLabeledPoint(x))
    toprint=visual_data_labeled_points.take(1)
    print(str(toprint))
    visual_model = RandomForest.trainRegressor(visual_data_labeled_points, categoricalFeaturesInfo={},
                                    numTrees=1000, featureSubsetStrategy="auto",
                                    impurity='variance', maxDepth=5, maxBins=100)
    #visual_model = LinearRegressionWithSGD.train(visual_data_labeled_points, iterations=3,intercept=True)

    visual_training_vectors = visual_data_flattened.map(lambda x : featuresToVectors(x[1]))
    toprint = visual_training_vectors.take(1)
    print(str(toprint))
    visual_in_sample_predictions = visual_model.predict(visual_training_vectors)
    visual_in_sample_labels_and_predictions = visual_data_labeled_points.map(lambda lp: lp.label).zip(visual_in_sample_predictions)
    visual_in_sample_labels_and_predictions.foreach(printline)
    squaresdf = visual_in_sample_labels_and_predictions.map(lambda p : (p[0] , p[0]*p[0] , p[0] - p[1] , (p[0] - p[1])*(p[0] - p[1]) , 1 ) )
    squares = squaresdf.reduce(lambda a , b : (a[0]+b[0] , a[1]+b[1] , a[2]+b[2] , a[3]+b[3] , a[4]+b[4] ) )
    tss = float(squares[1]) - float(squares[0]*squares[0])/float(squares[4])
    rss = float(squares[3]) - float(squares[2]*squares[2])/float(squares[4])
    r2 = 1-rss/tss
    print("Training set:")
    print("Total SS: " + str(tss))
    print("Redidual SS: " + str(rss))
    print("R-Squared: " + str(r2))
    print str(squares)



    (visual_test_image_array , visual_test_outcome_array ) = loadAerosolTestDataToArray()
    #We have to turn it into a list of observations

    visual_test_data = []
    for i in range(0,len(visual_test_outcome_array) ):
        visual_test_data.append((visual_test_outcome_array[i],visual_test_image_array[i]))
    visual_test_rdd = sc.parallelize(visual_test_data)
    visual_test_data_flattened = visual_test_rdd.map(lambda x : ( x[0] , averageBrightness4By4(x[1])) )
    visual_test_vectors = visual_test_data_flattened.map(lambda x : featuresToVectors(x[1]))
    visual_predictions = visual_model.predict(visual_test_vectors)
    visual_labels_and_predictions = visual_test_data_flattened.map(lambda lp: lp[0]).zip(visual_predictions)
    visual_labels_and_predictions.foreach(printline)
    squaresdf = visual_labels_and_predictions.map(lambda p : (p[0] , p[0]*p[0] , p[0] - p[1] , (p[0] - p[1])*(p[0] - p[1]) , 1 ) )
    squares = squaresdf.reduce(lambda a , b : (a[0]+b[0] , a[1]+b[1] , a[2]+b[2] , a[3]+b[3] , a[4]+b[4] ) )
    tss = float(squares[1]) - float(squares[0]*squares[0])/float(squares[4])
    rss = float(squares[3]) - float(squares[2]*squares[2])/float(squares[4])
    r2 = 1-rss/tss
    print("Test set:")
    print("Total SS: " + str(tss))
    print("Redidual SS: " + str(rss))
    print("R-Squared: " + str(r2))
    print str(squares)


    visual_model.save(sc,visualModelFile)

    (aerosol_training_image_array , aerosol_training_outcome_array ) = loadVisualTrainingDataToArray()
    #We have to turn it into a list of observations
    aerosol_training_data = []
    for i in range(0,len(aerosol_training_outcome_array) ):
        aerosol_training_data.append((aerosol_training_outcome_array[i],aerosol_training_image_array[i]))
    aerosol_training_rdd = sc.parallelize(aerosol_training_data)
    aerosol_data_flattened = aerosol_training_rdd.map(lambda x : ( x[0] , averageBrightness4By4(x[1])) )
    aerosol_data_labeled_points = aerosol_data_flattened.map(lambda x : varsToLabeledPoint(x))
    toprint=aerosol_data_labeled_points.take(1)
    print(str(toprint))
    aerosol_model = RandomForest.trainRegressor(aerosol_data_labeled_points, categoricalFeaturesInfo={},
                                    numTrees=1000, featureSubsetStrategy="auto",
                                    impurity='variance', maxDepth=5, maxBins=100)
    #aerosol_model = LinearRegressionWithSGD.train(aerosol_data_labeled_points, iterations=3,intercept=True)

    aerosol_training_vectors = aerosol_data_flattened.map(lambda x : featuresToVectors(x[1]))
    toprint = aerosol_training_vectors.take(1)
    print(str(toprint))
    aerosol_in_sample_predictions = aerosol_model.predict(aerosol_training_vectors)
    aerosol_in_sample_labels_and_predictions = aerosol_data_labeled_points.map(lambda lp: lp.label).zip(aerosol_in_sample_predictions)
    aerosol_in_sample_labels_and_predictions.foreach(printline)
    squaresdf = aerosol_in_sample_labels_and_predictions.map(lambda p : (p[0] , p[0]*p[0] , p[0] - p[1] , (p[0] - p[1])*(p[0] - p[1]) , 1 ) )
    squares = squaresdf.reduce(lambda a , b : (a[0]+b[0] , a[1]+b[1] , a[2]+b[2] , a[3]+b[3] , a[4]+b[4] ) )
    tss = float(squares[1]) - float(squares[0]*squares[0])/float(squares[4])
    rss = float(squares[3]) - float(squares[2]*squares[2])/float(squares[4])
    r2 = 1-rss/tss
    print("Training set:")
    print("Total SS: " + str(tss))
    print("Redidual SS: " + str(rss))
    print("R-Squared: " + str(r2))
    print str(squares)



    (aerosol_test_image_array , aerosol_test_outcome_array ) = loadAerosolTestDataToArray()
    #We have to turn it into a list of observations

    aerosol_test_data = []
    for i in range(0,len(aerosol_test_outcome_array) ):
        aerosol_test_data.append((aerosol_test_outcome_array[i],aerosol_test_image_array[i]))
    aerosol_test_rdd = sc.parallelize(aerosol_test_data)
    aerosol_test_data_flattened = aerosol_test_rdd.map(lambda x : ( x[0] , averageBrightness4By4(x[1])) )
    aerosol_test_vectors = aerosol_test_data_flattened.map(lambda x : featuresToVectors(x[1]))
    aerosol_predictions = aerosol_model.predict(aerosol_test_vectors)
    aerosol_labels_and_predictions = aerosol_test_data_flattened.map(lambda lp: lp[0]).zip(aerosol_predictions)
    aerosol_labels_and_predictions.foreach(printline)
    squaresdf = aerosol_labels_and_predictions.map(lambda p : (p[0] , p[0]*p[0] , p[0] - p[1] , (p[0] - p[1])*(p[0] - p[1]) , 1 ) )
    squares = squaresdf.reduce(lambda a , b : (a[0]+b[0] , a[1]+b[1] , a[2]+b[2] , a[3]+b[3] , a[4]+b[4] ) )
    tss = float(squares[1]) - float(squares[0]*squares[0])/float(squares[4])
    rss = float(squares[3]) - float(squares[2]*squares[2])/float(squares[4])
    r2 = 1-rss/tss
    print("Test set:")
    print("Total SS: " + str(tss))
    print("Redidual SS: " + str(rss))
    print("R-Squared: " + str(r2))
    print str(squares)

    aerosol_model.save(sc,aerosolModelFile)

