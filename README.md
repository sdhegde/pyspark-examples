# pyspark-examples
assorted spark examples

### **Extracting Spark:**
Download and unpack [Apache Spark](https://spark.apache.org/downloads.html). Download the py files & testdata from this repo.
```
tar -xvf spark-2.3.0-bin-hadoop2.7.tgz
cd spark-2.3.0-bin-hadoop2.7/bin
```

The python files can be submitted to spark cluster using `spark-submit` command

### **Files in this repo:**
#### 1) `minmax.py`:
find the minimum and maximum from distributed dataset using aggregate function.

_data_: 500 numbers in range [-1000, 1000]

_output_: min & max printed on the console

##### **Running**:

```./spark-submit --master local /home/sdh/Downloads/minmax.py ```


#### 2) `sparkWordCloud.py`: 
removes stop-words from all text files using spark's ML feature and creates wordcloud image. 

_data_: sample data is provided in testdata folder

_input_: Takes single text-file or directory of text-files as command line argument

_output_: bmp image at the path: `spark-2.3.0-bin-hadoop2.7/bin/myword.bmp`

##### **Prerequisites:**
1) wordcloud

##### **Installing wordcloud:**
Install wordcloud using pip
   
   `pip install wordcloud`
      
   wordcloud depends on numpy, pillow & matplotlib. If not already installed, you might need to install them manually.
   
   For detailed installation procedure & usage see this [GitHub repo](https://github.com/amueller/word_cloud)

##### **Running:**

```./spark-submit --master local /home/sdh/pyspark-examples/sparkWordCloud.py /home/sdh/pyspark-examples/testdata/```

Once the execution completes, the output image can be found in the current directory i.e. at `spark-2.3.0-bin-hadoop2.7/bin/myword.bmp`

