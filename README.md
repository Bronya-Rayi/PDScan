# PDScan

自动化资产搜集+漏扫平台

纯纯的胶水平台，借用了各个大师傅的优秀工具，完成了子域名查询（oneforall），ip端口扫描（scaninfo)，web站点存活探测（httpx），爬虫+漏扫（crawlergo+xray）的工作。

没有技术含量，但是可以省事

用sqlite做数据库，省去了配置数据库的烦恼

不会写前端，前端略丑。。。

## 安装

现成docker：

```bash
docker pull bronyarayi/pdscan

docker run --init -d -p 8888:8888 pdscan
```

### 自行构建docker

请自行下载工具放置tools目录，目录结构如下：

```bash
├─chrome
│      chromedriver_linux64.zip
│      google-chrome-stable_current_amd64.deb
（chrome请自行安装）
│
├─crawlergo
│      crawlergo
│
├─httpx
│  │  httpx
│  │
│  └─results
├─oneforall
（直接在tools目录下git clone 即可）
├─scaninfo
│  │  scaninfo
│  │
│  └─results
│          portscan_result.txt
│
└─xray
        config.yaml
        module.xray.yaml
        plugin.xray.yaml
        xray （二进制文件请更名）
        xray.yaml
```

Linux Only

理论上Windows也行，但是配环境太麻烦懒得弄了

```bash
docker build . -t pdscan

docker run --init -d -p 8888:8888 pdscan
```



## 使用

默认密码：`admin/123123123`

![image-20221223122118115](.assets/.README.assets/image-20221223122118115.png)


### 添加任务

![image-20221223122156036](.assets/.README.assets/image-20221223122156036.png)

查看任务状态

![image-20221223122227998](.assets/.README.assets/image-20221223122227998.png)

### 任务详情

均可导出csv，若想导出全部数据，先查询99999条（后端懒得写了）

![image-20221223122948608](.assets/.README.assets/image-20221223122948608.png)



内嵌xray报告

![image-20221223145710029](.assets/.README.assets/image-20221223145710029.png)







## Github链接

子域名探测 OneForall
https://github.com/shmilylty/OneForAll

端口扫描 scaninfo
扫的贼快，还比较准，想换成别的工具的师傅可以自行更换
https://github.com/redtoolskobe/scaninfo

Web存活探测 httpx
https://github.com/projectdiscovery/httpx

Web爬虫 crawlergo
https://github.com/Qianlitp/crawlergo

Web漏扫 xray
https://github.com/chaitin/xray


# 免责声明

本工具仅面向合法授权的企业安全建设行为，如您需要测试本工具的可用性，请自行搭建靶机环境。

在使用本工具进行检测时，您应确保该行为符合当地的法律法规，并且已经取得了足够的授权。请勿对非授权目标进行扫描。

如您在使用本工具的过程中存在任何非法行为，您需自行承担相应后果，我们将不承担任何法律及连带责任。

在安装并使用本工具前，请您务必审慎阅读、充分理解各条款内容，限制、免责条款或者其他涉及您重大权益的条款可能会以加粗、加下划线等形式提示您重点注意。 除非您已充分阅读、完全理解并接受本协议所有条款，否则，请您不要安装并使用本工具。您的使用行为或者您以其他任何明示或者默示方式表示接受本协议的，即视为您已阅读并同意本协议的约束。

另外，麻烦溯源的不要再溯我了，我也不知道站是谁日的，至少不是我干的，开源工具溯作者是个什么鬼溯源方法😅
