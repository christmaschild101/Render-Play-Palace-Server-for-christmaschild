# Локалізація Senet

game-name-senet = Senet

# Початок гри
senet-game-started = { $p1 } — перший гравець, { $p2 } — другий гравець. Першим ходить { $first }.

# Кидання паличок
senet-throw = { $player } кидає палички: { $result }.{ $bonus ->
    [yes] {" "}Додатковий кидок!
   *[no] {""}
}

# Рух
senet-move-you = Ви переміщуєте фішку з клітинки { $from } на клітинку { $to }.
senet-move-other = { $player } переміщує фішку з клітинки { $from } на клітинку { $to }.
senet-swap-you = Ви міняєтеся місцями з { $opponent } на клітинці { $to }. { $opponent } повертається на клітинку { $from }.
senet-swap-other = { $player } міняється місцями з { $opponent } на клітинці { $to }. { $opponent } повертається на клітинку { $from }.
senet-bearoff-you = Ви виводите фішку з клітинки { $from }. Залишилось: { $remaining }.
senet-bearoff-other = { $player } виводить фішку з клітинки { $from }. Залишилось: { $remaining }.
senet-water-you = Ви потрапили до Дому Води! Фішку відправлено на клітинку { $dest }.
senet-water-other = { $player } потрапив до Дому Води! Фішку відправлено на клітинку { $dest }.
senet-happiness-you = Ви досягли Дому Щастя.
senet-happiness-other = { $player } досяг Дому Щастя.

# Немає ходів
senet-no-moves-you = У вас немає допустимих ходів.
senet-no-moves-other = У { $player } немає допустимих ходів.

# Опис клітинок
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, ваша
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, ваша
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Назви особливих клітинок
senet-house-rebirth = Відродження
senet-house-happiness = Щастя
senet-house-water = Вода
senet-house-three-truths = Три Істини
senet-house-re-atum = Ре-Атум

# Статус
senet-status = { $p1 }: виведено { $off1 }. { $p2 }: виведено { $off2 }.{ $phase ->
    [throwing] {" "}Очікування кидка.
   *[moving] {" "}Кидок: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Кидок ще не зроблено.

# Перемога
senet-wins = { $player } перемагає! Всі фішки виведено.

# Назви дій
senet-check-status = Статус
senet-check-sticks = Палички
senet-check-score = Рахунок
senet-score = { $p1 }: виведено { $off1 }. { $p2 }: виведено { $off2 }.

# Помилки
senet-not-your-piece = Це не ваша фішка.
senet-no-piece-there = На цій клітинці немає фішки.
senet-no-moves-from-here = З цієї клітинки немає допустимих ходів.

# Налаштування
senet-option-bot-difficulty = Складність бота: { $bot_difficulty }
senet-option-select-bot-difficulty = Вибрати складність бота
senet-option-changed-bot-difficulty = Складність бота встановлено: { $bot_difficulty }.
senet-difficulty-random = Випадкова
senet-difficulty-simple = Проста
