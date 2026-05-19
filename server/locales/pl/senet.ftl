# Lokalizacja Senetu

game-name-senet = Senet

# Rozpoczęcie gry
senet-game-started = { $p1 } jest graczem 1, { $p2 } jest graczem 2. { $first } zaczyna.

# Rzut patyczkami
senet-throw = { $player } rzuca { $result }.{ $bonus ->
    [yes] {" "}Dodatkowy rzut!
   *[no] {""}
}

# Ruch
senet-move-you = Przesuwasz się z pola { $from } na pole { $to }.
senet-move-other = { $player } przesuwa się z pola { $from } na pole { $to }.
senet-swap-you = Zamieniasz się miejscami z { $opponent } na polu { $to }. { $opponent } wraca na pole { $from }.
senet-swap-other = { $player } zamienia się miejscami z { $opponent } na polu { $to }. { $opponent } wraca na pole { $from }.
senet-bearoff-you = Wyprowadzasz pionek z pola { $from }. Pozostało { $remaining }.
senet-bearoff-other = { $player } wyprowadza pionek z pola { $from }. Pozostało { $remaining }.
senet-water-you = Wylądowałeś w Domu Wody! Pionek wysłany na pole { $dest }.
senet-water-other = { $player } wylądował w Domu Wody! Pionek wysłany na pole { $dest }.
senet-happiness-you = Dotarłeś do Domu Szczęścia.
senet-happiness-other = { $player } dotarł do Domu Szczęścia.

# Brak ruchów
senet-no-moves-you = Nie masz żadnych dozwolonych ruchów.
senet-no-moves-other = { $player } nie ma żadnych dozwolonych ruchów.

# Opisy pól
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, twoje
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, twoje
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Nazwy specjalnych pól
senet-house-rebirth = Odrodzenie
senet-house-happiness = Szczęście
senet-house-water = Woda
senet-house-three-truths = Trzy Prawdy
senet-house-re-atum = Re-Atum

# Stan gry
senet-status = { $p1 }: { $off1 } wyprowadzonych. { $p2 }: { $off2 } wyprowadzonych.{ $phase ->
    [throwing] {" "}Oczekiwanie na rzut.
   *[moving] {" "}Rzut: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Brak rzutu.

# Wygrana
senet-wins = { $player } wygrywa! Wszystkie pionki wyprowadzone.

# Etykiety akcji
senet-check-status = Stan
senet-check-sticks = Patyczki
senet-check-score = Wynik
senet-score = { $p1 }: { $off1 } wyprowadzonych. { $p2 }: { $off2 } wyprowadzonych.

# Błędy
senet-not-your-piece = To nie jest twój pionek.
senet-no-piece-there = Na tym polu nie ma pionka.
senet-no-moves-from-here = Z tego pola nie ma dozwolonych ruchów.

# Opcje
senet-option-bot-difficulty = Poziom trudności bota: { $bot_difficulty }
senet-option-select-bot-difficulty = Wybierz poziom trudności bota
senet-option-changed-bot-difficulty = Poziom trudności bota ustawiony na { $bot_difficulty }.
senet-difficulty-random = Losowy
senet-difficulty-simple = Prosty
