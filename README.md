# 自动汉化词典（AutoTranslate Dictionary）

为「自动汉化模组」（Fabric · Minecraft 26.3）提供的内置翻译词典数据仓库。

## 数据概况

| 项目 | 数值 |
| --- | --- |
| 游戏版本 | Minecraft 26.3（Wilderness Bound） |
| byKey（翻译键 → 简体中文） | **8,578 条** |
| byText（英文原文 → 简体中文） | **7,655 条** |
| 词典文件 | `zh_cn_dict.json`（约 938 KB） |
| 数据来源 | Minecraft 26.3 官方语言文件（Mojang 资产，简体中文 + 英文） |

## 词典结构

```json
{
  "byKey":  { "block.minecraft.stone": "石头", "...": "..." },
  "byText": { "Stone": "石头", "...": "..." }
}
```

- **byKey**：按翻译键匹配。模组 Mixin 拦截 `net.minecraft.locale.Language#getOrDefault` 时，先查本表；适用于游戏内以翻译键查找文本的场景。
- **byText**：按英文原文匹配。适用于游戏内直接以英文原文显示、需要反查中文的场景（"仅补缺"模式）。

## 数据来源与更新

词典由 `build_dict.py` 从官方语言文件生成：

1. `en_us.json` / `zh_cn.json` —— 来自 Minecraft 26.3 官方客户端资产（assets index 34）
2. 运行 `python build_dict.py`，输出 `zh_cn_dict.json`
3. 脚本会**保留并优先**现有模组中的自定义条目（如需修正官方翻译或补充模组自身文本，改 `build_dict.py` 中 `EXISTING` 指向的文件即可）

随游戏大版本更新时，替换两个官方 json 后重新运行脚本即可。

## 使用

将 `zh_cn_dict.json` 放入自动汉化模组的
`src/main/resources/assets/autotranslate/lang/zh_cn_dict.json`，
重新构建即生效。也可将本文件复制到模组的
`config/autotranslate/dict/` 目录作为外部词典（热重载）。

## 许可证

MIT License。数据部分源自 Mojang 语言文件（属 Mojang 版权资产，仅用于模组本地化）。
