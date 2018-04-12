"""
Apache spark python code for finding minimum and maximum number in the distributed data.
Each node finds the minimum and maximum under the RDD partition it sees and the result is aggregated to get the final result

Data: 500 random numbers in the range of [-1000, 1000]
Result is printed on the console
"""

from __future__ import print_function
import random
from pyspark.sql import SparkSession
from pyspark.sql import Row


# Local function which is used for processing each RDD partition. i.e. min and max is found for each RDD partition
def localFunction(localres, ele):
  if(localres[2] == 1):
    min = ele
    max = ele
  else:  
   if(ele < localres[0]):
     min = ele
   else:
     min = localres[0]
   if(ele > localres[1]):
     max = ele
   else: 
     max = localres[1]
  #print("--------------------", localres,ele,min,max)
  return (min, max, 0)

# Global function which is used for aggregating the result of localFunction(). i.e. result from the RDD partitions are aggregated to find the global min & max
def aggregateFunction(res1, res2):
 if(res1[2] == 1):
   min = res2[0]
   max = res2[1]
 else:
  min = res1[0]
  max = res1[1]
  if(res1[0] < res2[0]):
    min = res1[0]
  else:
    min = res2[0]
  if(res1[1] > res2[1]):
    max = res1[1]
  else:
    max = res2[1]
 
 #print("---------", res1[0], res1[1])
 return (min, max, 0)
  
if __name__ == "__main__":
  spark = SparkSession.builder.appName("Min Max").getOrCreate()
  sc = spark.sparkContext

  # create random numbers between -1000 & 1000
  randArray = []
  for i in range(500):
    randArray.append(random.randint(-1000,1000))

  #create distributed data from randArray i.e. create RDD & with 4 partitions. Call the aggregate() with initial values (0,0,1)... 1 is just a flag
  result = sc.parallelize(randArray,4).aggregate((0,0,1),localFunction, aggregateFunction)
  # res = g.collect()
  print("Min: %r .............. Max: %r" % (result[0],result[1]))

  # Stop the spark context
  sc.stop()
