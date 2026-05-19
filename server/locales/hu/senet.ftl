# Senet lokalizáció

game-name-senet = Senet

# Játék kezdete
senet-game-started = { $p1 } az 1. játékos, { $p2 } a 2. játékos. { $first } kezd.

# Dobópálcák
senet-throw = { $player } dob: { $result }.{ $bonus ->
    [yes] {" "}Bónuszdobás!
   *[no] {""}
}

# Mozgás
senet-move-you = A(z) { $from }. mezőről a(z) { $to }. mezőre lép.
senet-move-other = { $player } a(z) { $from }. mezőről a(z) { $to }. mezőre lép.
senet-swap-you = Felcseréled { $opponent } bábúját a(z) { $to }. mezőn. { $opponent } visszakerül a(z) { $from }. mezőre.
senet-swap-other = { $player } felcseréli { $opponent } bábúját a(z) { $to }. mezőn. { $opponent } visszakerül a(z) { $from }. mezőre.
senet-bearoff-you = Leveszed a bábút a(z) { $from }. mezőről. Még { $remaining } maradt.
senet-bearoff-other = { $player } leveszi a bábút a(z) { $from }. mezőről. Még { $remaining } maradt.
senet-water-you = A Víz Házába léptél! A bábu a(z) { $dest }. mezőre kerül.
senet-water-other = { $player } a Víz Házába lépett! A bábu a(z) { $dest }. mezőre kerül.
senet-happiness-you = Elérted a Boldogság Házát.
senet-happiness-other = { $player } elérte a Boldogság Házát.

# Nincs lépés
senet-no-moves-you = Nincs érvényes lépésed.
senet-no-moves-other = { $player }nek nincs érvényes lépése.

# Mezőfeliratok
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, tiéd
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, tiéd
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Különleges mezők nevei
senet-house-rebirth = Újjászületés
senet-house-happiness = Boldogság
senet-house-water = Víz
senet-house-three-truths = Három Igazság
senet-house-re-atum = Re-Atum

# Állapot
senet-status = { $p1 }: { $off1 } le. { $p2 }: { $off2 } le.{ $phase ->
    [throwing] {" "}Dobásra vár.
   *[moving] {" "}Dobás: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Még nem dobott.

# Győzelem
senet-wins = { $player } nyert! Minden bábu levéve.

# Műveletek neve
senet-check-status = Állapot
senet-check-sticks = Pálcák
senet-check-score = Pontszám
senet-score = { $p1 }: { $off1 } le. { $p2 }: { $off2 } le.

# Hibák
senet-not-your-piece = Ez nem a te bábud.
senet-no-piece-there = Ezen a mezőn nincs bábu.
senet-no-moves-from-here = Erről a mezőről nincs érvényes lépés.

# Beállítások
senet-option-bot-difficulty = Bot nehézség: { $bot_difficulty }
senet-option-select-bot-difficulty = Bot nehézség kiválasztása
senet-option-changed-bot-difficulty = Bot nehézség beállítva: { $bot_difficulty }.
senet-difficulty-random = Véletlenszerű
senet-difficulty-simple = Egyszerű
