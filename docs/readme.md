# 使用教程

## 安装部署

### 1.获取代码

需要的代码：后端的代码、前端构建后的静态文件、docker的compose文件。

### 2.配置环境

#### 2.1前端

REACT_APP_BACKEND_API_HOST：后端的服务器的ip地址

REACT_APP_NOW_WEB_VERSION：当前应用的版本

#### 2.2后端

##### 系统环境变量

HOST_ADDRESS：后端服务器的ip地址

SECRET_KEY：应用秘钥

OWNER_NAME：组织名称

DB_PASSWARD：数据库的密码

##### flask环境变量

FLASK_APP：\__init__
FLASK_ENV：production
FLASK_DEBUG=0

##### oidc_client_secrets

```json
{
    "web": {
      "client_id":"709f90c5037d0813df53",
      "client_secret": "42735c600fcc754a51c08d9547bfc92e1945aa44",
      "auth_uri": "http://localhost:7000/login/oauth/authorize",
      "token_uri": "http://localhost:7000/api/login/oauth/access_token",
      "userinfo_uri": "http://localhost:7000/api/userinfo",
      "issuer": "http://localhost:7000"
    }
}

```

将所有的localhost:7000替换为实际的casdoor路径

#### 2.3docker

+ 各应用的端口映射
+ mysql的数据卷储存位置
+ mysql的密码
+ casdoor中关于mysql的配置

#### 2.4casdoor

##### 创建elab组织

修改名称，修改elab的favicon，主页地址，默认头像

##### 创建elab应用

修改名称，logo链接，所属组织，重定向url，启用注册为false，登录界面html，背景url，表单css，表单位置，主题

##### oidc_client_secrets

将后端中的client_id，client_secret填写为刚注册的elab应用的

#### 2.5nginx

#### 前端

设置为静态文件处理

默认前往index.html主页

#### 后端

将所有开头为api的url导向后端

还有/oidc_callback的url也导向后端

### 3.导入数据

将前后端、docker、nginx全部开启



## 升级

