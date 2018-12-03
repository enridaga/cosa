import functions

import os
import csv
import io
import sys
reload(sys)
# FIXME Find a way to set this outside ...
sys.path.append("/usr/local/Cellar/apache-spark/2.3.2/libexec/python")
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from pyspark.mllib.feature import Word2VecModel

from pyspark.sql import SparkSession
from pyspark import SparkContext  
from pyspark import SparkConf

class Model:
    _word2vec = None
    def __init__(self, modelFile):
        sconf = SparkConf()
        # FIXME Find a way to set this outside ...
        sconf.set("spark.driver.memory", "8g")
        sconf.set("spark.executor.memory", "8g")
        sconf.set("spark.kryoserializer.buffer.max","1024")
        # sconf.set("spark.akka.frameSize","2000")
        sconf.set("spark.rpc.message.maxSize","2000")
        sconf.set("spark.driver.maxResultSize","0")
        sconf.set("spark.default.parallelism","180")
        sconf.set("spark.dynamicAllocation.enabled","true")
        sconf.set("spark.io.compression.codec","snappy")
        sconf.set("spark.rdd.compress","true")
        sconf.set("spark.shuffle.service.enabled","true")
        sconf.set("spark.sql.pivotMaxValues", "1000000")    
        sconf.set("spark.sql.autoBroadcastJoinThreshold", "-1") 
        ss = SparkSession.builder.master("local").appName("Generate Embeddings").config(conf=sconf).getOrCreate()
        sc = ss.sparkContext
        sc.setLogLevel("INFO")
        Logger= ss._jvm.org.apache.log4j.Logger
        L = Logger.getLogger(__name__)
        try:
            self._word2vec = Word2VecModel.load(sc, modelFile)
        except Exception as e:
            L.error( "Exiting: " + str(e))
            sc.stop()
            exit()
    
    def similarToTerm(term, num):
        first=lambda x: x[0]
        # print "Looking for syns of " + depos(key)
        if len(key[0:key.find('[')]) < 3:
            L.debug(  "Skipping short string '%s', length %d" % (key,len(key)))
            return {}
        try:
            L.trace("Processing %s" % term)
            key=key.decode(encoding)
        except UnicodeError:
            L.debug( "Skipping invalid string '%s', length %d bytes" % (key, len(key)))
            return {}
        terms = {term: 1.0}
        try:
            terms = self._word2vec.findSynonyms(key, num)
        except UnicodeDecodeError:
            L.debug(  "unicode error on string '%s', length %d bytes" % (key, len(key)))
        except Exception as e:
            pass #print " - not found (exception)"
        except Error as r:
            pass #print " - error"
    
        return terms
        
        