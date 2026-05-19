# Ukuhumusha komdlalo i-Senet

game-name-senet = Senet

# Ukuqala komdlalo
senet-game-started = { $p1 } ungumidlali wokuqala, { $p2 } ungumidlali wesibili. { $first } uqala kuqala.

# Ukuphonsa izinti
senet-throw = { $player } uphonsa { $result }.{ $bonus ->
    [yes] {" "}Ukuphonsa kwengeziwe!
   *[no] {""}
}

# Ukuhamba
senet-move-you = Uhamba esikweyini { $from } uya esikweyini { $to }.
senet-move-other = { $player } uhamba esikweyini { $from } uya esikweyini { $to }.
senet-swap-you = Ushintsha indawo no-{ $opponent } esikweyini { $to }. { $opponent } ubuyela esikweyini { $from }.
senet-swap-other = { $player } ushintsha indawo no-{ $opponent } esikweyini { $to }. { $opponent } ubuyela esikweyini { $from }.
senet-bearoff-you = Ukukhipha uphawu lwakho esikweyini { $from }. { $remaining } kusele.
senet-bearoff-other = { $player } ukukhipha uphawu lwakhe esikweyini { $from }. { $remaining } kusele.
senet-water-you = Ufikile eNdlini Yamanzi! Uphawu luthunyelwe esikweyini { $dest }.
senet-water-other = { $player } ufikile eNdlini Yamanzi! Uphawu luthunyelwe esikweyini { $dest }.
senet-happiness-you = Ufikile eNdlini Yenjabulo.
senet-happiness-other = { $player } ufikile eNdlini Yenjabulo.

# Akukho zinyathelo
senet-no-moves-you = Awunazo izinyathelo ezisemthethweni.
senet-no-moves-other = { $player } akanazinyathelo ezisemthethweni.

# Izihloko zezikwele
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, elakho
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, elakho
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Amagama ezikwele ezikhethekile
senet-house-rebirth = Ukuzalwa Kabusha
senet-house-happiness = Injabulo
senet-house-water = Amanzi
senet-house-three-truths = Amaqiniso Amathathu
senet-house-re-atum = Re-Atum

# Isimo
senet-status = { $p1 }: { $off1 } phandle. { $p2 }: { $off2 } phandle.{ $phase ->
    [throwing] {" "}Ilindile ukuphonsa.
   *[moving] {" "}Inombolo: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Akukaphonswa nakanye.

# Ukuwina
senet-wins = { $player } uwine! Wonke amaphawu aphumile.

# Izihloko zezenzo
senet-check-status = Isimo
senet-check-sticks = Izinti
senet-check-score = Amanqolobane
senet-score = { $p1 }: { $off1 } phandle. { $p2 }: { $off2 } phandle.

# Amaphutha
senet-not-your-piece = Lokhu akusilo uphawu lwakho.
senet-no-piece-there = Akukho phawu lapho.
senet-no-moves-from-here = Akukho zinyathelo ezisemthethweni kusuka kulo sikwele.

# Izinketho
senet-option-bot-difficulty = Ubunzima bebot: { $bot_difficulty }
senet-option-select-bot-difficulty = Khetha ubunzima bebot
senet-option-changed-bot-difficulty = Ubunzima bebot busetelwe ku-{ $bot_difficulty }.
senet-difficulty-random = Ngokungahleliwe
senet-difficulty-simple = Elula
