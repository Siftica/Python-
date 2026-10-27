# 第 04 课：读取文本文件，保存 JSON，再读取核对。
# 运行方法：python lesson_04_text_files_and_json.py
# 只使用 Python 标准库；示例输入会在首次运行时自动生成。
# 数据目录位于运行时的当前工作目录下，程序会打印实际位置。
# input.txt 已存在时会保留；generated_records.json 是每次更新的生成结果。
# 本课按行保留文字、空格与中间空行；空文件会产生空记录列表。

import json
from pathlib import Path


def encode(text, token_to_id):
    token_ids = []

    for char in text:
        if char in token_to_id:
            token_id = token_to_id[char]
        else:
            token_id = token_to_id["<unk>"]

        token_ids.append(token_id)

    return token_ids


def decode(token_ids, id_to_token):
    restored = ""

    for token_id in token_ids:
        restored = restored + id_to_token[token_id]

    return restored


token_to_id = {
    "我": 0,
    "爱": 1,
    "学": 2,
    "习": 3,
    "模": 4,
    "型": 5,
    "<unk>": 6,
}
id_to_token = ["我", "爱", "学", "习", "模", "型", "<unk>"]

work_dir = Path.cwd() / "lesson_04_data"
work_dir.mkdir(exist_ok=True)
input_path = work_dir / "input.txt"
output_path = work_dir / "generated_records.json"

# 只有输入文件不存在时，才创建示例；已存在的输入会被保留。
sample_text = '我爱学习\n我爱大模型\n\n学习模型\n'
if not input_path.exists():
    input_path.write_text(sample_text, encoding="utf-8")

raw_text = input_path.read_text(encoding="utf-8")
lines = raw_text.splitlines()

records = []
line_number = 1

for text in lines:
    token_ids = encode(text, token_to_id)
    record = {
        "line_number": line_number,
        "text": text,
        "token_ids": token_ids,
    }
    records.append(record)
    line_number = line_number + 1

# 这是重新生成的结果文件，每次运行都会按当前输入更新。
json_text = json.dumps(records, ensure_ascii=False, indent=2)
output_path.write_text(json_text, encoding="utf-8")

saved_text = output_path.read_text(encoding="utf-8")
loaded_records = json.loads(saved_text)

print("工作目录：", work_dir.resolve())
print("输入文件：", input_path.resolve())
print("结果文件：", output_path.resolve())
print("记录数量：", len(loaded_records))

for record in loaded_records:
    restored = decode(record["token_ids"], id_to_token)
    print("行号：", record["line_number"])
    print("原文：", record["text"])
    print("编号：", record["token_ids"])
    print("解码：", restored)
    print()
