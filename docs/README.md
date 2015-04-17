#Paxp2 说明手册

---

##目录结构

```
.
├── pdf
│   ├── Protocol-0.14-v1-for-DSP.pdf
│   └── Protocol-0.14-v1-for-SDK.pdf
├── protocol-0.14
│   ├── appendix.yaml
│   ├── example
│   │   ├── dsp
│   │   │   ├── bid-request-example.json
│   │   │   ├── bid-response-failed-example.json
│   │   │   ├── bid-response-successful-example.json
│   │   │   └── notice-example.json
│   │   └── sdk
│   │       ├── clk-request-example.json
│   │       ├── clk-response-failed-example.json
│   │       ├── clk-response-successful-example.json
│   │       └── result-example.json
│   ├── protocol-0.14.html
│   ├── protocol-0.14.raml
│   └── schema
│       ├── bid-request-schema.json
│       ├── bid-response-schema.json
│       ├── clk-request-schema.json
│       ├── clk-response-schema.json
│       ├── notice-schema.json
│       └── result-schema.json
└── README.md
```

__*pdf/*__

 - 基于协议的最新电子版手册 这里只会放置最新版本协议
 - 包含向 DSP 和 向 SDK 两方面发送的内容

__*protocol-0.14/*__

 - appendix.yaml
  附录表的内容

 - example/
  基于最新版本协议生成的一份标准数据内容

 - protocol-0.14.raml
  接口定义的 REST API 文档

 - protocol-0.14.html
  提供 web 界面展示协议所依赖的 API 接口定义

 - schema/
  定义调用接口时限制输入方请求内容字段格式的 JSON 语法
