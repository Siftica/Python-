# 第 06 课：模块、程序入口与小型项目组织。
# 运行方法：python lesson_06_modules_and_main.py
# 只用标准库；独立运行，不依赖讲义生成的两文件项目。
# 直接运行：处理固定示例，更新当前工作目录下 lesson_06_data/generated_records.json。
# 导入本文件：定义函数，不调用 main，不生成上述数据文件。
# 词表沿用前几课的约定；本课重点是组织与调用代码。

import json
from pathlib import Path


def encode(text, token_to_id):
    if not isinstance(text, str):
        raise ValueError("text 必须是字符串")

    token_ids = []
    for char in text:
        if char in token_to_id:
            token_id = token_to_id[char]
        else:
            token_id = token_to_id["<unk>"]
        token_ids.append(token_id)
    return token_ids


def decode(token_ids, id_to_token):
    if not isinstance(token_ids, list):
        raise ValueError("token_ids 必须是列表")

    restored = ""
    for token_id in token_ids:
        if isinstance(token_id, bool):
            raise ValueError("编号不能是布尔值")
        if not isinstance(token_id, int):
            raise ValueError("编号必须是整数")
        if token_id < 0:
            raise ValueError("编号不能小于 0")
        if token_id >= len(id_to_token):
            raise ValueError("编号超出词表范围")
        restored = restored + id_to_token[token_id]
    return restored


def main(output_dir):
    token_to_id = {
        "我": 0, "爱": 1, "学": 2, "习": 3,
        "模": 4, "型": 5, "<unk>": 6,
    }
    id_to_token = ["我", "爱", "学", "习", "模", "型", "<unk>"]

    texts = ["我爱学习", "我爱大模型", ""]
    records = []
    for text in texts:
        token_ids = encode(text, token_to_id)
        restored = decode(token_ids, id_to_token)
        record = {
            "text": text,
            "token_ids": token_ids,
            "decoded_text": restored,
        }
        records.append(record)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "generated_records.json"
    json_text = json.dumps(records, ensure_ascii=False, indent=2)
    output_path.write_text(json_text, encoding="utf-8")

    print("记录数量：", len(records))
    print("结果文件：", output_path.resolve())
    for record in records:
        print(record)
    return records


if __name__ == "__main__":
    main(Path.cwd() / "lesson_06_data")
