# Localización de Senet

game-name-senet = Senet

# Inicio de partida
senet-game-started = { $p1 } es el jugador 1, { $p2 } es el jugador 2. { $first } comienza.

# Lanzamiento de palos
senet-throw = { $player } lanza { $result }.{ $bonus ->
    [yes] {" "}¡Turno extra!
   *[no] {""}
}

# Movimiento
senet-move-you = Mueves de la casilla { $from } a la casilla { $to }.
senet-move-other = { $player } mueve de la casilla { $from } a la casilla { $to }.
senet-swap-you = Intercambias con { $opponent } en la casilla { $to }. { $opponent } retrocede a la casilla { $from }.
senet-swap-other = { $player } intercambia con { $opponent } en la casilla { $to }. { $opponent } retrocede a la casilla { $from }.
senet-bearoff-you = Sales del tablero desde la casilla { $from }. Quedan { $remaining }.
senet-bearoff-other = { $player } sale del tablero desde la casilla { $from }. Quedan { $remaining }.
senet-water-you = ¡Has caído en la Casa del Agua! Pieza enviada a la casilla { $dest }.
senet-water-other = ¡{ $player } ha caído en la Casa del Agua! Pieza enviada a la casilla { $dest }.
senet-happiness-you = Has llegado a la Casa de la Felicidad.
senet-happiness-other = { $player } ha llegado a la Casa de la Felicidad.

# Sin movimientos
senet-no-moves-you = No tienes movimientos legales.
senet-no-moves-other = { $player } no tiene movimientos legales.

# Etiquetas de casillas
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, tuya
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, tuya
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Nombres de casillas especiales
senet-house-rebirth = Renacimiento
senet-house-happiness = Felicidad
senet-house-water = Agua
senet-house-three-truths = Tres Verdades
senet-house-re-atum = Re-Atum

# Estado
senet-status = { $p1 }: { $off1 } fuera. { $p2 }: { $off2 } fuera.{ $phase ->
    [throwing] {" "}Esperando lanzamiento.
   *[moving] {" "}Tirada: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Aún no se ha lanzado.

# Victoria
senet-wins = ¡{ $player } gana! Todas las piezas han salido del tablero.

# Etiquetas de acciones
senet-check-status = Estado
senet-check-sticks = Palos
senet-check-score = Puntuación
senet-score = { $p1 }: { $off1 } fuera. { $p2 }: { $off2 } fuera.

# Errores
senet-not-your-piece = Esa no es tu pieza.
senet-no-piece-there = No hay ninguna pieza ahí.
senet-no-moves-from-here = No hay movimientos legales desde esta casilla.

# Opciones
senet-option-bot-difficulty = Dificultad del bot: { $bot_difficulty }
senet-option-select-bot-difficulty = Seleccionar dificultad del bot
senet-option-changed-bot-difficulty = Dificultad del bot establecida en { $bot_difficulty }.
senet-difficulty-random = Aleatorio
senet-difficulty-simple = Simple
