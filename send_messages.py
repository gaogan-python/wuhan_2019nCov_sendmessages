import requests,json,re,os,time

class Yqts(object):
	
    def __init__(self):
        self.url = "https://3g.dxy.cn/newh5/view/pneumonia"
    def send_dingmessage(self,content,content_p):
        dingding_url = "https://oapi.dingtalk.com/robot/send?access_token=*****"#Your Dingding’s access_token"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        text= "#### %s 感染: \n >全国截止 %s: \n\n > - 确诊病例:%s \n\n > - 疑似病例:%s \n\n > - 死亡人数:%s \n\n > - 治愈人数:%s  \n\n > - "\
              "\n > %s数据： \n\n > - 确诊病例:%s \n\n > - 疑似病例:%s \n\n > - 死亡人数:%s \n\n > - 治愈人数:%s  \n\n > -"\
              "\n > 各城市明细数据： \n\n > - 确诊病例:%s \n\n > - 疑似病例:%s \n\n > - 死亡人数:%s \n\n > - 治愈人数:%s  \n\n > -"\
              "![screenshot](%s)\n  > "\
              "![screenshot](%s)\n  > "\
              "###### 数据来自 [丁香园-丁香医生](https://3g.dxy.cn/newh5/view/pneumonia)"\
              %(content['virus'],time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(content['modifyTime']/1000)),\
              content['confirmedCount'],content['suspectedCount'],content['deadCount'],content['curedCount'],\
              content_p['provinceName'],content_p['confirmedCount'],content_p['suspectedCount'],content_p['deadCount'],content_p['curedCount'],\
              content['imgUrl'],content['dailyPic'])
        post_data = {"msgtype": "markdown","markdown": {"title":"丁香园全国疫情数据新闻","text": text}}
        requests.post(dingding_url, headers=headers, data=json.dumps(post_data))
    def get_dxy_data(self):
        source_html = requests.get(self.url).content.decode('utf8')
        country_json = self.re_match('window.getStatisticsService = (.*?)}catch',source_html)
        provinces_json = self.re_match('window.getAreaStat = (.*?)}catch',source_html)
        return country_json,provinces_json
    def re_match(self,match_string,source_string):
    	match_data = re.search(match_string,source_string).group(1)
    	return json.loads(match_data, encoding='utf8')
    def decide_data(self,content):
        if os.path.exists('data.json'):
            filename = 'data.json'
            with open(filename) as file_obj:
                text = json.load(file_obj)
                file_obj.close()
                if text == content:
                    return False
                else:
                    os.remove('data.json')
                    with open(filename,'w') as new_file_obj:
                        json.dump(content,new_file_obj)
                        new_file_obj.close()
                    return True
        else:
            filename = 'data.json'
            with open(filename,'w') as file_obj:
                json.dump(content,file_obj)
                file_obj.close()
            return True

if __name__ == '__main__':
    yqts = Yqts()
    country_result,provinces_result = yqts.get_dxy_data()
    if yqts.decide_data(country_result):
    	for i in range(0,len(provinces_result)-1):
            if provinces_result[i]['provinceName'] == '吉林省':
                print(country_result,provinces_result[i])
                yqts.send_dingmessage(country_result,provinces_result[i])
    else:
    	print("暂无数据更新！")