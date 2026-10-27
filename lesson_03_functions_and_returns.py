# 第 03 课：函数、参数与返回值。
# 运行方法：python lesson_03_functions_and_returns.py
# 本程序只使用 Python 标准功能，无需第三方包、模型文件或显卡。
# encode 接收文字与词表，返回编号列表。
# decode 接收有效编号与对应字符表，返回字符串。
# 两份表的编号必须一致；词表需包含 <unk>。


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


# 保留前两课的编号；大、小等未收录的字符仍使用 6 号。
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

# 用同一组函数处理三种输入：已知字符、含未知字符、空字符串。
texts = ["我爱学习", "我爱大模型", ""]

for text in texts:
    token_ids = encode(text, token_to_id)
    restored = decode(token_ids, id_to_token)

    print("原文：", text)
    print("编号：", token_ids)
    print("解码：", restored)
    print()
