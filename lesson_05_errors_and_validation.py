# 第 05 课：异常处理与数据检查。
# 运行方法：python lesson_05_errors_and_validation.py
# 只使用 Python 标准库，无需显卡或其他课程文件。
# 数据目录：当前工作目录下的 lesson_05_data。
# input_records.json 缺失时生成示例；已存在时保留原内容。
# 读取、JSON 解析或校验失败时，不会更新 validated_records.json。
# 只检查结构、字段类型与编号范围，不检查 text 与 token_ids 是否对应。
# 初始化示例目录/文件要求当前目录可写；写盘失败不保证旧输出完整。

import json
from pathlib import Path


def decode(token_ids, id_to_token):
    restored = ""

    for token_id in token_ids:
        restored = restored + id_to_token[token_id]

    return restored


def load_records(path):
    json_text = path.read_text(encoding="utf-8")
    return json.loads(json_text)


def validate_records(records, vocab_size):
    if not isinstance(records, list):
        raise ValueError("最外层必须是列表，例如 [{...}, {...}]")

    record_number = 1
    for record in records:
        location = "第 " + str(record_number) + " 条记录"

        if not isinstance(record, dict):
            raise ValueError(location + "必须是字典")
        if "text" not in record:
            raise ValueError(location + "缺少 text 字段")
        if "token_ids" not in record:
            raise ValueError(location + "缺少 token_ids 字段")
        if not isinstance(record["text"], str):
            raise ValueError(location + "的 text 必须是字符串")
        if not isinstance(record["token_ids"], list):
            raise ValueError(location + "的 token_ids 必须是列表")

        token_index = 0
        for token_id in record["token_ids"]:
            token_location = location + "的 token_ids[" + str(token_index) + "]"
            # Python 的 bool 也能通过 int 类型检查，因此先排除它。
            if isinstance(token_id, bool):
                raise ValueError(token_location + "不能是布尔值")
            if not isinstance(token_id, int):
                raise ValueError(token_location + "必须是整数")
            if token_id < 0:
                raise ValueError(token_location + "不能小于 0")
            if token_id >= vocab_size:
                raise ValueError(token_location + "必须小于词表大小 " + str(vocab_size))
            token_index = token_index + 1

        record_number = record_number + 1

    # 检查通过后返回原数据；这个函数不修改、不补齐、不纠正数据。
    return records


def process_file(input_path, output_path, id_to_token):
    # 第一阶段：读取、解析、检查。任一步失败就退出本次函数。
    try:
        records = load_records(input_path)
        checked_records = validate_records(records, len(id_to_token))
    except FileNotFoundError:
        print("读取失败：找不到输入文件：", input_path.resolve())
        return False
    except UnicodeDecodeError:
        print("读取失败：输入文件不是可读取的 UTF-8 文本。请检查文件编码。")
        return False
    except OSError as error:
        print("读取失败：", error)
        return False
    except json.JSONDecodeError as error:
        print("JSON 格式错误：第", error.lineno, "行，第", error.colno, "列：", error.msg)
        return False
    except ValueError as error:
        print("数据检查未通过：", error)
        return False

    # 第二阶段：全部记录检查通过后，才构造输出。
    results = []
    for record in checked_records:
        result = record.copy()
        result["decoded_text"] = decode(record["token_ids"], id_to_token)
        results.append(result)

    # 第三阶段：保存生成结果。写盘失败与输入数据错误分开提示。
    try:
        json_text = json.dumps(results, ensure_ascii=False, indent=2)
        output_path.write_text(json_text, encoding="utf-8")
    except OSError as error:
        print("保存失败：", error)
        print("输出可能没有完整写入，请解决保存问题后重新运行。")
        return False

    print("成功：已检查并保存", len(results), "条记录。")
    print("结果文件：", output_path.resolve())
    return True


id_to_token = ["我", "爱", "学", "习", "模", "型", "<unk>"]

work_dir = Path.cwd() / "lesson_05_data"
work_dir.mkdir(exist_ok=True)
input_path = work_dir / "input_records.json"
output_path = work_dir / "validated_records.json"

sample_records = [
    {"line_number": 1, "text": "我爱学习", "token_ids": [0, 1, 2, 3]},
    {"line_number": 2, "text": "我爱大模型", "token_ids": [0, 1, 6, 4, 5]},
    {"line_number": 3, "text": "", "token_ids": []},
    {"line_number": 4, "text": "学习模型", "token_ids": [2, 3, 4, 5]},
]

# 首次运行便于开始练习；已存在的输入，即使有错误，也不会被替换。
if not input_path.exists():
    sample_json = json.dumps(sample_records, ensure_ascii=False, indent=2)
    input_path.write_text(sample_json, encoding="utf-8")

print("输入文件：", input_path.resolve())
success = process_file(input_path, output_path, id_to_token)
print("本次处理成功：", success)
