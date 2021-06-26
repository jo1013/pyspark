# AIRFLOW


## 0\. 환경셋팅

```
$ git clone https://github.com/jo1013/Airflowex.git 
$ cd Airflow
$ docker pull jo1013/Airflowex:0.03
```

## 1\. 실행 명령어

```
$ docker run -it -d -p 8090:8080 -v ~/workspace:/home -e LC_ALL=C.UTF-8 --name airflow6 jo1013/airflowex:0.06

$ docker run -it -d -p [연결로컬포트]:[연결도커포트] -v [로컬디렉터리]:[컨테이너디렉터리] -e LC_ALL=C.[인코딩방식] --name [설정할이름] [dockerhubid]/[imagename]:[tag]
```

## 2\. 배쉬 접속하기

```
$ docker exec -it airflow4 bash

$ docker exec -it [설정이름] bash
```

* postgreqs 시작
```
$ service postgresql start
```


## 2.5. DB 생성 후 


```
$ sudo su - postgres
$ psql
$ CREATE DATABASE airflow;
$ CREATE USER timmy with ENCRYPTED password '0000';
$ GRANT all privileges on DATABASE airflow to timmy;
```


#### postgres 유저의 airflow db접속

```
$ \c airflow
$ GRANT all privileges on all tables in schema public to timmy;
$ \q        
$ exit
```

## 3\. postgre cluster 설정

```
$ pg_createcluster 13 main 
$ pg_ctlcluster 13 main start
```

## 4\. postgresql 설정

```
# $ cd /etc/postgresql/13/main
# $ nano pg_hba.conf
```

#### 아래와 같이 수정

```
# IPv4 local connections:                                                          
host        all             all             0.0.0.0/0               md5 
```

#### 재시작

```
$ service postgresql restart
```

# airflow 수정하기

## 1\. 연결 DB 변경

```
$ nano /root/airflow/airflow.cfg

```

아래와 같이 수정한다.

```
# dags_folder = /root/airflow/dags 
dags_folder = /home/dags 

# base_log_folder = /root/airflow/logs 
base_log_folder = /home/logs 

# default_timezone = utc 
default_timezone = Asia/Seoul 

# executor = SequentialExecutor 
executor = LocalExecutor 

# sql_alchemy_conn = sqlite:////root/airflow/airflow.db 
sql_alchemy_conn = postgresql+psycopg2://timmy:0000@172.17.0.2/airflow

```

* sql\_alchemy\_conn에 localhost를 적으면 해당 컨테이너를 찾아가지 못하기 때문에 host의 ip 혹은 postgres컨테이너의 ip를 넣어줘야한다.

#### ip 확인

```
$ ifconfig

```

## 2\. 외부접속 허용

```
$ cd /etc/postgresql/13/main
$ nano pg_hba.conf 
```

#### 아래처럼 수정

```
IPv4 local connections:                                                          
host        all             all             0.0.0.0/0               md5 
```

```
$ service postgresql restart
```

## 3\. 폴더 만들기

```
$ cd Airflow
$ mkdir dags
$ mkdir logs
```

## 4\. airflow db 초기화 (로그인 안될때 이용)

```
$ airflow db init
```

## 5\. 변경 내용 저장

```
$ docker commit postgres postgres:airflow
```

## 6\. 계정 생성 py 파일 실행

```
$ cd home

$ nano makeuser.py  
```

makeuser.py를 ~/airflow\_home 위치로 수정

```
$ cp makeuser.py airflow
```

#### makr user.py 에 넣을 내용 아래 복사 (아이디,비밀번호 수정)


```
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

user.email = 'sunny@test.com'
user.password = 'sunny'
user.superuser = True
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()

```

---

####  또는 터미널에서 직접 계정생성
#### (아이디,비밀번호 수정)

```
$ airflow users create \
          --username admin \
          --firstname FIRST_NAME \
          --lastname LAST_NAME \
          --role Admin \
          --email admin@example.org

```





#### airflow 시작

```
$ airflow webserver
```

```
airflow db init 
```

## 참고 자료



### Creating a Database Cluster

```
-   In file system terms, a database cluster is a single directory under which all data will be stored. We call this the data directory or data area. It is completely up to you where you choose to store your data. There is no default, although locations such as /usr/local/pgsql/data or /var/lib/pgsql/data are popular. The data directory must be initialized before being used, using the program initdb which is installed with PostgreSQL.
-   보통 위의 글중에 나온 경로와 같이 경로 설정을 하지만 꼭 그럴 필요는 없다는 내용~

---
```

## Airflow 명명법
### 다음은 Airflow 업무 흐름을 설계할 때 사용하는 몇 가지 용어에 관한 간략한 개요이다.

* Airflow DAG는 태스크로 구성된다.

* 각 태스크는 오퍼레이터 클래스를 인스턴스화하여 만든다. 구성한 오퍼레이터 인스턴스는 다음과 같이 태스크가 된다. my_task = MyOperator(...)

* DAG가 시작되면 Airflow는 데이터베이스에 DAG 런 항목을 만든다.

* 특정 DAG 런 맥락에서 태스크를 실행하면 태스크 인스턴스가 만들어진다.

* AIRFLOW_HOME은 DAG 정의 파일과 Airflow 플러그인을 저장하는 디렉터리이다.



출처 : https://aldente0630.github.io/data-engineering/2018/06/17/developing-workflows-with-apache-airflow.html
















# pyspark


``` 
$ docker pull jo1013/pyspark:0.05
```

##  pyspark 컨테이너만 실행 
```
$ docker run -it --rm -p 8888:8888 -p 8000:8000 -v ~/workspace:/home jo1013/pyspark:0.05
```


### 쥬피터 노트북 실행 포트 8888 
```
$ jupyter notebook --allow-root --ip=0.0.0.0 --port=8888 --no-browser
```


### 컨테이너 베쉬 접속
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

```
$ docker run --name db-mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql
```

### airflow dag 리스트 보기 
```
$ airflow dags list애
```



### task list 보기 

```
$ airflow tasks list
```
