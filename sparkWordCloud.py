"""
Apache Spark python code for generating Wordcloud from the user given text files.
Stop words are removed using Spark's machine learning package, before creating the wordcloud.

usage:
$ ./spark-submit --master local /home/sdh/Downloads/sparkWordCloud.py file-or-directory-path
User can specify either single file or a directory containing text files via command line.

Output:
myword.bmp in current directory i.e. "spark-2.3.0-bin-hadoop2.7/bin/"

Prerequisites:
wordcloud from https://github.com/amueller/word_cloud, which inturn would need numpy, pillow and matplotlib. 
consult the github page for detailed installation & usage options.

Installing wordcloud:
$ pip install wordcloud
"""

from __future__ import print_function
import sys
import operator

from pyspark.sql import SparkSession 
from pyspark.sql import Row
from pyspark.ml.feature import StopWordsRemover
from wordcloud import WordCloud

if __name__ == "__main__":
  # Check if user has specified the file path
  if(len(sys.argv) != 2):
    print("Usage: wordcount directory-name", file=sys.stderr)
    exit(-1)

  # create spark session and access spark context
  spark = SparkSession.builder.appName("word count app").getOrCreate()
  sc = spark.sparkContext

  # read the file path and create RDD
  rdd = sc.textFile(sys.argv[1], use_unicode=False)
  # split the RDD elements based and flatten the result. Result is simply an RDD containing collection of words.
  rdd1 = rdd.flatMap(lambda x: x.split(' '))
  
  # remove stop-words using spark's ML package  
  rdd2 = rdd1.map(lambda x: Row(name=[x]))
  sparkDataFrame = spark.createDataFrame(rdd2)
  remover = StopWordsRemover(inputCol="name", outputCol="filtered")
  filteredRDD = remover.transform(sparkDataFrame).rdd.flatMap(lambda x: x.filtered)
  #remover.transform(sparkDataFrame).show()

  # get the frequency of each element of  RDD2 through below steps.
  """
  eg: rdd2 = ["hello", "spark", "hello", "distributed"] 
      step 1: convet rdd1 to  --> [("hello",1), ("spark", 1), ("hello",1), ("distributed", 1)] 
      step 2: convert output of step 1 to  -- > [("hello", 2), ("spark", 1), ("distributed", 1)]
  """
  rdd3 = filteredRDD.map(lambda x: (x,1)).reduceByKey(operator.add)

  """
  # Uncomment below code if you want to save the RDD to a text file for future reference. The textfile should be read for generating wordcloud.
  rdd2.saveAsTextFile("./wordcount")
  text = open('./wordcount/part-00000')).read()
  wordCloudOutput = WordCloud().generate(text)
  wordCloudOutput.to_file('wordcloud.bmp')  
  """

  
  #Saving RDD to a text file and reading the text file is slower. Hence, we directly read the contents of RDD and feed to wordcloud module.  
  #rddOutput = rdd2.filter(lambda x: x[1]>3).coalesce(1).collectAsMap() #wordcloud needs a dictionary. Hence convert RDD elements to dictionary
  rddOutput = rdd3.coalesce(1).collectAsMap() #wordcloud needs a dictionary. Hence convert RDD elements to dictionary
  wordCloudOutput = WordCloud().generate_from_frequencies(rddOutput)
  wordCloudOutput.to_file('myword.bmp') # save the image to file in current directory
  
  # Stop the spark context
  sc.stop()
