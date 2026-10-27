# 第 02 课：用字典和条件判断处理未知字符。
# 运行方法：python lesson_02_dict_and_conditions.py
# 只需要 Python；没有第三方依赖，不需要显卡或网络。
# <unk> 是本程序约定的未知字符标记，不是 Python 自动识别的语法。

text = "我爱大模型"

# 沿用第 01 课的 0–5 号，新增 6 号表示未知字符。
token_to_id = {
    "我": 0,
    "爱": 1,
    "学": 2,
    "习": 3,
    "模": 4,
    "型": 5,
    "<unk>": 6,
}

token_ids = []

for char in text:
    if char in token_to_id:
        token_id = token_to_id[char]
    else:
        token_id = token_to_id["<unk>"]

    # 每个字符选好编号之后，都追加一次。
    token_ids.append(token_id)

print("原文：", text)
print("编号：", token_ids)
