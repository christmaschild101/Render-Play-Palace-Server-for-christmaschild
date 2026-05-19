# Senet орчуулга

game-name-senet = Senet

# Тоглоом эхлэх
senet-game-started = { $p1 } — 1-р тоглогч, { $p2 } — 2-р тоглогч. { $first } эхэлнэ.

# Саваа шидэх
senet-throw = { $player } шидлээ: { $result }.{ $bonus ->
    [yes] {" "}Бонус шидэлт!
   *[no] {""}
}

# Хөдөлгөөн
senet-move-you = { $from }-р нүднээс { $to }-р нүд рүү явлаа.
senet-move-other = { $player } { $from }-р нүднээс { $to }-р нүд рүү явлаа.
senet-swap-you = { $to }-р нүд дээр { $opponent }-тай байр солилцлоо. { $opponent } { $from }-р нүд рүү буцлаа.
senet-swap-other = { $player } { $to }-р нүд дээр { $opponent }-тай байр солилцлоо. { $opponent } { $from }-р нүд рүү буцлаа.
senet-bearoff-you = { $from }-р нүднээс тавиур авлаа. { $remaining } үлдлээ.
senet-bearoff-other = { $player } { $from }-р нүднээс тавиур авлаа. { $remaining } үлдлээ.
senet-water-you = Усны Ордонд орлоо! Тавиур { $dest }-р нүд рүү явлаа.
senet-water-other = { $player } Усны Ордонд орлоо! Тавиур { $dest }-р нүд рүү явлаа.
senet-happiness-you = Жаргалын Ордонд хүрлээ.
senet-happiness-other = { $player } Жаргалын Ордонд хүрлээ.

# Хөдөлгөөн байхгүй
senet-no-moves-you = Танд зөвшөөрөгдсөн хөдөлгөөн байхгүй.
senet-no-moves-other = { $player }-д зөвшөөрөгдсөн хөдөлгөөн байхгүй.

# Нүдний шошго
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, таных
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, таных
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Тусгай нүдний нэрс
senet-house-rebirth = Дахин төрөлт
senet-house-happiness = Жаргал
senet-house-water = Ус
senet-house-three-truths = Гурван Үнэн
senet-house-re-atum = Re-Atum

# Байдал
senet-status = { $p1 }: { $off1 } гарсан. { $p2 }: { $off2 } гарсан.{ $phase ->
    [throwing] {" "}Шидэлтийг хүлээж байна.
   *[moving] {" "}Үр дүн: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Одоогоор шидээгүй.

# Ялалт
senet-wins = { $player } ялав! Бүх тавиур гарлаа.

# Үйлдлийн шошго
senet-check-status = Байдал
senet-check-sticks = Саваанууд
senet-check-score = Оноо
senet-score = { $p1 }: { $off1 } гарсан. { $p2 }: { $off2 } гарсан.

# Алдаанууд
senet-not-your-piece = Энэ таны тавиур биш.
senet-no-piece-there = Энэ нүдэнд тавиур байхгүй.
senet-no-moves-from-here = Энэ нүднээс зөвшөөрөгдсөн хөдөлгөөн байхгүй.

# Тохиргоо
senet-option-bot-difficulty = Ботын хүнд байдал: { $bot_difficulty }
senet-option-select-bot-difficulty = Ботын хүнд байдал сонгох
senet-option-changed-bot-difficulty = Ботын хүнд байдал тохируулагдлаа: { $bot_difficulty }.
senet-difficulty-random = Санамсаргүй
senet-difficulty-simple = Энгийн
