#!/usr/bin/env python3
"""
Algorithm-Fundamentals 题目整理工具：按算法类型自动分类 + 自动补题面。

用法：
    python3 tools/classify.py               # 扫描根目录散落的新文件并分类/补题面
    python3 tools/classify.py --all         # 全量扫描（含 leetcode/misc 中可再分类的）
    python3 tools/classify.py --fetch-only  # 只补题面，不移动文件

流程：
    1. 按文件名前缀/关键词把题目文件 git mv 到 leetcode/<category>/
    2. 从文件名提取题号，经 leetcode.cn graphql 抓取标准题面，
       插入 ipynb 首个 markdown cell（跳过已含题面的）
    3. 打印分类统计与无法分类清单

幂等：已分类、已补题面的文件自动跳过，可重复执行。
零依赖（仅标准库），需要网络访问 leetcode.cn。
"""
import os
import re
import json
import shutil
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LEETCODE_DIR = os.path.join(REPO, 'leetcode')
INDEX_URL = 'https://leetcode.cn/api/problems/all/'
GRAPHQL_URL = 'https://leetcode.cn/graphql'

# 文件名中文类型前缀 → 分类目录（kebab-case）
PREFIX_MAP = {
    '动归': 'dynamic-programming', '贪心算法': 'greedy',
    '二分查找': 'binary-search', '二分变种': 'binary-search', '二分法': 'binary-search',
    '二分法变种': 'binary-search', '二分': 'binary-search', '二分搜索变种': 'binary-search',
    '二分查找前缀和': 'binary-search',
    '链表': 'linked-list', '树': 'tree', 'BFS': 'graph', 'DFS': 'graph',
    'dfs回溯': 'backtracking', 'Trie': 'trie', 'Trie树变种': 'trie',
    '树状数组': 'binary-indexed-tree', '前缀和': 'prefix-sum', '字符串': 'string',
    '贪心': 'greedy', '位运算': 'bit-manipulation', '排列组合': 'backtracking',
    '双指针': 'two-pointers', '滑动窗口': 'sliding-window', '堆': 'heap',
    '矩阵运算': 'matrix', '栈': 'stack', '哈希': 'hash', '并查集': 'union-find',
    '快速排序': 'sorting', '归并排序': 'sorting', '逆序数': 'sorting',
    '牛顿迭代法': 'math', '大模拟': 'simulation', 'N数码问题': 'graph',
}
# 纯题号 py 文件按题目名关键词 → 分类
PY_KEYWORDS = [
    ('trie', 'trie'), ('word-search', 'backtracking'), ('generate-parentheses', 'backtracking'),
    ('buy-and-sell', 'dynamic-programming'), ('stock', 'dynamic-programming'),
    ('pow-x-n', 'math'), ('sqrt', 'math'),
    ('process-tasks', 'heap'), ('substring-with-concatenation', 'sliding-window'),
    ('binary-tree', 'tree'), ('lowest-common-ancestor', 'tree'),
    ('majority-element', 'hash'),
]
# 具体文件名 → 分类（覆盖规则化不中的）
NAME_MAP = {
    '0_白板.xlsx': 'misc', '0_調試.py': 'misc', 'jupyter本身的问题.ipynb': 'misc',
    'Leetcode.code-workspace': 'misc', 'leetcode.pynb': 'misc', 'tmp6278.png': 'misc',
    '如何使用leetcode插件': 'misc', '时间复杂度.ipynb': 'misc', '树状数组.md': 'binary-indexed-tree',
    '0特殊_循环数组的单调递增子序列的最大值.ipynb': 'binary-search',
    '基础算法_15_3sum.ipynb': 'two-pointers', '基础算法_16_set用法_twoSum.ipynb': 'hash',
    '基础算法_20_单调栈_判断括号字符否有效.ipynb': 'stack',
    '基础算法_242_哈希表_字母异位词.ipynb': 'hash',
    '基础算法_26原地删除有序数组中的重复项.ipynb': 'two-pointers',
    '基础算法_27_原地移除数组中的元素.ipynb': 'two-pointers',
    '基础算法_29_快速幂的变种快速减hhh.ipynb': 'math',
    '基础算法_415_高精度加.ipynb': 'math', '基础算法_43_高精乘.ipynb': 'math',
    '基础算法_ThreeSum.ipynb': 'two-pointers', '基础算法_ThreeSum变种.ipynb': 'two-pointers',
    '基础算法_Two_Sum.ipynb': 'hash', '基础算法_快速幂_50.ipynb': 'math',
    '基础算法_判定回文数字.ipynb': 'math',
}

IGNORED = {'.git', '.DS_Store', '.gitignore', 'README.md', 'LARGE_FILES.md', 'tools'}


def classify(fname):
    """文件名 → 分类目录。"""
    if fname in NAME_MAP:
        return NAME_MAP[fname]
    if fname.startswith('0_python') or fname.startswith('0_基本原理'):
        return 'python-basics'
    if fname.startswith('0_特殊'):
        return 'math'
    if fname.startswith('1_34') or fname.startswith('2_1870'):
        return 'binary-search'
    if fname.startswith('贪心-'):
        return 'greedy'
    m = re.match(r'^([A-Za-z\u4e00-\u9fff]+?)[_0-9]', fname)
    if m and m.group(1) in PREFIX_MAP:
        return PREFIX_MAP[m.group(1)]
    if re.match(r'^\d+\.', fname):  # 121.best-time-to-buy-and-sell-stock.py
        low = fname.lower()
        for kw, cat in PY_KEYWORDS:
            if kw in low:
                return cat
        return 'math'
    return 'misc'


def load_problem_index():
    """下载/读取 leetcode.cn 全量题目索引（题号 → slug）。"""
    cache = os.path.join(REPO, 'tools', '.lc-index.json')
    if os.path.exists(cache):
        with open(cache) as f:
            return json.load(f)
    print(f'下载题目索引 {INDEX_URL} ...')
    with urllib.request.urlopen(INDEX_URL, timeout=60) as r:
        data = json.loads(r.read())
    ids = {}
    for q in data['stat_status_pairs']:
        fid = str(q['stat']['frontend_question_id']).strip()
        if fid.isdigit():
            ids[int(fid)] = q['stat']['question__title_slug']
    with open(cache, 'w') as f:
        json.dump(ids, f)
    return ids


def extract_problem_id(fname, ids):
    """提取题号：忽略开头序号段（0_/1_/2_），取第一个命中索引的数字。"""
    base = fname
    m = re.match(r'^\d+_', base)
    if m:
        base = base[m.end():]
    for n in re.findall(r'\d+', base):
        if len(n) >= 2 and int(n) in ids:
            return int(n)
    return None


def fetch_statement(pid, ids):
    """按题号抓取题面，返回 markdown 字符串（含标题）。"""
    slug = ids[pid]
    q = json.dumps({'query': 'query{question(titleSlug:"%s"){title content}}' % slug}).encode()
    req = urllib.request.Request(GRAPHQL_URL, data=q,
                                 headers={'Content-Type': 'application/json',
                                          'Referer': 'https://leetcode.cn'})
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read())
    qd = d['data']['question']
    if not qd or not qd.get('content'):
        return None
    text = re.sub(r'<pre>.*?</pre>', '', qd['content'], flags=re.S)
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return f"# [{pid}] {qd['title']}\n\n{text}"


def has_statement(nb):
    """ipynb 首 cell 是否已含题面（以 [#] 标题开头）。"""
    cells = nb.get('cells') or []
    if not cells:
        return False
    src = ''.join(cells[0].get('source', []))
    return bool(re.match(r'^#\s*\[\d+\]', src.strip()))


def main():
    fetch_only = '--fetch-only' in sys.argv
    scan_all = '--all' in sys.argv
    os.chdir(REPO)

    # ---- 1. 分类移动 ----
    moved = {}
    if not fetch_only:
        sources = []
        # 只扫仓库根目录一层（不递归子目录），避免误移 2025-*/weekly-contest 等
        for fname in sorted(os.listdir('.')):
            if fname in IGNORED or os.path.isdir(fname):
                continue
            sources.append(('.', fname))
        # --all 时也扫 leetcode/misc
        if scan_all:
            for f in os.listdir(os.path.join(LEETCODE_DIR, 'misc')):
                if classify(f) != 'misc':
                    sources.append((f'leetcode/misc', f))
        for root, fname in sources:
            cat = classify(fname)
            if cat == 'misc' and root.startswith('leetcode'):
                continue  # 已分类过的跳过
            dest = os.path.join(LEETCODE_DIR, cat)
            os.makedirs(dest, exist_ok=True)
            src = os.path.join(root, fname)
            dst = os.path.join(dest, fname)
            if os.path.abspath(src) == os.path.abspath(dst) or os.path.exists(dst):
                continue
            if subprocess.run(['git', 'mv', src, dst]).returncode != 0:
                shutil.move(src, dst)  # 未跟踪文件用普通移动
                print(f'  移动(未跟踪) {fname} -> {cat}')
            else:
                print(f'  移动 {fname} -> {cat}')
            moved[cat] = moved.get(cat, 0) + 1
        if moved:
            print(f'本次移动 {sum(moved.values())} 个: {dict(sorted(moved.items()))}')
        else:
            print('无新文件需要移动')

    # ---- 2. 补题面 ----
    ids = load_problem_index()
    targets = []
    bad_files = []
    for root, _, fs in os.walk(LEETCODE_DIR):
        for f in fs:
            if not f.endswith('.ipynb'):
                continue
            path = os.path.join(root, f)
            try:
                nb = json.load(open(path))
            except (json.JSONDecodeError, OSError):
                bad_files.append(path)
                continue
            if not has_statement(nb):
                pid = extract_problem_id(f, ids)
                if pid:
                    targets.append((path, pid))
    if bad_files:
        print(f'警告: {len(bad_files)} 个损坏/非 JSON 的 ipynb 跳过:')
        for p in bad_files:
            print(f'  ! {p}')
    if targets:
        print(f'待补题面: {len(targets)}')
        with ThreadPoolExecutor(max_workers=10) as ex:
            stmts = dict(ex.map(lambda t: (t[0], fetch_statement(t[1], ids)), targets))
        inserted = 0
        for path, stmt in stmts.items():
            if not stmt:
                continue
            nb = json.load(open(path))
            nb['cells'].insert(0, {'cell_type': 'markdown', 'metadata': {},
                                   'source': [stmt]})
            json.dump(nb, open(path, 'w'), ensure_ascii=False, indent=1)
            inserted += 1
        print(f'已插入题面: {inserted}/{len(targets)}')
    else:
        print('无缺失题面')


if __name__ == '__main__':
    main()
