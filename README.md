# pyspark


``` 
$ docker pull jupyter/pyspark-notebook
```
~~$ docker run -it --rm -p 8888:8888 -v pwd:/home jupyter/pyspark-notebook~~


```
$ docker run --rm -p 8888:8888 --name jupyter -e NB_USER=felipebn -e CHOWN_HOME=yes -e CHOWN_EXTRA_OPTS='-R' --user root -w /home -v ~/pyspark:/home jupyter/pyspark-notebook

```


