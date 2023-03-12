
# 标注工具

## software

* python 3.7
* web.py

也提供了requirements.txt文件

## data
任务在./jobs目录下，每个人的任务对应自己姓名全拼的.sql文件。标注结束后数据也会存放在这个文件里。所以请在标注结束后将自己的.sql文件发给我。

## Start web server
在开始前修改./config.json中的"user_id"字段，改成自己的姓名全拼。

```bash
./do_start_server.sh 
```
然后访问http://0.0.0.0:9999/ 进行标注。如果9999端口被占用，可以在./do_start_server.sh里面修改端口号，并且重启浏览器，访问新的地址。

标注任务是判断中文句子是否流利。提交之后会自动跳到下一个句子。
字母键a表示流利，子母键s表示不流利，回车键表示提交，方向键左右表示上一页和下一页。
