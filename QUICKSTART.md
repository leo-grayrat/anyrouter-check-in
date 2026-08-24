# 最简使用：注册账号，然后填账号密码

这份文件只讲最短流程。正常情况下**不需要获取 Cookie、不需要找 `api_user`、不需要配置 `PROVIDERS`**。

## 1. 去需要的站注册

目前可直接使用内置 provider 的站点：

| 站点 | 注册入口 | provider |
| --- | --- | --- |
| AnyRouter | https://anyrouter.top/register | `anyrouter` |
| GoRouter | https://gorouter.app/sign-up | `gorouter` |
| TabiToken | https://tabitoken.com/sign-up | `tabitoken` |
| DoCode | https://docode.cc/register | `docode` |
| JianZhiLe | https://jianzhile.vip/register | `jianzhile` |
| 肖恩 AI | https://free.supxh.xin/register | `shawn` |
| api456 | https://api456.me/register | `api456` |

这些公益站开放注册状态变化很快。某个站暂时注册不了，直接跳过即可，不影响其他站。

另外两个站情况特殊：

- `agentrouter` 已内置，但 GitHub Actions 访问它通常还需要代理配置；先不放进最简模板。
- `jun`（君の公益）已内置，但注册方式可能只开放第三方登录；如果没有可用的账号密码登录，也先跳过。

如果其他站注册时同样只允许 GitHub / LinuxDo 等第三方登录、没有站内账号密码，就先把它从模板删除；当前“最简模式”只自动填写账号密码登录表单。

> 建议每个站使用独立密码。账号密码只放到 GitHub Secret，不要提交到仓库文件里。

## 2. 把注册好的账号填进下面模板

把没注册的整段删掉，只保留你实际拥有的账号：

```json
[
  {
    "name": "AnyRouter",
    "provider": "anyrouter",
    "email": "你的邮箱",
    "password": "你的密码"
  },
  {
    "name": "GoRouter",
    "provider": "gorouter",
    "email": "你的邮箱",
    "password": "你的密码"
  },
  {
    "name": "TabiToken",
    "provider": "tabitoken",
    "email": "你的邮箱",
    "password": "你的密码"
  },
  {
    "name": "DoCode",
    "provider": "docode",
    "email": "你的邮箱",
    "password": "你的密码"
  },
  {
    "name": "JianZhiLe",
    "provider": "jianzhile",
    "email": "你的邮箱",
    "password": "你的密码"
  },
  {
    "name": "肖恩 AI",
    "provider": "shawn",
    "email": "你的邮箱",
    "password": "你的密码"
  },
  {
    "name": "api456",
    "provider": "api456",
    "email": "你的邮箱",
    "password": "你的密码"
  }
]
```

如果以后又发现一个普通 NewAPI 站，甚至不需要改代码，直接写域名：

```json
{
  "name": "新站",
  "domain": "https://example.com",
  "email": "你的邮箱",
  "password": "你的密码"
}
```

## 3. 把整段 JSON 放进一个 GitHub Secret

进入你的 fork：

`Settings` → `Environments` → 新建或进入 `production` → `Add environment secret`

只需要新建这一个：

- Name：`ANYROUTER_ACCOUNTS`
- Value：第 2 步那整段 JSON

不要给每个站分别新建 Secret。

## 4. 开启并测试 Actions

进入 `Actions`，启用工作流，然后手动运行一次 **AnyRouter 自动签到**。

结果里每个账号会分别显示成功或失败。一个站失败不会妨碍其他站继续签到。

如果某个普通 NewAPI 站失败，再去看日志；大多数情况下才需要考虑 Cookie、特殊签到路径或 WAF。那些属于排错步骤，不是首次配置步骤。
