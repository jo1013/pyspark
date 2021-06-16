# pyspark


``` 
$ docker pull jupyter/pyspark-notebook
```


~~$ docker run -it --rm -p 8888:8888 -v pwd:/home jupyter/pyspark-notebook~~



```
$ docker run -it --rm -p 8888:8888 -p 8000:8000 -v ~/workspace:/home jo1013/pyspark:0.04
```

```
$ jupyter notebook --allow-root --ip=0.0.0.0 --port=8888 --no-browser
```