# pyspark


``` 
$ docker pull jupyter/pyspark-notebook
```
~~$ docker run -it --rm -p 8888:8888 -v pwd:/home jupyter/pyspark-notebook~~


```
$ docker run --rm -p 8888:8888 --user root -w /home -v ~/pyspark:/home jupyter/pyspark-notebook
```




