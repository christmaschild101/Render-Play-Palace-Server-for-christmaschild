# Lokalizácia Senetu

game-name-senet = Senet

# Začiatok hry
senet-game-started = { $p1 } je hráč 1, { $p2 } je hráč 2. { $first } začína.

# Hádzanie tyčiek
senet-throw = { $player } hodí { $result }.{ $bonus ->
    [yes] {" "}Bonusový hod!
   *[no] {""}
}

# Pohyb
senet-move-you = Presuniete sa z políčka { $from } na políčko { $to }.
senet-move-other = { $player } sa presunie z políčka { $from } na políčko { $to }.
senet-swap-you = Vymeníte sa s { $opponent } na políčku { $to }. { $opponent } sa vráti na políčko { $from }.
senet-swap-other = { $player } sa vymení s { $opponent } na políčku { $to }. { $opponent } sa vráti na políčko { $from }.
senet-bearoff-you = Vynesie sa figúrka z políčka { $from }. Zostáva { $remaining }.
senet-bearoff-other = { $player } vynesie figúrku z políčka { $from }. Zostáva { $remaining }.
senet-water-you = Pristáli ste v Dome vody! Figúrka odoslaná na políčko { $dest }.
senet-water-other = { $player } pristál v Dome vody! Figúrka odoslaná na políčko { $dest }.
senet-happiness-you = Dosiahli ste Dom šťastia.
senet-happiness-other = { $player } dosiahol Dom šťastia.

# Žiadne ťahy
senet-no-moves-you = Nemáte žiadne platné ťahy.
senet-no-moves-other = { $player } nemá žiadne platné ťahy.

# Popis políčok
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, vaše
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, vaše
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Názvy špeciálnych políčok
senet-house-rebirth = Znovuzrodenie
senet-house-happiness = Šťastie
senet-house-water = Voda
senet-house-three-truths = Tri pravdy
senet-house-re-atum = Re-Atum

# Stav hry
senet-status = { $p1 }: { $off1 } vynesených. { $p2 }: { $off2 } vynesených.{ $phase ->
    [throwing] {" "}Čaká sa na hod.
   *[moving] {" "}Hod: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Zatiaľ žiadny hod.

# Výhra
senet-wins = { $player } vyhral! Všetky figúrky sú vynesené.

# Popisky akcií
senet-check-status = Stav
senet-check-sticks = Tyčky
senet-check-score = Skóre
senet-score = { $p1 }: { $off1 } vynesených. { $p2 }: { $off2 } vynesených.

# Chyby
senet-not-your-piece = To nie je vaša figúrka.
senet-no-piece-there = Na tomto políčku nie je žiadna figúrka.
senet-no-moves-from-here = Z tohto políčka nie sú žiadne platné ťahy.

# Možnosti
senet-option-bot-difficulty = Obtiažnosť bota: { $bot_difficulty }
senet-option-select-bot-difficulty = Vyberte obtiažnosť bota
senet-option-changed-bot-difficulty = Obtiažnosť bota nastavená na { $bot_difficulty }.
senet-difficulty-random = Náhodný
senet-difficulty-simple = Jednoduchý
