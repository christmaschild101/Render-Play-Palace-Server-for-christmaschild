# 세네트 현지화

game-name-senet = 세네트

# 게임 시작
senet-game-started = { $p1 }이(가) 플레이어 1, { $p2 }이(가) 플레이어 2입니다. { $first }이(가) 먼저 시작합니다.

# 막대 던지기
senet-throw = { $player }이(가) { $result }을(를) 던졌습니다.{ $bonus ->
    [yes] {" "}보너스 던지기!
   *[no] {""}
}

# 이동
senet-move-you = { $from }번 칸에서 { $to }번 칸으로 이동했습니다.
senet-move-other = { $player }이(가) { $from }번 칸에서 { $to }번 칸으로 이동했습니다.
senet-swap-you = { $to }번 칸에서 { $opponent }와(과) 자리를 바꿨습니다. { $opponent }은(는) { $from }번 칸으로 돌아갑니다.
senet-swap-other = { $player }이(가) { $to }번 칸에서 { $opponent }와(과) 자리를 바꿨습니다. { $opponent }은(는) { $from }번 칸으로 돌아갑니다.
senet-bearoff-you = { $from }번 칸에서 말을 꺼냈습니다. 남은 말: { $remaining }개.
senet-bearoff-other = { $player }이(가) { $from }번 칸에서 말을 꺼냈습니다. 남은 말: { $remaining }개.
senet-water-you = 물의 집에 빠졌습니다! 말이 { $dest }번 칸으로 이동합니다.
senet-water-other = { $player }이(가) 물의 집에 빠졌습니다! 말이 { $dest }번 칸으로 이동합니다.
senet-happiness-you = 행복의 집에 도달했습니다.
senet-happiness-other = { $player }이(가) 행복의 집에 도달했습니다.

# 이동 불가
senet-no-moves-you = 가능한 이동이 없습니다.
senet-no-moves-other = { $player }은(는) 가능한 이동이 없습니다.

# 칸 레이블
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, 내 말
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, 내 말
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# 특수 칸 이름
senet-house-rebirth = 재생
senet-house-happiness = 행복
senet-house-water = 물
senet-house-three-truths = 세 가지 진실
senet-house-re-atum = 레-아툼

# 상태
senet-status = { $p1 }: { $off1 }개 꺼냄. { $p2 }: { $off2 }개 꺼냄.{ $phase ->
    [throwing] {" "}던지기 대기 중.
   *[moving] {" "}결과: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = 아직 던지지 않았습니다.

# 승리
senet-wins = { $player } 승리! 모든 말을 꺼냈습니다.

# 액션 레이블
senet-check-status = 상태
senet-check-sticks = 막대 결과
senet-check-score = 점수
senet-score = { $p1 }: { $off1 }개. { $p2 }: { $off2 }개.

# 오류
senet-not-your-piece = 내 말이 아닙니다.
senet-no-piece-there = 그 칸에 말이 없습니다.
senet-no-moves-from-here = 이 칸에서 가능한 이동이 없습니다.

# 옵션
senet-option-bot-difficulty = 봇 난이도: { $bot_difficulty }
senet-option-select-bot-difficulty = 봇 난이도 선택
senet-option-changed-bot-difficulty = 봇 난이도가 { $bot_difficulty }(으)로 설정되었습니다.
senet-difficulty-random = 랜덤
senet-difficulty-simple = 쉬움
