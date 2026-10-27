# 第 01 课：把中文变成编号，再按编号还原。
# 运行方法：python lesson_01_text_to_ids.py
# 只需要 Python；没有第三方依赖，不需要显卡或网络。
# 本课的输入字符需要已经存在于 vocab 中；未知字符在第 02 课处理。

# 1. 准备原文和固定词表。
text = "我爱学习"
vocab = ["我", "爱", "学", "习", "模", "型"]

# 2. 编码：按顺序查找每个字符的位置，保存编号。
token_ids = []
for char in text:
    token_id = vocab.index(char)
    token_ids.append(token_id)

print("原文：", text)
print("词表：", vocab)
print("编号：", token_ids)

# 3. 还原：按编号查出字符，再依次拼接。
restored = ""
for token_id in token_ids:
    restored = restored + vocab[token_id]

print("还原：", restored)
