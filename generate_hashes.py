import pickle
import hashlib
import sys

# 测试数据集（包含基本类型、嵌套结构和递归引用）
test_cases = [
    # 基本类型
    None,
    42,
    3.14,
    "hello",
    b"bytes",
    # 嵌套结构
    [1, [2, {'a': (3, 4)}]],
    {'x': {'y': [5, 6]}},
    # 递归结构
    lambda: (recursive := {}, recursive.update({'self': recursive}))[1],
    # 集合（注意Python 3.3+的哈希随机化）
    {1, 2, 3}
]

def generate_hashes():
    hashes = {}
    for obj in test_cases:
        # 处理递归结构的lambda
        if callable(obj):
            obj = obj()
        
        # 序列化并记录元数据
        pickled = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        key = f"{type(obj).__name__}_{hashlib.sha256(pickled).hexdigest()[:6]}"
        hashes[key] = {
            'pickled': pickled,
            'type': type(obj).__name__,
            'py_version': f"{sys.version_info.major}.{sys.version_info.minor}",
            'protocol': pickle.HIGHEST_PROTOCOL
        }
    
    # 保存到文件
    with open('test_cases.pkl', 'wb') as f:
        pickle.dump(hashes, f)

if __name__ == '__main__':
    generate_hashes()
    print("基准哈希已生成到 test_cases.pkl")