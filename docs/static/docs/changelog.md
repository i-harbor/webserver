## v0.4.4
* 存储桶和桶归档model增加字段type，及clearbucket命令只清理原生桶；
* 兼容s3 api使用说明网页视图实现；
* ceph rados读写代码修改和单元测试代码；
* 其他一些细节和代码优化；

## v0.4.3
* s3兼容api文档
* obj元数据查询条件修改
* ftp upload calculate md5
* obj元数据api返回数据增加rados信息

## v0.4.2
* add put object api
* 网页端上传改为使用put object api
* get object api未认证可以下载公有桶对象

## v0.4.1
* 升级到jquery3,bootstrap4
* ftp服务解决ls文件报错bug

## v0.4.0
* 国际化多语言   

## v0.3.11
* 桶统计API超级用户可以访问所有桶
* ftp服务list dir最多可返回两万条数据
* 目录对象列表网页实现跳转到指定页码

## v0.3.10
* 时间统一ISO格式   

## v0.3.9
* 桶API同时支持桶ID和桶name   
* 创建空对象元数据API   
* 自动同步更新对象大小API   

## v0.3.8
* 桶备注功能

## v0.3.7 
* 弃用旧jwt和API文档库相关代码移除   
* 桶列表网页桶资源统计查看实现   

## v0.3.6
* 多ceph pool实现，桶记录自己的pool name

## v0.3.5
* 使用drf-yasg生成API文档
* 新的jwt api， 旧api弃用
* evcloud v3版
* 带密码的分享

## v0.3.4
* clearbucket命令修改，增加selectobject命令，桶归档桶名去除唯一索引   
* 对象rados存储信息API obj-rados   
* 日志库concurrent_log_handler和日志相关修改   

## v0.3.3
* 去除桶软删除，增加存储通归档表   
* 增加vpn口令密码   

## v0.3.2 
* ftp兼容filezilla客户端  
* 增加ftp list_dir生成器接口  
* 域名修改科技云通行证登录配置修改，logo修改   

## v0.3.1
* 对象和目录model删除sh字段，重命名srd字段为share   
* 对象分享API参数修改   

## v0.3.0
* 增加分享功能，分享桶和目录，分享链接浏览下载分享内容    
* 对象model增加na_md5和srd字段    
* 分享功能相关的API实现   

## v0.2.11
* 修复科技云通行证登录回调500 bug  
* FTP修复小文件下载存在的问题  

## v0.2.10
* 修复obs下载找不到桶的bug   

## v0.2.9   
* 存储桶ftp访问增加只读密码   

## v0.2.8  
* 群发通知邮件命令
* 修复list dir分页bug

## v0.2.7  
* ftp性能优化  

## v0.2.6
* 为ftp封装一些操作Harbor对象的接口，rest API也使用这些接口   
*  ceph配置修改    

## v0.2.5
* 用户模型增加role字段   
* 获取ceph IO状态接口完善   
* 修复用户未认证时记录用户活跃日期时的错误   
* 对象元数据通过metadata api获取，删除通过obj api获取对象元数据的功能   
* 上传对象分片时，更新对象元数据修改，对象大小字段只在更新的值比数据库中此字段的值大时才更新  
* 存储桶删除和设置权限API的参数ids改为通过url传递    

## v0.2.4
* 添加获取元数据API，一些路由格式修改   
* 文件上传时乐观锁更新对象元数据，防止并发数据不一致   
* 前端页面实现对象重命名   
* 前端js修改，对象列表页面包屑路径改为在前端生成渲染，移除无用的python第三方包  
* 列举目录下的对象或子目录时不再按创建时间倒叙排序  
* clearbucket命令启用多线程    
* ceph集群的访问接口基于官方python包封装实现   
* 增加获取ceph集群统计信息API，获取ceph集群组件信息API,获取ceph集群io性能信息API    
* 增加用户资源统计API，查询用户总量API, 系统可用性监控API，系统访问信息统计API，系统是否可用查询API    
* 对象分片上传由PUT改为POST方法    
* list dir分页优化    
* 对象下载支持Range和Content-Range标头参数    
* 交互式api文档Schema相关修改，用action或method区分manual fields参数    

## v0.2.3
* 增加用户信息修改API和用户API权限修改
* 增加通过用户名获取用户安全凭证的API   
* 通过django-cors-headers实现跨域支持   
* 限制同一路径下存在重名对象或目录  
* 增加移动对象和重命名对象API   

## v0.2.2
* 增加存储桶所占资源统计API   
* 日志文件存放路径改为/var/log/evharbor   
* 支持第三方科技云通行证登录认证  

## v0.2.1  
* 对象模型添加对象名称联合唯一索引，对象和目录名称长度最大255字符限制  
* 对象元数据序列化器修改和对应js修改   
* 添加访问密钥（access_key, secret_key）认证方式，添加访问密钥相关API，安全凭证前端页面添加访问密钥内容  
* 添加django-debug-toolbar，方便多网页时一些调试分析   
* 对象查询管理类的一些修改   
* 添加存储桶名唯一性约束，软删除修改        

## v0.2.0
* 对象元数据存储从mongodb改为mysql数据库   
* 一些依赖包版本更新,如Django 1.11.18   
* 目录创建API修改，对应js文件修改，支持含特殊字符文件夹创建
* 修改clearbucket命令（因对象元数据存储数据库更改）  
* 增加一些统计耗时时长的日志代码   
* rados接口修改   
* 后台管理修改以支持修改用户的密码   
* uwsgi配置文件修改   
* 对象下载API自定义下载时返回不正确的二进制数据流问题修正 
* 压缩迁移文件，对象元数据切换mysql后一些语义化代码修改，耗时统计log修改        
* 虚拟机备注信息修改实现   

## v0.1.7
* 添加各功能部分的说明文档页面，ckeditor富文本编辑支持    
* APIAuth模型字段修改   

## v0.1.6
* 完善虚拟机限制数量问题   
* 对象名作为shard key   
* 添加openvpn autt认证脚本  

## v0.1.5
* rados接口类增加写入方法可传入一个文件  
* 元数据对象名字段唯一unique  
* 对象上传方式为覆盖上传  
* 创建桶时创建shard collection  
* Bucket增加大小和对象数量字段，其他一些代码优化  
* 对象元数据和对象数据原子性操作修改  
* 对象名改为存全路径，桶的集合名为'bucket_' + 桶id, rados对象名key改为桶id+对象原数据id  
* 非空目录不允许删除，对象和目录删除改为物理删除   
* 添加自定义django命令'clearbucket'   
* firefox文件下载中文文件名乱码问题修改，对象下载API参数名修改和自定义读取文件块不得大于20MB限制  

## v0.1.4
* 修复firefox浏览器下载文件时无文件名问题  
* 页面实现文件对象分享公开设置及相关代码修改，js代码api字符串的拼接整理  
* 增加存储桶访问权限设置API和对应页面设置桶权限的功能实现  
* 解决mongoengine上下文管理器switch_collection线程安全问题  
* 修改文件夹对象分页方式，分享下载api添加存储桶访问权限的判断   
* 增加文档app  
* 实现用户桶数量限制  
* 增加用户模型字段，注册时获取更多用户信息  
* 桶内对象数量限制

## v0.1.3
* 找回密码修改
* 用户注册bug修复

## v0.1.2
* utc时间转本地时间
* 添加安全凭证页面
* mongoengine swith_collection使用相关修改
* 用户注册修改

## v0.1.1
* 增加找回密码功能。

# v0.1.0
* 第一个发布版本，基础功能和API实现。
