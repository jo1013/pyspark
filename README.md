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


## 컨테이너 베쉬 접속
```
$ docker exec -it cef2db19cd8b bash
```

### mysql도 같이 작동
```
$ docker-compose up 
```