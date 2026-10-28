#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""第 08 课：向量、点积与矩阵形状。

运行：python lesson_08_vectors_dot_shapes.py
依赖：仅 Python 标准库，无需显卡、PyTorch 或 NumPy。
"""

import math


def add_vectors(a, b):
    """逐元素相加，要求两个向量等长。"""
    if len(a) != len(b):
        raise ValueError("向量加法要求两个向量长度相同")
    result = []
    for index in range(len(a)):
        result.append(a[index] + b[index])
    return result


def scale_vector(vector, factor):
    """向量数乘。"""
    result = []
    for number in vector:
        result.append(number * factor)
    return result


def dot(a, b):
    """点积：对应位置相乘后相加。"""
    if len(a) != len(b):
        raise ValueError("点积要求两个向量长度相同")
    total = 0
    for index in range(len(a)):
        total += a[index] * b[index]
    return total


def norm(vector):
    """向量的欧氏长度。"""
    return math.sqrt(dot(vector, vector))


def cosine_similarity(a, b):
    """余弦相似度；零向量没有定义。"""
    denominator = norm(a) * norm(b)
    if denominator == 0:
        raise ValueError("零向量无法计算余弦相似度")
    return dot(a, b) / denominator


def matrix_shape(matrix):
    """返回二维列表的形状 (行数, 列数)，拒绝空矩阵与不规则行。"""
    if not matrix:
        raise ValueError("矩阵必须至少有一行")
    columns = len(matrix[0])
    if columns == 0:
        raise ValueError("矩阵每行必须至少有一个元素")
    for row in matrix:
        if len(row) != columns:
            raise ValueError("矩阵各行长度必须一致")
    return len(matrix), columns


def matrix_vector(matrix, vector):
    """矩阵乘向量：每行与 vector 做一次点积。"""
    _, columns = matrix_shape(matrix)
    if columns != len(vector):
        raise ValueError("矩阵列数必须等于向量长度")
    result = []
    for row in matrix:
        result.append(dot(row, vector))
    return result


def qk_scaled_scores(queries, keys):
    """计算 QK^T/sqrt(d_k)，只返回未做 softmax 的分数矩阵。

    queries: [查询个数, d_k]，keys: [键的个数, d_k]
    输出: [查询个数, 键的个数]
    """
    _, query_width = matrix_shape(queries)
    _, key_width = matrix_shape(keys)
    if query_width != key_width:
        raise ValueError("Q 与 K 的每行向量维度必须相同")
    scores = []
    for query in queries:
        one_row = []
        for key in keys:
            one_row.append(dot(query, key) / math.sqrt(query_width))
        scores.append(one_row)
    return scores


def run_checks():
    """固定输入和预期结果，检查计算函数与维度错误处理。"""
    a = [1, 2, 3]
    b = [-1, 0, 2]
    matrix = [[1, 2, 0], [0, 1, 3]]
    q = [[1, 0], [0, 1], [1, 1]]
    k = [[1, 0], [0, 1], [1, 1]]
    scores = qk_scaled_scores(q, k)

    checks = [
        ("向量加法", add_vectors(a, b) == [0, 2, 5]),
        ("向量数乘", scale_vector(a, 2) == [2, 4, 6]),
        ("向量点积", dot(a, b) == 5),
        ("点积对称性", dot(a, b) == dot(b, a)),
        ("向量长度", math.isclose(norm([3, 4]), 5)),
        ("垂直向量余弦相似度", math.isclose(cosine_similarity([1, 0], [0, 1]), 0)),
        ("矩阵形状", matrix_shape(matrix) == (2, 3)),
        ("矩阵乘向量", matrix_vector(matrix, [2, 1, 1]) == [4, 4]),
        ("QK 分数矩阵形状", matrix_shape(scores) == (3, 3)),
        ("QK 第一项的缩放", math.isclose(scores[0][0], 1 / math.sqrt(2))),
        ("QK 末项的缩放", math.isclose(scores[2][2], math.sqrt(2))),
    ]
    passed = 0
    for label, okay in checks:
        if not okay:
            raise AssertionError("检查失败：" + label)
        passed += 1

    # 这些错误输入必须抛出 ValueError，而不能悄悄计算出一个结果。
    error_cases = [
        ("点积维度不匹配", lambda: dot([1, 2], [1])),
        ("矩阵行长不一致", lambda: matrix_shape([[1, 2], [3]])),
        ("矩阵乘向量维度不匹配", lambda: matrix_vector(matrix, [1, 2])),
        ("QK 维度不匹配", lambda: qk_scaled_scores([[1, 0]], [[1, 0, 2]])),
        ("零向量余弦相似度", lambda: cosine_similarity([0, 0], [1, 0])),
    ]
    for label, operation in error_cases:
        try:
            operation()
        except ValueError:
            passed += 1
        else:
            raise AssertionError("应当抛出 ValueError：" + label)

    print("通过固定检查：", passed, "项")
    return passed


def main():
    a = [1, 2, 3]
    b = [-1, 0, 2]
    print("向量 a：", a)
    print("向量 b：", b)
    print("a + b：", add_vectors(a, b))
    print("2 * a：", scale_vector(a, 2))
    print("a · b：", dot(a, b))
    print("a 的长度（约）：", round(norm(a), 4))
    print("余弦相似度（约）：", round(cosine_similarity(a, b), 4))

    matrix = [[1, 2, 0], [0, 1, 3]]
    vector = [2, 1, 1]
    print("矩阵形状：", matrix_shape(matrix))
    print("矩阵乘向量：", matrix_vector(matrix, vector))

    queries = [[1, 0], [0, 1], [1, 1]]
    keys = [[1, 0], [0, 1], [1, 1]]
    scores = qk_scaled_scores(queries, keys)
    print("Q 的形状：", matrix_shape(queries))
    print("K 的形状：", matrix_shape(keys))
    print("缩放点积分数的形状：", matrix_shape(scores))
    print("缩放点积分数（保留四位小数）：")
    for row in scores:
        rounded = []
        for number in row:
            rounded.append(round(number, 4))
        print(" ", rounded)
    print("注意：这些是 softmax 之前的分数，不是注意力概率。")
    run_checks()


if __name__ == "__main__":
    main()
