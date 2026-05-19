# Localização do Senet

game-name-senet = Senet

# Início do jogo
senet-game-started = { $p1 } é o jogador 1, { $p2 } é o jogador 2. { $first } começa.

# Lançamento dos paus
senet-throw = { $player } lança { $result }.{ $bonus ->
    [yes] {" "}Turno extra!
   *[no] {""}
}

# Movimento
senet-move-you = Você move da casa { $from } para a casa { $to }.
senet-move-other = { $player } move da casa { $from } para a casa { $to }.
senet-swap-you = Você troca com { $opponent } na casa { $to }. { $opponent } volta para a casa { $from }.
senet-swap-other = { $player } troca com { $opponent } na casa { $to }. { $opponent } volta para a casa { $from }.
senet-bearoff-you = Você sai do tabuleiro a partir da casa { $from }. Restam { $remaining }.
senet-bearoff-other = { $player } sai do tabuleiro a partir da casa { $from }. Restam { $remaining }.
senet-water-you = Você caiu na Casa da Água! Peça enviada para a casa { $dest }.
senet-water-other = { $player } caiu na Casa da Água! Peça enviada para a casa { $dest }.
senet-happiness-you = Você chegou à Casa da Felicidade.
senet-happiness-other = { $player } chegou à Casa da Felicidade.

# Sem movimentos
senet-no-moves-you = Você não tem movimentos legais.
senet-no-moves-other = { $player } não tem movimentos legais.

# Rótulos das casas
senet-sq-empty = { $sq }
senet-sq-own = { $sq }, sua
senet-sq-opponent = { $sq }, { $owner }
senet-sq-empty-special = { $sq }, { $name }
senet-sq-own-special = { $sq }, { $name }, sua
senet-sq-opponent-special = { $sq }, { $name }, { $owner }

# Nomes das casas especiais
senet-house-rebirth = Renascimento
senet-house-happiness = Felicidade
senet-house-water = Água
senet-house-three-truths = Três Verdades
senet-house-re-atum = Re-Atum

# Status
senet-status = { $p1 }: { $off1 } fora. { $p2 }: { $off2 } fora.{ $phase ->
    [throwing] {" "}Aguardando lançamento.
   *[moving] {" "}Resultado: { $roll }.
}
senet-sticks = { $result }
senet-sticks-none = Nenhum lançamento ainda.

# Vitória
senet-wins = { $player } venceu! Todas as peças saíram do tabuleiro.

# Rótulos de ações
senet-check-status = Status
senet-check-sticks = Paus
senet-check-score = Pontuação
senet-score = { $p1 }: { $off1 } fora. { $p2 }: { $off2 } fora.

# Erros
senet-not-your-piece = Essa não é a sua peça.
senet-no-piece-there = Não há nenhuma peça aí.
senet-no-moves-from-here = Não há movimentos legais a partir desta casa.

# Opções
senet-option-bot-difficulty = Dificuldade do bot: { $bot_difficulty }
senet-option-select-bot-difficulty = Selecionar dificuldade do bot
senet-option-changed-bot-difficulty = Dificuldade do bot definida como { $bot_difficulty }.
senet-difficulty-random = Aleatório
senet-difficulty-simple = Simples
