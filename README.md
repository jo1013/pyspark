# Airflow + PySpark 설치 및 실행 가이드

> 이 가이드는 우분투 환경을 기준으로 작성되었습니다.

## 목차
- [환경 설정](#환경-설정)
- [Docker 실행](#docker-실행)
- [Airflow 설정](#airflow-설정)
- [PostgreSQL 설정](#postgresql-설정)
- [Airflow 계정 생성](#airflow-계정-생성)
- [PySpark 실행](#pyspark-실행)
- [MySQL 설정](#mysql-설정)
- [유용한 명령어](#유용한-명령어)
- [SSH 설정](#ssh-설정)

## 환경 설정

### Docker 이미지 다운로드
```bash
docker pull jo1013/pyspark:0.05
docker pull jo1013/airflow:0.07
docker pull mysql:8.0.17
```

### 저장소 클론
```bash
git clone https://github.com/jo1013/pyspark.git
cd pyspark
```

## Docker 실행

### 모든 컨테이너 실행
```bash
docker-compose up  # mysql, pyspark, airflow(postgresql) 컨테이너 실행
```
> `docker-compose.yml`에서 볼륨 설정을 본인 환경에 맞게 수정하세요.

### 컨테이너 접속
```bash
docker exec -it airflow bash
docker exec -it [컨테이너_이름] bash
```

## Airflow 설정

### 디렉토리 설정 변경
`airflow.cfg` 파일을 열어 설정을 변경합니다:
```bash
nano /root/airflow/airflow.cfg
```

다음 항목을 수정합니다:
```
# 디렉토리 설정
dags_folder = /home/pyspark/airflow/dags
base_log_folder = /home/pyspark/airflow/logs
plugins_folder = /home/pyspark/airflow/plugins

# 시간대 설정
default_timezone = Asia/Seoul

# 실행자 설정
executor = LocalExecutor
```

### Airflow 단독 실행
```bash
# 대화형 모드
docker run -it -d -p 8090:8080 -v ~/workspace:/home -e LC_ALL=C.UTF-8 --name airflow6 jo1013/airflowex:0.06

# 일반 형식
docker run -it -d -p [로컬포트]:[컨테이너포트] -v [로컬디렉토리]:[컨테이너디렉토리] -e LC_ALL=C.[인코딩방식] --name [컨테이너이름] [이미지명]:[태그]
```

### Airflow 웹서버 실행
```bash
# 컨테이너 내부에서 실행
airflow webserver

# 백그라운드로 실행
docker exec -it -d airflow airflow webserver
```
> 웹 인터페이스는 `http://localhost:8090`으로 접속할 수 있습니다.

## PostgreSQL 설정

### PostgreSQL 시작
```bash
service postgresql start

# 백그라운드로 실행
docker exec -it -d airflow service postgresql start
```

### 데이터베이스 및 사용자 생성
```bash
sudo su - postgres
psql
CREATE DATABASE airflow;
CREATE USER timmy with ENCRYPTED password '0000';
GRANT all privileges on DATABASE airflow to timmy;
\c airflow
GRANT all privileges on all tables in schema public to timmy;
\q
exit
```

### PostgreSQL 클러스터 설정
```bash
pg_createcluster 13 main
pg_ctlcluster 13 main start
```

### 외부 접속 허용 설정
```bash
cd /etc/postgresql/13/main
nano pg_hba.conf
```

다음 내용으로 수정:
```
# IPv4 local connections:
host    all    all    0.0.0.0/0    md5
```

PostgreSQL 재시작:
```bash
service postgresql restart
```

### Airflow 데이터베이스 연결 설정
`airflow.cfg` 파일에서 다음 항목을 수정:
```
# SQL Alchemy 연결 설정
sql_alchemy_conn = postgresql+psycopg2://timmy:0000@localhost/airflow
```
> 컨테이너에서 PostgreSQL이 동작하므로 `localhost`로 설정합니다.

### 컨테이너 IP 확인
```bash
ifconfig
```

## Airflow 계정 생성

### 데이터베이스 초기화
```bash
airflow db init
```

### 방법 1: Python 스크립트로 계정 생성
`makeuser.py` 파일 생성:
```bash
cd home
nano makeuser.py
```

다음 내용 추가:
```python
import airflow
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser

user = PasswordUser(models.User())
user.username = 'admin'
user.email = 'sunny@test.com'
user.password = 'sunny'
user.superuser = True
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
```

### 방법 2: 명령줄에서 계정 생성
```bash
airflow users create \
  --username admin \
  --firstname FIRST_NAME \
  --lastname LAST_NAME \
  --role Admin \
  --email admin@example.org \
  --password admin
```

## PySpark 실행

### PySpark 컨테이너 단독 실행
```bash
docker run -it --rm -p 8888:8888 -p 8000:8000 -v ~/workspace:/home jo1013/pyspark:0.05
```

### Jupyter Notebook 실행
```bash
jupyter notebook --allow-root --ip=0.0.0.0 --port=8888 --no-browser
```

## MySQL 설정

### MySQL 컨테이너 실행
```bash
docker run --name db-mysql -e MYSQL_ROOT_PASSWORD=root -d -p 3306:3306 mysql

# 옵션 추가 버전
docker run -n db-mysql -e MYSQL_DATABASE=testdb -e MYSQL_ROOT_PASSWORD=root -e TZ=Asia/Seoul -p 3306:3306 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

## 유용한 명령어

### Airflow 명령어
```bash
# DAG 목록 확인
airflow dags list

# 태스크 목록 확인
airflow tasks list [dag_id]
```

## SSH 설정

### SSH 키 생성
```bash
ssh-keygen -t rsa
```
> 이 명령은 `id_rsa`(비밀키)와 `id_rsa.pub`(공개키)를 생성합니다.

### 사용자 추가 및 설정
```bash
# 사용자 추가
useradd airflow

# 사용자로 전환
su - airflow

# SSH 디렉토리 생성
mkdir .ssh

# 폴더 권한 설정
chown -R airflow:airflow /home/workspace
```

## Airflow 용어 정리

- **DAG(Directed Acyclic Graph)**: 태스크로 구성된 워크플로우
- **Task**: 오퍼레이터 클래스의 인스턴스
- **DAG Run**: DAG가 실행되면 생성되는 데이터베이스 항목
- **Task Instance**: 특정 DAG 실행 컨텍스트에서 태스크가 실행될 때 생성
- **AIRFLOW_HOME**: DAG 정의 파일과 Airflow 플러그인을 저장하는 디렉토리
