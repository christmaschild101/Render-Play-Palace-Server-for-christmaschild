# Локализация Senet

game-name-senet = Senet

# Начало игры
senet-game-started = { $p1 } — первый игрок, { $p2 } — второй игрок. Первым ходит { $first }.

# Бросок палочек
senet-throw = { $player } бросает палочки: { $result }.{ $bonus ->
    [yes] {" "}Дополнительный бросок!
   *[no] {""}
}

# Движение
senet-move-you = Вы перемещаете фишку с клетки { $from } на клетку { $to }.
senet-move-other = { $player } перемещает фишку с клетки { $from } на клетку { $to }.
senet-swap-you = Вы меняетесь местами с { $opponent } на клетке { $to }. { $opponent } возвращается на клетку { $from }.
senet-swap-other = { $player } меняется местами с { $opponent } на клетке { $to }. { $opponent } возвращается на клетку { $from }.
senet-bearoff-you = Вы выводите фишку с клетки { $from }. Осталось: { $remaining }.
senet-bearoff-other = { $player } выводит фишку с клетки { $from }. Осталось: { $remaining }.
senet-water-you = Вы попали в Дом Воды! Фишка отправлена на клетку { $dest }.
senet-water-other = { $player } попал в Дом Воды! Фишка отправлена на клетку { $dest }.
senet-happiness-you = Вы достигли Дома Счастья.
senet-happiness-other = { $player } достиг Дома Счастья.

# Нет ходов
senet-no-moves-you = У вас нет допустимых ходов.
senet-no-moves-other = У { $player } нет допустимых ходов.

# Описание клеток
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, ваша
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, ваша
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Названия особых клеток
senet-house-rebirth = Возрождение
senet-house-happiness = Счастье
senet-house-water = Вода
senet-house-three-truths = Три Истины
senet-house-re-atum = Ре-Атум

# Статус
senet-status = { $p1 }: выведено { $off1 }. { $p2 }: выведено { $off2 }.{ $phase ->
    [throwing] {" "}Ожидание броска.
   *[moving] {" "}Бросок: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Бросок ещё не сделан.

# Победа
senet-wins = { $player } побеждает! Все фишки выведены.

# Названия действий
senet-check-status = Статус
senet-check-sticks = Палочки
senet-check-score = Счёт
senet-score = { $p1 }: выведено { $off1 }. { $p2 }: выведено { $off2 }.

# Ошибки
senet-not-your-piece = Это не ваша фишка.
senet-no-piece-there = На этой клетке нет фишки.
senet-no-moves-from-here = С этой клетки нет допустимых ходов.

# Настройки
senet-option-bot-difficulty = Сложность бота: { $bot_difficulty }
senet-option-select-bot-difficulty = Выбрать сложность бота
senet-option-changed-bot-difficulty = Сложность бота установлена: { $bot_difficulty }.
senet-difficulty-random = Случайная
senet-difficulty-simple = Простая
