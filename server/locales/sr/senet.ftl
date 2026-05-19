# Локализација Сенета

game-name-senet = Senet

# Почетак игре
senet-game-started = { $p1 } је играч 1, { $p2 } је играч 2. { $first } иде први.

# Бацање штапића
senet-throw = { $player } баца { $result }.{ $bonus ->
    [yes] {" "}Додатно бацање!
   *[no] {""}
}

# Кретање
senet-move-you = Померате се са поља { $from } на поље { $to }.
senet-move-other = { $player } се помера са поља { $from } на поље { $to }.
senet-swap-you = Мењате се са { $opponent } на пољу { $to }. { $opponent } се враћа на поље { $from }.
senet-swap-other = { $player } се мења са { $opponent } на пољу { $to }. { $opponent } се враћа на поље { $from }.
senet-bearoff-you = Изводите фигуру са поља { $from }. Преостало { $remaining }.
senet-bearoff-other = { $player } изводи фигуру са поља { $from }. Преостало { $remaining }.
senet-water-you = Слетели сте у Кућу воде! Фигура послата на поље { $dest }.
senet-water-other = { $player } је слетео у Кућу воде! Фигура послата на поље { $dest }.
senet-happiness-you = Стигли сте до Куће среће.
senet-happiness-other = { $player } је стигао до Куће среће.

# Нема потеза
senet-no-moves-you = Немате ниједан дозвољени потез.
senet-no-moves-other = { $player } нема ниједан дозвољени потез.

# Описи поља
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, ваше
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, ваше
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Називи посебних поља
senet-house-rebirth = Препород
senet-house-happiness = Срећа
senet-house-water = Вода
senet-house-three-truths = Три истине
senet-house-re-atum = Re-Atum

# Стање игре
senet-status = { $p1 }: { $off1 } изведених. { $p2 }: { $off2 } изведених.{ $phase ->
    [throwing] {" "}Чека се бацање.
   *[moving] {" "}Бацање: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Још нема бацања.

# Победа
senet-wins = { $player } побеђује! Све фигуре су изведене.

# Ознаке радњи
senet-check-status = Стање
senet-check-sticks = Штапићи
senet-check-score = Резултат
senet-score = { $p1 }: { $off1 } изведених. { $p2 }: { $off2 } изведених.

# Грешке
senet-not-your-piece = То није ваша фигура.
senet-no-piece-there = На том пољу нема фигуре.
senet-no-moves-from-here = С овог поља нема дозвољених потеза.

# Могућности
senet-option-bot-difficulty = Тежина бота: { $bot_difficulty }
senet-option-select-bot-difficulty = Одаберите тежину бота
senet-option-changed-bot-difficulty = Тежина бота постављена на { $bot_difficulty }.
senet-difficulty-random = Насумично
senet-difficulty-simple = Једноставно
