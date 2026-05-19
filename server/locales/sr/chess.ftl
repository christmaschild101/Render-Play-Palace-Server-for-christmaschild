# Chess

game-name-chess = Šah

# Options
chess-set-turn-timer = Vreme za potez: { $mode }
chess-select-turn-timer = Izaberite vreme za potez
chess-option-changed-turn-timer = Vreme za potez podešeno na { $mode }.

chess-toggle-auto-draw = Automatski remi nakon ponavljanja ili 50 poteza: { $enabled }
chess-option-changed-auto-draw = Automatski remi { $enabled }.

chess-toggle-show-coordinates = Prikaži koordinate u potezima: { $enabled }
chess-option-changed-show-coordinates = Prikazivanje koordinata { $enabled }.

# Game start
chess-game-started = { $white } je beli, { $black } je crni. Beli igra prvi.

# Turn / move messages
chess-you-select = Izabrano { $piece } na { $square }. Kliknite na odredište.
chess-no-piece = Nema figure koja se ovde može izabrati.
chess-move-cancelled = Potez otkazan.
chess-illegal-move = Neispravan potez.

chess-you-move = Pomerate figuru { $piece } sa { $from } na { $to }.
chess-player-moves = { $player } pomera figuru { $piece } sa { $from } na { $to }.
chess-you-capture = Uzimate figuru { $captured } na { $to } figurom { $piece } sa { $from }.
chess-player-captures = { $player } uzima figuru { $captured } na { $to } figurom { $piece } sa { $from }.

chess-you-en-passant = Uzimate en passant na { $to } pešakom sa { $from }.
chess-player-en-passant = { $player } uzima en passant na { $to } pešakom sa { $from }.

chess-you-castle-kingside = Pravite malu rokadu.
chess-player-castles-kingside = { $player } pravi malu rokadu.
chess-you-castle-queenside = Pravite veliku rokadu.
chess-player-castles-queenside = { $player } pravi veliku rokadu.

chess-you-promote = Promovišete pešaka u figuru { $piece } na { $square }.
chess-player-promotes = { $player } promoviše pešaka u figuru { $piece } na { $square }.

# Check / checkmate / draw
chess-check = Šah!
chess-checkmate = Mat! { $winner } pobeđuje.
chess-you-win-checkmate = Mat! Pobeđujete.
chess-stalemate = Pat. Igra je nerešena.
chess-draw-fifty = Remi nakon pedeset poteza.
chess-draw-repetition = Remi nakon tri ponavljanja.
chess-draw-material = Remi nakon nedovoljno mogućnosti za pobedu.
chess-draw-agreement = Remi nakon zajedničkog slaganja.

# Resign
# Resign
chess-resign = Predaj
chess-resign-confirm = Da li ste sigurni da želite da se predate?
chess-resign-yes = Da, predaj
chess-resign-no = Ne, nastavi igru
chess-you-resign = Predajete. { $opponent } pobeđuje.
chess-player-resigns = { $player } predaje. { $opponent } pobeđuje.

# Draw offer
chess-offer-draw = Predloži remi
chess-you-offer-draw = Predlažete remi.
chess-player-offers-draw = { $player } predlaže remi.
chess-you-accept-draw = Prihvatate remi.
chess-player-accepts-draw = { $player } prihvata remi.
chess-you-decline-draw = Odbijate remi.
chess-player-declines-draw = { $player } odbija remi.
chess-no-draw-offer = Nema predloga za remi na koji možete da odgovorite.
chess-already-offered = Već ste predložili remi.

# Undo
chess-undo-request = Poništi poslednji potez
chess-you-request-undo = Zahtevate poništavanje poslednjeg poteza.
chess-player-requests-undo = { $player } zahteva poništavanje poslednjeg poteza.
chess-you-accept-undo = Prihvatate poništavanje.
chess-player-accepts-undo = { $player } prihvata poništavanje. Potez poništen.
chess-you-decline-undo = Odbijate poništavanje.
chess-player-declines-undo = { $player } odbija zahtev za poništavanje.
chess-no-undo-request = Nema zahteva za poništavanje na koji možete da odgovorite.
chess-no-moves-to-undo = Nema poteza koji mogu da se ponište.
chess-already-requested-undo = Već ste zahtevali poništavanje.
chess-undo-applied = Poslednji potez poništen.  { $player } je na potezu.

# Promotion
chess-select-promotion = Izaberite figuru za promociju

# View board
chess-view-board = Prikaži tablu
chess-flip-board = Okreni tablu
chess-viewer-own = vašoj
chess-viewer-opponent = protivničkoj
chess-board-flipped = Tabla okrenuta u { $viewer }  perspektivi ({ $color }).

chess-board-rank = Rang { $rank }: { $pieces }
chess-empty = Prazno
chess-board-header = Stanje table:

# Status / scores
chess-status-white = Beli: { $player }
chess-status-black = Crni: { $player }
chess-status-turn = Potez: { $color }
chess-status-move-count = Potezi: { $count }
chess-check-status = Proveri status igre

# Type move
chess-type-move = Upiši potez
chess-enter-move = Upišite potez (na primer e2-e4, o-o, o-o-o)
chess-move-parse-error = Nemoguće obraditi ovaj potez. Pokušajte e2-e4, pe2-e4, o-o, ili o-o-o.

# FEN
chess-import-fen = Uvezi FEN
chess-enter-fen = Nalepite FEN niz
chess-fen-loaded = FEN uspešno učitan.
chess-fen-error = Greška pri učitavanju FEN-a.

# Piece names
chess-piece-pawn = Pešak
chess-piece-knight = Konj
chess-piece-bishop = Lovac
chess-piece-rook = Top
chess-piece-queen = Kraljica
chess-piece-king = Kralj

# Piece grammatical gender (m = masculine, f = feminine)
# Translators: change these to match the grammatical gender in your language.
chess-piece-pawn-gender = m
chess-piece-knight-gender = m
chess-piece-bishop-gender = m
chess-piece-rook-gender = m
chess-piece-queen-gender = f
chess-piece-king-gender = m

# Timer
chess-check-turn-timer = Vreme za potez
chess-turn-timeout = Vreme je isteklo!

# Timer choice labels (game-specific durations)
chess-timer-120 = 2 minuta
chess-timer-180 = 3 minuta
chess-timer-300 = 5 minuta
