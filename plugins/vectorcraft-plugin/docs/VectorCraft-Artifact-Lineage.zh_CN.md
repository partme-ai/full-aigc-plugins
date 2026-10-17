# 产物血缘

插件57锁定源43。公开工作流登记稳定逻辑ID、内容寻址包版本、执行ID、计划摘要、原生工程、导出和登记素材。整包移动使用相对路径；修订在安装运行时前验证父包，保留逻辑身份。历史包明确登记无版本父来源。

```mermaid
flowchart LR
    P[Plan + registered assets] --> W[Public workflow]
    O[Verified parent package] --> W
    W --> N[Native project + exports]
    N --> L[lineage.json]
    L --> M[manifest.json digest binding]
    M --> C[Public delivery checker]
    C -->|All current bytes and edges match| I[Integrity PASS]
    C -->|Missing or changed dependency| F[Refuse before decoding]
    I --> R[Separate native reopening and creative review]
```

公开校验先核对全部文件和语义依赖，再解码。旧包仍可读取，血缘状态为NOT_RUN。该校验只证明包内身份一致性，不证明外部任务认证、原生重开或创作验收。源五项测试、公开三项测试覆盖重签摘要后的语义错配。原生候选已完成创建、移动重开、修订及五类拒绝；固定安装任务5.3仍开放。

[候选证据](evidence/vectorcraft-lineage-candidate57-20261009.json)。


插件58修正公开校验的导入方式，保持安装技能字节不变。57真实CI缓存写入失败记录保留；只读回归在57失败、58通过。本地74项Python通过，固定58验收仍待完成。 [Evidence](evidence/vectorcraft-lineage-candidate58-20261009.json).


公开58／源43实际安装于Codex0.153.4 macOS arm64，已通过当前VC-AR-001三个场景：原生创建、整包移动重开、父版本绑定修订及公开七案例校验。13项安装摘要保持不变。5.3关闭，总体114/127完成，13项开放；创作与其他平台验收独立。 [Evidence](evidence/vectorcraft-lineage-fixed58-20261009.json).
