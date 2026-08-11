#!/usr/bin/env python3
"""cp.py — 刷题脚本组件

用法（在某题目录内运行，路径写相对/绝对均可）：
  python3 cp.py new <题目名> [--lang rs|py]   建题目脚手架
  python3 cp.py test <题目目录>               跑 tests/ 下所有样例对，diff 校验
  python3 cp.py stress <题目目录> [-n 次数]   对拍：gen.py 造数据，正解 vs brute.py
  python3 cp.py time <题目目录> [-i 输入文件] 计时跑一次（默认最大样例）

约定（零配置的根基）：
  正解：  <dir>/src/main.rs（cargo 工程）或 <dir>/sol.py，二者有其一
  暴力：  <dir>/brute.py
  生成器：<dir>/gen.py（向 stdout 打印一组随机数据）
  样例：  <dir>/tests/N.in 与 N.ans 成对
"""
import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATES = ROOT / "templates"

# ---------- 工具 ----------

def run(cmd, stdin_file=None, input_text=None, timeout=10):
    """跑命令，返回 (stdout, 耗时秒, 是否超时/出错)。输入可给文件或字符串。"""
    start = time.perf_counter()
    try:
        if stdin_file:
            with open(stdin_file) as f:
                proc = subprocess.run(cmd, stdin=f, capture_output=True,
                                      text=True, timeout=timeout)
        else:
            proc = subprocess.run(cmd, input=input_text or "",
                                  capture_output=True, text=True, timeout=timeout)
        return proc.stdout, time.perf_counter() - start, proc.returncode != 0
    except subprocess.TimeoutExpired:
        return "", timeout, True


def solution_cmd(problem: Path):
    """探测正解怎么跑：优先 cargo（release），其次 sol.py。"""
    if (problem / "Cargo.toml").exists():
        subprocess.run(["cargo", "build", "--release"], cwd=problem,
                       capture_output=True, check=True)
        return [str(problem / "target" / "release" / problem.name)]
    if (problem / "sol.py").exists():
        return [sys.executable, str(problem / "sol.py")]
    sys.exit(f"在 {problem} 里没找到 src/main.rs 或 sol.py")


def compare(out: str, ans: str) -> bool:
    """按行比较，忽略行尾空白和末尾空行（兼容多数 OJ 的判题习惯）。"""
    norm = lambda s: [line.rstrip() for line in s.strip().splitlines()]
    return norm(out) == norm(ans)

# ---------- 命令 ----------

def cmd_new(args):
    target = ROOT / args.name
    if target.exists():
        sys.exit(f"{target} 已存在")
    if args.lang == "rs":
        subprocess.run(["cargo", "new", str(target), "--vcs", "none"], check=True)
    else:
        target.mkdir(parents=True)
        shutil.copy(TEMPLATES / "sol.py", target / "sol.py")
    shutil.copy(TEMPLATES / "brute.py", target / "brute.py")
    shutil.copy(TEMPLATES / "gen.py", target / "gen.py")
    (target / "tests").mkdir(exist_ok=True)
    (target / "tests" / "1.in").write_text("")
    (target / "tests" / "1.ans").write_text("")
    print(f"✓ 建好 {args.name}（{args.lang}），去写 {args.name}/"
          f"{'src/main.rs' if args.lang == 'rs' else 'sol.py'} 吧")


def cmd_test(args):
    problem = Path(args.dir).resolve()
    cmd = solution_cmd(problem)
    cases = sorted((problem / "tests").glob("*.in"))
    if not cases:
        sys.exit("tests/ 下没有 .in 文件")
    failed = 0
    for in_file in cases:
        ans_file = in_file.with_suffix(".ans")
        out, elapsed, bad = run(cmd, stdin_file=in_file)
        ok = not bad and compare(out, ans_file.read_text())
        mark = "✓" if ok else "✗"
        print(f"{mark} {in_file.name:8s} {elapsed*1000:7.1f}ms")
        if not ok:
            failed += 1
            print(f"  期望:\n{ans_file.read_text()}\n  实际:\n{out}")
    sys.exit(1 if failed else 0)


def cmd_stress(args):
    problem = Path(args.dir).resolve()
    sol = solution_cmd(problem)
    brute = [sys.executable, str(problem / "brute.py")]
    gen = [sys.executable, str(problem / "gen.py")]
    for i in range(1, args.n + 1):
        data, _, bad = run(gen)
        if bad:
            sys.exit("gen.py 出错了")
        out1, _, bad1 = run(sol, input_text=data)
        out2, _, bad2 = run(brute, input_text=data)
        if bad1 or bad2:
            Path("counterexample.txt").write_text(data)
            print(f"✗ 第 {i} 组有进程出错/超时！数据已存 counterexample.txt")
            sys.exit(1)
        if not compare(out1, out2):
            Path("counterexample.txt").write_text(data)
            print(f"✗ 第 {i} 组对拍失败！反例已存 counterexample.txt")
            print(f"正解输出:\n{out1}\n暴力输出:\n{out2}")
            sys.exit(1)
    print(f"✓ {args.n} 组对拍全部一致")


def cmd_time(args):
    problem = Path(args.dir).resolve()
    cmd = solution_cmd(problem)
    in_file = Path(args.input) if args.input else max(
        (problem / "tests").glob("*.in"), key=lambda p: p.stat().st_size)
    _, elapsed, bad = run(cmd, stdin_file=in_file, timeout=60)
    status = "出错/超时" if bad else "完成"
    print(f"{status}，耗时 {elapsed*1000:.1f}ms（输入 {in_file.name}）")


def main():
    parser = argparse.ArgumentParser(description="刷题脚本组件")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("new", help="建题目脚手架")
    p.add_argument("name")
    p.add_argument("--lang", choices=["rs", "py"], default="rs")
    p.set_defaults(fn=cmd_new)

    p = sub.add_parser("test", help="跑样例对")
    p.add_argument("dir")
    p.set_defaults(fn=cmd_test)

    p = sub.add_parser("stress", help="对拍")
    p.add_argument("dir")
    p.add_argument("-n", type=int, default=1000)
    p.set_defaults(fn=cmd_stress)

    p = sub.add_parser("time", help="计时")
    p.add_argument("dir")
    p.add_argument("-i", "--input")
    p.set_defaults(fn=cmd_time)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
