# 塞尼特本地化

game-name-senet = 塞尼特

# 游戏开始
senet-game-started = { $p1 } 是玩家一，{ $p2 } 是玩家二。{ $first } 先手。

# 投掷棍棒
senet-throw = { $player } 投出了 { $result }。{ $bonus ->
    [yes] {" "}额外投掷！
   *[no] {""}
}

# 移动
senet-move-you = 您从第 { $from } 格移动到第 { $to } 格。
senet-move-other = { $player } 从第 { $from } 格移动到第 { $to } 格。
senet-swap-you = 您与第 { $to } 格的 { $opponent } 互换位置。{ $opponent } 退回第 { $from } 格。
senet-swap-other = { $player } 与第 { $to } 格的 { $opponent } 互换位置。{ $opponent } 退回第 { $from } 格。
senet-bearoff-you = 您从第 { $from } 格移出棋子。剩余 { $remaining } 枚。
senet-bearoff-other = { $player } 从第 { $from } 格移出棋子。剩余 { $remaining } 枚。
senet-water-you = 您落入了水之殿！棋子被送往第 { $dest } 格。
senet-water-other = { $player } 落入了水之殿！棋子被送往第 { $dest } 格。
senet-happiness-you = 您到达了幸福之殿。
senet-happiness-other = { $player } 到达了幸福之殿。

# 无合法移动
senet-no-moves-you = 您没有合法移动。
senet-no-moves-other = { $player } 没有合法移动。

# 格子标签
senet-sq-empty = { $sq }
senet-sq-own = { $sq }，己方棋子
senet-sq-opponent = { $sq }，{ $owner }
senet-sq-empty-special = { $sq }，{ $name }
senet-sq-own-special = { $sq }，{ $name }，己方棋子
senet-sq-opponent-special = { $sq }，{ $name }，{ $owner }

# 特殊格子名称
senet-house-rebirth = 重生之殿
senet-house-happiness = 幸福之殿
senet-house-water = 水之殿
senet-house-three-truths = 三真之殿
senet-house-re-atum = 拉-阿图姆之殿

# 状态
senet-status = { $p1 }：已移出 { $off1 } 枚。{ $p2 }：已移出 { $off2 } 枚。{ $phase ->
    [throwing] {" "}等待投掷。
   *[moving] {" "}点数：{ $roll }。
}
senet-sticks = { $result }
senet-sticks-none = 尚未投掷。

# 胜利
senet-wins = { $player } 获胜！所有棋子已全部移出。

# 操作标签
senet-check-status = 状态
senet-check-sticks = 棍棒结果
senet-check-score = 分数
senet-score = { $p1 }：{ $off1 } 枚。{ $p2 }：{ $off2 } 枚。

# 错误
senet-not-your-piece = 这不是您的棋子。
senet-no-piece-there = 该格子没有棋子。
senet-no-moves-from-here = 该格子没有合法移动。

# 选项
senet-option-bot-difficulty = 机器人难度：{ $bot_difficulty }
senet-option-select-bot-difficulty = 选择机器人难度
senet-option-changed-bot-difficulty = 机器人难度已设置为{ $bot_difficulty }。
senet-difficulty-random = 随机
senet-difficulty-simple = 简单
