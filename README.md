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



### mysql run 
```
$ docker run -n db-mysql -e MYSQL_DATABASE=testdb - MYSQL_ROOT_PASSWORD=root - TZ=Asia/Seoul -p 3306:3306 -c --character-set-server=utf8mb4 -c --collation-server=utf8mb4_unicode_ci 
```


docker run --name db-mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql


