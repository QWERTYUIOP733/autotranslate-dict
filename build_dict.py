#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动汉化模组 - 内置词典生成脚本
=================================
从 Minecraft 26.3 官方语言文件生成完整内置词典 zh_cn_dict.json：
  - byKey : 翻译键 -> 简体中文（覆盖官方全部键）
  - byText: 英文原文 -> 简体中文（供"按原文匹配"拦截使用）
保留并优先现有模组词典中的自定义条目。

用法:
  python build_dict.py
"""
import json
import io
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EN_US = os.path.join(BASE_DIR, "en_us.json")
ZH_CN = os.path.join(BASE_DIR, "zh_cn.json")
EXISTING = r"D:\豆包工作区\自动汉化模组\AutoTranslateMod\src\main\resources\assets\autotranslate\lang\zh_cn_dict.json"
OUTPUT = os.path.join(BASE_DIR, "zh_cn_dict.json")

def load_json(path):
    with io.open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def dump_json(obj, path):
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
        f.write("\n")

def main():
    print("加载官方语言文件...")
    en = load_json(EN_US)
    zh = load_json(ZH_CN)
    print("  en_us: %d 键" % len(en))
    print("  zh_cn: %d 键" % len(zh))

    # 1) byKey：官方键 -> 中文
    by_key = {}
    for k, v in zh.items():
        by_key[k] = v
    # 官方 en_us 有而 zh_cn 没有的键，保留英文原样（键在，值兜底）
    for k in en.keys():
        if k not in by_key:
            by_key[k] = en[k]

    # 2) byText：英文原文 -> 中文（仅当该键官方有中文且原文不同）
    by_text = {}
    for k, ev in en.items():
        zv = zh.get(k)
        if zv and zv != ev:
            by_text[ev] = zv

    # 3) 合并现有自定义条目（用户自定义优先）
    if os.path.exists(EXISTING):
        existing = load_json(EXISTING)
        ek = existing.get("byKey", {})
        et = existing.get("byText", {})
        custom_key = len([k for k in ek.keys() if k not in by_key])
        custom_text = len([k for k in et.keys() if k not in by_text])
        by_key.update(ek)
        by_text.update(et)
        print("  合并现有词典: byKey 自定义 %d 条, byText 自定义 %d 条" % (custom_key, custom_text))

    # 排序（键排序便于 diff 与维护）
    by_key = dict(sorted(by_key.items()))
    by_text = dict(sorted(by_text.items()))

    result = {"byKey": by_key, "byText": by_text}
    dump_json(result, OUTPUT)

    size = os.path.getsize(OUTPUT)
    print("生成完成: %s" % OUTPUT)
    print("  byKey: %d 条" % len(by_key))
    print("  byText: %d 条" % len(by_text))
    print("  文件大小: %.2f KB" % (size / 1024.0))

if __name__ == "__main__":
    main()
