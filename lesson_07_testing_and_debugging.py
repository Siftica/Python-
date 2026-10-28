# 第 07 课：自动检查与基础调试。
# 运行方法：python lesson_07_testing_and_debugging.py
# 仅使用 Python 内置功能；不依赖其他课程文件或测试框架。
# 直接运行会执行 20 项固定检查；测试失败时抛出异常，不打印全部通过。
# 导入本文件只定义函数，不自动运行测试；本程序不读写数据文件。
# assert 用于这些开发检查；外部输入检查仍由 if + raise ValueError 完成。


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


def test_encode_cases(token_to_id):
    cases = [
        {"name": "已知字符", "text": "我爱学习", "expected": [0, 1, 2, 3]},
        {"name": "混合未知字符", "text": "我爱大模型", "expected": [0, 1, 6, 4, 5]},
        {"name": "空字符串", "text": "", "expected": []},
        {"name": "重复已知字符", "text": "我我爱", "expected": [0, 0, 1]},
        {"name": "重复未知字符", "text": "大大", "expected": [6, 6]},
    ]
    for case in cases:
        actual = encode(case["text"], token_to_id)
        expected = case["expected"]
        message = case["name"] + "，输入：" + repr(case["text"])
        message = message + "，预期：" + repr(expected) + "，实际：" + repr(actual)
        assert actual == expected, message

    first = encode("我爱", token_to_id)
    second = encode("学习", token_to_id)
    assert first == [0, 1], "连续调用后第一次结果不应变化，实际：" + repr(first)
    assert second == [2, 3], "第二次调用不应累积旧编号，实际：" + repr(second)
    return len(cases) + 2


def test_decode_cases(id_to_token):
    cases = [
        {"name": "已知编号", "token_ids": [0, 1, 2, 3], "expected": "我爱学习"},
        {"name": "未知标记", "token_ids": [6], "expected": "<unk>"},
        {"name": "空编号列表", "token_ids": [], "expected": ""},
        {"name": "重复编号", "token_ids": [0, 0, 1], "expected": "我我爱"},
    ]
    for case in cases:
        actual = decode(case["token_ids"], id_to_token)
        expected = case["expected"]
        message = case["name"] + "，输入：" + repr(case["token_ids"])
        message = message + "，预期：" + repr(expected) + "，实际：" + repr(actual)
        assert actual == expected, message
    return len(cases)


def test_invalid_inputs(token_to_id, id_to_token):
    bad_texts = [123, None, []]
    for bad_text in bad_texts:
        raised_expected_error = False
        try:
            encode(bad_text, token_to_id)
        except ValueError:
            raised_expected_error = True
        assert raised_expected_error, "encode 应拒绝这个输入：" + repr(bad_text)

    bad_token_lists = ["0,1", [-1], [7], [True], ["1"], [1.0]]
    for bad_ids in bad_token_lists:
        raised_expected_error = False
        try:
            decode(bad_ids, id_to_token)
        except ValueError:
            raised_expected_error = True
        assert raised_expected_error, "decode 应拒绝这个输入：" + repr(bad_ids)

    return len(bad_texts) + len(bad_token_lists)


def main():
    # -O / -OO 会移除 assert；本课入口明确拒绝这种启动方式。
    if not __debug__:
        raise RuntimeError("本课使用 assert，请使用普通 Python 运行，不要启用 -O 或 -OO。")
    token_to_id = {
        "我": 0, "爱": 1, "学": 2, "习": 3,
        "模": 4, "型": 5, "<unk>": 6,
    }
    id_to_token = ["我", "爱", "学", "习", "模", "型", "<unk>"]

    encode_count = test_encode_cases(token_to_id)
    print("通过：编码与连续调用", encode_count, "项")
    decode_count = test_decode_cases(id_to_token)
    print("通过：解码", decode_count, "项")
    invalid_count = test_invalid_inputs(token_to_id, id_to_token)
    print("通过：错误输入", invalid_count, "项")

    total = encode_count + decode_count + invalid_count
    print("全部通过：", total, "项固定检查。")
    return total


if __name__ == "__main__":
    main()
