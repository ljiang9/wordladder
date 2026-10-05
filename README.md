# wordladder 单词接龙(词梯)

每次只换一个字母, 把一个单词变成另一个单词的小游戏。纯标准库, 零依赖。

## 安装 / 运行

```bash
python -m wordladder play              # 随机题目开始玩
python -m wordladder play CAT DOG      # 指定起点和终点
python -m wordladder solve CAT DOG     # 只看最短解法(BFS)
python -m wordladder solve CAT DOG --length 4  # 仅限 4 字母词
```

## 规则

- 每一步必须**恰好改变一个字母**, 且结果必须在内置词表里。
- 例如: CAT -> COT -> DOT -> DOG(3 步)。
- 交互模式下输入 `q` 退出; 通关后会告诉你最短步数是多少。

## 设计取舍

- 求解用 **BFS**, 保证找到的词梯是最短的。
- 词表是内置的约 200 个常见 3–5 字母英文单词, 全部小写、去重。
- 随机题目会挑"最短路径 ≥ 4 步"的词对, 太简单的题直接跳过。
- 邻居按字母序枚举, 同一输入的结果可复现。

## 已知局限

- 内置词表很小(~200 词), 很多词对无解; 这是"小巧"的代价, 想加词直接改 `WORDS`。
- 只支持英文单词, 无中文模式。
- `solve` 要求起点终点等长且都在词表里, 否则直接报无解。

## License

MIT, Copyright (c) 2026 ljiang9.
