FROM ubuntu
workdir /app
copy . /app
run apt update -y && apt install apt-utils -y &&  apt install libmariadb3 libmariadb-dev apt-utils python3 python3-pip -y
run pip install -r requirements.txt 
run  pip3 install mariadb==1.1.4
expose 5000
entrypoint python3 main.py
