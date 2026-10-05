"""wordladder - 单词接龙(词梯)游戏: 每次只换一个字母, 从一个单词变成另一个单词。

用法:
    python -m wordladder play            # 交互玩(随机给起点/终点)
    python -m wordladder play CAT DOG    # 交互玩(指定起点/终点)
    python -m wordladder solve CAT DOG   # BFS 求最短变换序列
    python -m wordladder solve CAT DOG --length 4  # 仅限 4 字母词

规则: 每一步必须恰好改变一个字母, 且结果必须在词表里。
"""

import argparse
import random
import sys
from collections import deque

WORDS = """cat cot dot dog hot hog log fog frog dig dug pig big bag bat bet
bet bar car care dare fare fear gear hear near pear rear tear wear
year ball call fall hall mall tall wall well bell sell tell spell
smell shell doll full bull pull bull dull gull hill hill pill sill
will will fill fill kill hill mill nil oil foil boil coil soil
toil door poor boor boon boor book book look took cook hook
rook shook brook brook brook stool stool spool spool spool cool
pool tool fool wool wool wool blood flood floor flour flour
flour four tour sour your hour our
our out put put pet pet pen pen pin pin pan pan pat pat
pot pot pod pod nod nod nod fog fog hog hog jog jog
jog jug jug mug mug bug bug bud bud bid bid big big
big dig dig dog dog dot dot cot cot cat cat cap cap
cup cup pup pup pop pop top top tap tap tip tip
tip tin tin sin sin sun sun run run ran ran ban ban
man man map map mop mop hop hop hot hot hit hit
sit sit sat sat set set bet bet bit bit bat bat
bad bad bed bed bud bud bun bun fun fun fan fan
fin fin win win wine wine dine dine dime dime
time time lime lime like like bike bike bake bake
cake cake lake lake make make take take tale tale
sale sale male male pale pale pile pile mile mile
smile smile tile tile while while white white write write
right right light light fight fight night night
eight eight sight sight tight tight might might
""".split()

# 去重并保证都是小写字母
WORDS = sorted({w.strip().lower() for w in WORDS if w.strip().isalpha()})


def differ_by_one(a, b):
    """a 与 b 是否恰好差一个字母(同长度)。"""
    if len(a) != len(b):
        return False
    return sum(x != y for x, y in zip(a, b)) == 1


def neighbors(word, wordset):
    """word 的所有一步邻居(按字母序, 保证可复现)。"""
    return sorted(w for w in wordset if differ_by_one(word, w))


def solve(start, end, words):
    """BFS 求最短词梯; 返回单词列表, 无解返回 None。"""
    start, end = start.lower(), end.lower()
    if len(start) != len(end):
        return None
    wordset = {w for w in words if len(w) == len(start)}
    if start not in wordset or end not in wordset:
        return None
    if start == end:
        return [start]
    prev = {start: None}
    queue = deque([start])
    while queue:
        cur = queue.popleft()
        for nb in neighbors(cur, wordset):
            if nb not in prev:
                prev[nb] = cur
                if nb == end:
                    path = [end]
                    while prev[path[-1]] is not None:
                        path.append(prev[path[-1]])
                    return path[::-1]
                queue.append(nb)
    return None


def pick_puzzle(words, length, rng):
    """随机挑一对有解的(起点, 终点)。"""
    pool = [w for w in words if len(w) == length]
    for _ in range(200):
        a, b = rng.sample(pool, 2)
        path = solve(a, b, words)
        if path and len(path) >= 4:  # 太短的没意思
            return a, b
    return pool[0], pool[1]


def play(start, end, words):
    print(f"目标: {start.upper()} -> {end.upper()}")
    print("规则: 每次输入一个单词, 必须恰好改变一个字母, 且必须在词表里。输入 q 退出。\n")
    cur = start
    steps = 0
    while cur != end:
        print(f"当前: {cur.upper()}  (已走 {steps} 步)")
        try:
            guess = input("下一步: ").strip().lower()
        except EOFError:
            print("\n再见!")
            return 1
        if guess in ("q", "quit", "退出"):
            print("再见!")
            return 1
        if len(guess) != len(cur):
            print(f"长度不对, 请输入 {len(cur)} 个字母的单词。")
            continue
        if guess not in words:
            print("这个单词不在词表里, 换一个。")
            continue
        if not differ_by_one(cur, guess):
            print("必须恰好改变一个字母!")
            continue
        cur = guess
        steps += 1
    print(f"\n🎉 成功! {start.upper()} -> {end.upper()}, 共用了 {steps} 步。")
    best = solve(start, end, words)
    if best:
        print(f"最短步数是 {len(best) - 1} 步: {' -> '.join(w.upper() for w in best)}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="单词接龙(词梯): 每次只换一个字母, 从一个单词变成另一个单词。")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_play = sub.add_parser("play", help="交互玩")
    p_play.add_argument("start", nargs="?", help="起点单词(默认随机)")
    p_play.add_argument("end", nargs="?", help="终点单词(默认随机)")
    p_play.add_argument("--length", type=int, default=3, help="随机题目时的单词长度(默认 3)")

    p_solve = sub.add_parser("solve", help="BFS 求最短变换序列")
    p_solve.add_argument("start", help="起点单词")
    p_solve.add_argument("end", help="终点单词")
    p_solve.add_argument("--length", type=int, default=None, help="仅限该长度的词表")

    args = parser.parse_args(argv)
    words = WORDS
    if args.length is not None and args.cmd == "solve":
        words = [w for w in WORDS if len(w) == args.length]

    if args.cmd == "solve":
        path = solve(args.start, args.end, words)
        if path is None:
            print(f"无解: {args.start.upper()} -> {args.end.upper()} (检查长度/词表)")
            return 1
        print(" -> ".join(w.upper() for w in path))
        print(f"共 {len(path) - 1} 步")
        return 0

    # play
    rng = random.Random()
    if args.start and args.end:
        start, end = args.start.lower(), args.end.lower()
        if len(start) != len(end):
            print("error: 起点和终点长度必须相同", file=sys.stderr)
            return 2
        if start not in WORDS or end not in WORDS:
            print("error: 起点/终点不在词表里", file=sys.stderr)
            return 2
    else:
        start, end = pick_puzzle(WORDS, args.length, rng)
    return play(start, end, WORDS)


if __name__ == "__main__":
    raise SystemExit(main())
