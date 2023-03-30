
# 流利度标注工具

## software

* python 3.7
* web.py

也提供了requirements.txt文件

## data

任务在./jobs目录下，每个人的任务对应自己姓名全拼的.sql文件。标注结束后数据也会存放在这个文件里。所以请在标注结束后将自己的.sql文件发给我。

## Start web server

在开始前修改./config.json中的"user_id"字段，改成自己的姓名全拼。

运行如下代码

```bash
./do_start_server.sh 
```
然后访问http://0.0.0.0:9999/ 进行标注。如果9999端口被占用，可以在./do_start_server.sh里面修改端口号，并且重启浏览器，访问新的地址。
如果在服务器上运行，可以访问服务器的ip地址加上对应的端口号。

标注任务是判断中文句子是否流利。提交之后会自动跳到下一个句子。
字母键a表示”流利“，子母键s表示”不流利“，子母键d表示”不确定“，回车键表示提交，方向键左右表示上一页和下一页。

## 标注示例
### 流利
标准是中文流畅，翻译准确。
【流利】 中文：中文英国北威尔士海滩上的古老巨石。 英文：Ancient boulders on a beach in north wales uk
【流利】 中文：在空旷的花园里荡秋千。           英文：Swings on an empty garden


### 不流利
中文不流畅，翻译有误。
【不流利】 中文：雪橇上的圣诞老人与雪花飞舞的驯鹿的数字合成。   英文：Digital composite of santa in sleigh with reindeer flying with snowflakes
【不流利】 中文：希腊海滩海浪冲击海岸。                     英文：Greece beach waves crashing the shore
【不流利】 中文：背景上穿着蓝色裙子的女人的腿的小狗。           英文：Little dog with the legs of a woman in a blue skirt on background
【不流利】 中文：公园长椅上坐着智能手机的美女。                 英文：Pretty woman with smartphone sitting on bench in the park 

### 不确定
不能判断出来具体是流利不流利的可以标为”不确定“。