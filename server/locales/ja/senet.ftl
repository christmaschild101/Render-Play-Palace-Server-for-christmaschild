# セネトのローカライズ

game-name-senet = セネト

# ゲーム開始
senet-game-started = { $p1 }がプレイヤー1、{ $p2 }がプレイヤー2です。{ $first }が先攻です。

# 棒投げ
senet-throw = { $player }が{ $result }を投げました。{ $bonus ->
    [yes] {" "}ボーナス投げ！
   *[no] {""}
}

# 移動
senet-move-you = マス{ $from }からマス{ $to }へ移動しました。
senet-move-other = { $player }がマス{ $from }からマス{ $to }へ移動しました。
senet-swap-you = マス{ $to }で{ $opponent }と入れ替わりました。{ $opponent }はマス{ $from }に戻ります。
senet-swap-other = { $player }がマス{ $to }で{ $opponent }と入れ替わりました。{ $opponent }はマス{ $from }に戻ります。
senet-bearoff-you = マス{ $from }からコマを取り出しました。残り{ $remaining }個。
senet-bearoff-other = { $player }がマス{ $from }からコマを取り出しました。残り{ $remaining }個。
senet-water-you = 水の家に落ちました！コマはマス{ $dest }へ送られます。
senet-water-other = { $player }が水の家に落ちました！コマはマス{ $dest }へ送られます。
senet-happiness-you = 幸福の家に到達しました。
senet-happiness-other = { $player }が幸福の家に到達しました。

# 合法手なし
senet-no-moves-you = 合法手がありません。
senet-no-moves-other = { $player }には合法手がありません。

# マスのラベル
senet-sq-empty = { $sq }
senet-sq-own = { $sq }、自分のコマ
senet-sq-opponent = { $sq }、{ $owner }
senet-sq-empty-special = { $sq }、{ $name }
senet-sq-own-special = { $sq }、{ $name }、自分のコマ
senet-sq-opponent-special = { $sq }、{ $name }、{ $owner }

# 特殊マスの名前
senet-house-rebirth = 再生
senet-house-happiness = 幸福
senet-house-water = 水
senet-house-three-truths = 三つの真実
senet-house-re-atum = レ＝アトゥム

# ステータス
senet-status = { $p1 }：{ $off1 }個取り出し済み。{ $p2 }：{ $off2 }個取り出し済み。{ $phase ->
    [throwing] {" "}投げ待ち中。
   *[moving] {" "}出目：{ $roll }。
}
senet-sticks = { $result }
senet-sticks-none = まだ投げていません。

# 勝利
senet-wins = { $player }の勝利！全コマを取り出しました。

# アクションラベル
senet-check-status = ステータス
senet-check-sticks = 棒の結果
senet-check-score = スコア
senet-score = { $p1 }：{ $off1 }個。{ $p2 }：{ $off2 }個。

# エラー
senet-not-your-piece = 自分のコマではありません。
senet-no-piece-there = そこにコマはありません。
senet-no-moves-from-here = このマスから合法手はありません。

# オプション
senet-option-bot-difficulty = ボット難易度：{ $bot_difficulty }
senet-option-select-bot-difficulty = ボット難易度を選択
senet-option-changed-bot-difficulty = ボット難易度を{ $bot_difficulty }に設定しました。
senet-difficulty-random = ランダム
senet-difficulty-simple = 簡単
