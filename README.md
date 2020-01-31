# wuhan_2019nCov_send-messages

武汉肺炎2019nCoV疫情数据事实推送脚本，数据基于丁香园·丁香医生。

## 使用说明

### 环境要求

- Python3
- 钉钉群机器人（access_token）

### 推送配置

#### 钉钉消息推送机器人

第8行，将「"*********"」Your Dingding’s access_token 换成你的 access_token即可。
```
dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=填写access_token"
```

#### 推送内容

- 推送全国统计数据
- 自定义所在省份数据

第55行，可自定义省份名称推送省份数据。

```
 provinces_result[i]['provinceName'] == "自定义省份名称"
```

#### 内容重复检测

第29行 decide_data 方法根据将请求数据写入data.json文件，每次检测判断请求数据是否有变化，从而确定是否进行数据推送

### 定时执行

可以通过 Linux cron定时任务执行此脚本。

```
*/10 * * * * /usr/local/bin/python send_messages.py
```