# AIRFLOW + PYSPARK

이 글은 우분투 기준으로 작성되었습니다.

---

## 0\. 환경셋팅

### docker 환경 다운

```
$ docker pull jo1013/pyspark:0.05
$ docker pull jo1013/airflow:0.07
$ docker pull mysql:8.0.17
```


### git clone (글쓴이는 /home/workspace 에서 실행)

```
$ git clone https://github.com/jo1013/pyspark.git
$ cd pyspark
```

## 1\. 실행 명령어 

``` 
$ docker-compose up  ## mysql pyspark airflow(postgresql) 컨테이너실행
```
* (docker-compose.yml에서 3개의 container는 본인의 volumes에 맞게 수정한다.)

## 2\. 다른 터미널로 컨테이너 접속하기

```
$ docker exec -it airflow bash

$ docker exec -it [설정이름] bash
```

## 3\.  postgresql 구동

* postgreqs 시작


```
$ service postgresql start
```

#### 컨테이너를 계속 띄우기 싫다면 ?
* 로컬 터미널에서
```
$ docker exec -it -d airflow service postgresql start 
```

## 4\. 연결 디렉토리 변경

```
$ nano /root/airflow/airflow.cfg
```

### 자신의 볼률 설정에 맞게 수정 (글쓴이와 폴더설정 같을 경우 고칠 필요 X)

```
# dags_folder = /root/airflow/dags 
dags_folder = /home/pyspark/airflow/dags

# base_log_folder = /root/airflow/logs 
base_log_folder = /home/pyspark/airflow/logs 

# plugins_folder = /root/airflow/plugins
plugins_folder = /home/pyspark/airflow/plugins

# default_timezone = utc 
default_timezone = Asia/Seoul 

# executor = SequentialExecutor 
executor = LocalExecutor 

```
## 5\. 실행


### airflow 시작 명령어


```
$ airflow webserver
```
#### 컨테이너를 계속 띄우기 싫다면 ?
* 로컬 터미널에서
```
$ docker exec -it -d airflow airflow webserver
```



* https://localhost:8090으로 접속하면 airflow화면을 볼 수 있다. 
 
* id : admin
* password : admin



---
---
## AIRFLOW


### airflow만  실행 명령어
```
$ cd Airflow
$ docker run -it -d -p 8090:8080 -v ~/workspace:/home -e LC_ALL=C.UTF-8 --name airflow6 jo1013/airflowex:0.06
$ docker run -it -d -p [연결로컬포트]:[연결도커포트] -v [로컬디렉터리]:[컨테이너디렉터리] -e LC_ALL=C.[인코딩방식] --name [설정할이름] [dockerhubid]/[imagename]:[tag]
```



### DB account 설정 및 권한 설정
```
$ sudo su - postgres
$ psql
$ CREATE DATABASE airflow;
$ CREATE USER timmy with ENCRYPTED password '0000';
$ GRANT all privileges on DATABASE airflow to timmy;
```


### postgres 유저의 airflow db접속

```
$ \c airflow
$ GRANT all privileges on all tables in schema public to timmy;
$ \q        
$ exit
```

### postgre cluster 설정

```
$ pg_createcluster 13 main 
$ pg_ctlcluster 13 main start
```

## postgresql 설정

```
# $ cd /etc/postgresql/13/main
# $ nano pg_hba.conf
```

### 아래와 같이 수정


### 모든 포트에 대해 열어놓기 (추후 수정 필요)
```
# IPv4 local connections:                                                          
host        all             all             0.0.0.0/0               md5 
```

### DB 재시작

```
$ service postgresql restart
```

### Arflow 수정하기



```
# sql_alchemy_conn = sqlite:////root/airflow/airflow.db 
# sql_alchemy_conn = postgresql+psycopg2://timmy:0000@172.17.0.2/airflow    

# docker hub에서는 가능햇으나 docker-compose에서는 단일 컨테이너과 IP Adress가 달라진다.

sql_alchemy_conn = postgresql+psycopg2://timmy:0000@localhost/airflow
# --> 같은 docker (컨테이너) 내에서 postgresql이 작동하므로 localhost로 고친다.
```



* sql\_alchemy\_conn에 localhost를 적으면 해당 컨테이너를 찾아가지 못하기 때문에 postgres컨테이너의 IP를 넣어줘야한다.

### IP 확인

```
$ ifconfig
```

## 외부접속 허용

```
$ cd /etc/postgresql/13/main
$ nano pg_hba.conf 
```

#### 아래처럼 수정

```
IPv4 local connections:                                                          
host        all             all             0.0.0.0/0               md5 
```

## postgresql 재시작
```
$ service postgresql restart
```

##  폴더 만들기

```
$ cd Airflow
$ mkdir dags
$ mkdir logs
```

##  airflow db 초기화 (로그인 안될때 이용)

```
$ airflow db init
```

##  변경 내용 저장

```
$ docker commit postgres postgres:airflow
```

## 계정 생성 py 파일 실행

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






* db 초기화 (postgres 'airflow' table )
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

-> 버전이 달라서인지  위 출처의 튜토리얼을 따라하다보면  import 오류가 발생하는데    dags/test_operators.py 에서 

```
from airflow.operators import MyFirstOperator
```
를  

```
from my_operators import MyFirstOperator

from [filename] import [classname]
```
으로 고쳐주면 된다. 

버전 변경으로 인한 오류로 보인다.?




---------------------------------------------------








# pyspark



#### pyspark 컨테이너만 실행 

```
$ docker run -it --rm -p 8888:8888 -p 8000:8000 -v ~/workspace:/home jo1013/pyspark:0.05
```

### pyspark bash 접속

```
$ docker exec -it py_spark bash
$ docker exec -it [container id or container name] bash
```

### 쥬피터 노트북 실행 포트 8888 (pyspark 컨테이너 내에서 실행)
```
$ jupyter notebook --allow-root --ip=0.0.0.0 --port=8888 --no-browser
```



### mysql만 run   run 

```
$ docker run -n db-mysql -e MYSQL_DATABASE=testdb - MYSQL_ROOT_PASSWORD=root - TZ=Asia/Seoul -p 3306:3306 -c --character-set-server=utf8mb4 -c --collation-server=utf8mb4_unicode_ci 
```

```
$ docker run --name db-mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql
```

### airflow dag 리스트 보기 
```
$ airflow dags list
```

### task list 보기 

```
$ airflow tasks list
```



### 쥬피터 노트북 실행 포트 8888 
```
$ jupyter notebook --allow-root --ip=0.0.0.0 --port=8888 --no-browser
```


---

# mysql Container db 연결법

로컬터미널에서 ip 주소 확인
```
$ ifconfig
```
### 로컬에 연결되 있으므로 연결 db호스트를 로컬 ip주소를 입력하면된다.

# 다른 컨테이너로 파이썬파일 실행할떄 ssh 사용


## Airflow dag command에 다른컨테이너 명령 실행 방법

## 해법 :   ssh로 명령내리기 

---

*그전에 해당컨테이너와 명령어 받는 컨테이너에 ssh 설치하고명령어 받는 컨테이너에 /etc/ssh/sshd_config 에서 PermitRootLogin 을 yes로 고쳐주어야함 (절대X) (보안 위험)

### ssh 접속 정보를 코드에 두는 것을 피하기 위해 
1.  Airflow DB에 접속정보를 저장하고 operator에서는 불러서 쓸 수 있는 SSH Connection을 설정해서 사용
2. 추가로 가능하다면 외부 secret manager 형 서비스를 사용하시는 것을 권장드립니다.


```
$ ssh-keygen -t rsa
```

* id_rsa: 비밀키
* id_rsa.pub: 공개키


실행하는 컨테이너에서 사용자를 추가 
```
$ useradd airflow
$ useradd [유저]
```
```
su -  airflow
```
```
$  mkdir .ssh
```

### 사용 폴더 권한 허용
```
$ chown -R airflow:airflow /home/workspace
$ chown -R 계정명:계정명 [홈디렉터리경로]
```
