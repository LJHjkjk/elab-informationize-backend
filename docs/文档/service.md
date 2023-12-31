# 服务

## 一、申请

### 1.1总览

处理各种申请。

申请就是有人提出申请，然后给指定的人发送任务，然后处理，处理完成后这个任务结束。

对于申请的需要记录的信息：

+ 发起人
+ 发起日期
+ 处理结果
+ 处理人
+ 处理日期
+ 申请的附件
+ 是否完成

申请的种类有多种，每一种对应着一种具体的事物，例如有加入申请、退出申请。每一种申请都对应着一组处理人，这组处理人都可以处理对应的申请。当有人发起申请时，所有的处理人都会受到处理任务，当任何一位处理人处理了申请后，处理任务就完成了，所有人的处理任务就消失了。



==具体流程==：有对应处理申请的职务：后面放着这个职务对应的人。当有人发出申请后，对应的申请中心的未处理记录一条申请。当有处理人上线后，检索其对应的职务是否有未处理，当有时将处理发送给处理人。处理人处理后记录结果，然后将这个申请修改为已做。但是事件不能做完就没有了，处理完事件之后需要一个回调函数，执行对应的处理结果（可能是删除、修改新增数据等）。最后会发送一个邮件通知申请人。

使用mysql表来记录各种申请。



### 1.2 科研助手申请

#### 具体需求

用户下载一个表格模板，填写完成后上传。



### 1.3 报销申请

#### 具体需求

申请报销比其他的申请多一个内容。

首先用户提出申请，然后管理员通过申请。然后需要用户提交一个发票，这个发票发送给处理人和物料系统。比其他的申请多了一个提交给用户的流程。

#### 实现

当用户申请通过之后，在申请人处添加一个任务：上传发票。当用户上传完发票之后，这个任务完成，删除。



## 二、任务

上面的申请中所有的处理人是固定的，也就是说会收到申请处理的待办事项的人也是固定的。但是向报销申请中，因为需要上传发票，也就是申请人也会有任务处理，因此这个事件处理的人不固定。因此有了任务，任务相比起申请更加的灵活，处理的任务的人不是固定的，而是根据情况动态变化。

任务将建立一个新表，所有用户的任务均在此，使用外键相连。用户可以在此检索自己的任务。任务也在待办事项中。使用起来和待办事项没有任何的区别。

任务不储存任何的数据，只是一个通知用户办事的接口。任务就像一个指针一样，最终要导向其他的办事，例如申请。



