### matrix 
### 操作手册

#### 运行看板（dashboard） 
cd dashboard 
python3 app.py
http://127.0.0.1:8002/dashboard

#### 运行总服务端
python3 fl_main_app.py -p 8000 

#### 运行安全聚合起

python3 ./fl_sec_app.py -p 8001

#### 运行客户端

 python3 fl_cli_app.py -p 8003 -n 0
 python3 fl_cli_app.py -p 8004 -n 1
 python3 fl_cli_app.py -p 8003 -n 2
 ...
 客户端数量配置见 hosts.yml
