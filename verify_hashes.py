import pickle
import hashlib
import sys

def verify_hashes():
    with open('test_cases.pkl', 'rb') as f:
        baseline = pickle.load(f)
    
    results = {}
    for case_id, meta in baseline.items():
        # 反序列化
        obj = pickle.loads(meta['pickled'])
        
        # 重新序列化并哈希
        current_pickled = pickle.dumps(obj, protocol=meta['protocol'])
        current_hash = hashlib.sha256(current_pickled).hexdigest()
        original_hash = hashlib.sha256(meta['pickled']).hexdigest()
        
        results[case_id] = {
            'type': meta['type'],
            'original_version': meta['py_version'],
            'current_version': f"{sys.version_info.major}.{sys.version_info.minor}",
            'hash_match': current_hash == original_hash,
            'size_match': len(current_pickled) == len(meta['pickled']),
            'protocol': meta['protocol']
        }
    
    # 打印结果
    print(f"\n{'='*40}\nPython {sys.version.split()[0]} 验证结果\n{'='*40}")
    for case_id, res in results.items():
        status = '✅' if res['hash_match'] else '❌'
        print(f"[{status}] {case_id}")
        print(f"  Type: {res['type']}")
        print(f"  From: Python {res['original_version']}")
        print(f"  Protocol: {res['protocol']}")
        if not res['hash_match']:
            print("  !!! 哈希不匹配")
        if not res['size_match']:
            print("  !!! 序列化长度变化")
        print("-" * 30)

if __name__ == '__main__':
    verify_hashes()