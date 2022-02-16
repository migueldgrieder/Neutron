import field
import humanPlayer
import move
import random
import neutron


#    Estados do jogo
# 1 - Jogo nao iniciado
# 2 - Proximo jogador
# 3 - Jogada iregular
# 4 - Jogo finalizado com vencedor
# 5 - Jogo finalizado empatado


class Board:  # Realiza a gerencia real do tabuleiro "back-end"

    def __init__(self):
        # Define os jogadores
        super().__init__()
        self._neutron = neutron.Neutron()
        self._player1 = humanPlayer.HumanPlayer()
        self._player2 = humanPlayer.HumanPlayer()
        self._player1.initialize("Jogador Próton", 1)
        self._player2.initialize("Jogador Elétron", 2)
        self._matchStatus = -1
        self._statusMessage = None

        # Define as posicoes no "backend"

        self._fields = []  # tabuleiro
        self._neutronPosition = [2, 2]
        self._aMovePiece = None
        self._message = 1
        self._passedFirstMatch = False
        self.initialPieces()

    def getPassedFirstMatch(self):
        # Retorna bool caso ja passou a primeira jogada(onde nao controla neutron)
        return self._passedFirstMatch

    def setFirstMatch(self, boolean):
        # Define bool de primeira jogada
        self._passedFirstMatch = boolean

    def initialPieces(self):
        # Define as posicaos iniciais do tabuleiro
        for y in range(5):
            column = []
            for x in range(5):
                column.append(field.Field(None))
            self._fields.append(column)

        for i in range(5):
            self._fields[i][0] = field.Field(self._player1)
        for i in range(5):
            self._fields[i][4] = field.Field(self._player2)

        self._fields[2][2] = field.Field(self._neutron)

    def getStatus(self):
        # Retorna o estado do jogo
        # -1 - antes de partida iniciar
        # 0 - vez  de selecionar a peca do time
        # 1 - vez de selecionar local vazio para onde mover a peca time
        # 2 - vez de selecionar local vazio para onde mover o  neutron
        return self._matchStatus

    def setStatus(self, value):
        # Define o estado do jogo
        self._matchStatus = value

    def getStatusMessage(self):
        # Retorna a mensagem de estado
        status = self.getStatus()
        jogador = (self.getEnabledPlayer().getName())

        if (status == 0):
            self._statusMessage = (jogador + " - Selecione uma peça sua para mover - status0")
        elif (status == 1):
            self._statusMessage = (jogador + " - Selecione a posição para mover sua peça - status1")
        elif (status == 2):
            self._statusMessage = (jogador + " - Selecione a posição para mover o Neutron - status2")
        else:
            self._statusMessage = status
        return self._statusMessage

    def setMessage(self, message):
        self._message = message

    def getMessage(self):
        # Retorna a mensagem de advertencia
        message = self._message
        jogador = (self.getEnabledPlayer().getName())

        if (message == 1):  # 1+ - status -1 , o
            self._message = ""
        elif (message == 2):
            self._message = ("Local vazio. Jogue novamente")

        elif (message == 10):  # 10+ - status 10
            self._message = ""
        elif (message == 11):
            self._message = ("Local incorreto. Jogue novamente")

        elif (message == 20):  # 20+ - status 20
            self._message = ""

        elif (message == 30):
            self._message = ("A peça clicada é do oponente! Jogue novamente")
        elif (message == 31):
            self._message = ("A peça clicada é o Neutron! Jogue novamente")
        elif (message == 32):
            self._message = ("")

        return self._message

    def getField(self, aMove):
        # Retorna o estado da posicao indicada
        x = aMove.getLine() - 1
        y = aMove.getColumn() - 1
        return self._fields[x][y]

    def getEnabledPlayer(self):
        # Retorna o jogador da rodada
        if self._player1.getTurn():
            return self._player1
        else:
            return self._player2

    def getDisabledPlayer(self):
        # Retorna o jogador da proxima rodada
        if self._player1.getTurn():
            return self._player2
        else:
            return self._player1

    def getValue(self, x, y):
        # Retorna o tipo de peça de um campo
        if (self._fields[x][y].occupied()):
            value = (self._fields[x][y].getOccupant()).getSymbol()
        else:
            value = 0
        return value

    def moveNeutron(self, aMove):
        could_move = self.movePiece(aMove, None)
        return could_move

    def linearCheck(self, x_difference, y_difference, x_start, x_final, y_start, y_final):
        legit_linear = True
        list_0_to_4 = [0, 1, 2, 3, 4]
        if x_difference == 0 and y_difference > 0:
            for i in range(abs(y_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start][y_start + i + 1].occupied():
                    legit_linear = False
                    break

            if legit_linear:
                for j in range(1, 4, 1):  # tenta mover a mais caso for casas vazias
                    try:
                        if  not self._fields[x_final][y_final + 1].occupied():
                            if y_final + 1 in list_0_to_4:
                                y_final = y_final + 1
                    except IndexError:
                        break

        elif x_difference == 0 and y_difference < 0:
            for i in range(abs(y_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start][y_start - i - 1].occupied():
                    legit_linear = False
                    break

            if legit_linear:
                for j in range(1, 4, 1):  # tenta mover a mais caso for casas vazias
                    try:
                        if  not self._fields[x_final][y_final - 1].occupied():
                            if y_final - 1 in list_0_to_4:
                                y_final = y_final - 1
                    except IndexError:
                        break

        elif y_difference == 0 and x_difference > 0:
            for i in range(abs(x_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start + 1 + i][y_start].occupied():
                    legit_linear = False
                    break

            if legit_linear:
                for j in range(1, 4, 1):  # tenta mover a mais caso for casas vazias
                    try:
                        if  not self._fields[x_final + 1][y_final].occupied():
                            if x_final + 1 in list_0_to_4:
                                x_final = x_final + 1
                    except IndexError:
                        break

        elif y_difference == 0 and x_difference < 0:
            for i in range(abs(x_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start - 1 - i][y_start].occupied():
                    legit_linear = False
                    break

            if legit_linear:
                for j in range(1, 4, 1):  # tenta mover a mais caso for casas vazias
                    try:
                        if  not self._fields[x_final - 1][y_final].occupied():
                            if x_final - 1 in list_0_to_4:
                                x_final = x_final - 1
                    except IndexError:
                        break

        return legit_linear, x_final, y_final


    def movePiece(self, aMoveDestiny, player):
        if player:
            x_start = self._aMovePiece.getLine() - 1
            y_start = self._aMovePiece.getColumn() - 1
        else:
            x_start = self._neutronPosition[0]
            y_start = self._neutronPosition[1]

        x_final = aMoveDestiny.getLine() - 1
        y_final = aMoveDestiny.getColumn() - 1

        x_difference = x_final - x_start
        y_difference = y_final - y_start
        if x_difference == 0 or y_difference ==0: #Checa se o movimento linear é valido
            legit_linear, x_final, y_final = self.linearCheck(x_difference, y_difference, x_start, x_final, y_start, y_final)
            self.moveResults(player, legit_linear, x_start, x_final, y_start, y_final)
            return legit_linear

        if abs(x_difference) == abs(y_difference): #Checa se o movimento diagonal é valido
            legit_diagonal, x_final, y_final = self.moveDiagonal( x_difference, y_difference, x_start, x_final,y_start, y_final)
            self.moveResults(player, legit_diagonal, x_start, x_final,y_start, y_final)
            return legit_diagonal

        else:
            return False


    def moveDiagonal(self, x_difference, y_difference, x_start, x_final,y_start, y_final):
        legit_diagonal = True
        list_0_to_4 = [0, 1, 2, 3, 4]
        if x_difference > 0 and y_difference > 0:
            for i in range(abs(x_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start + i + 1][y_start + i + 1].occupied():
                    legit_diagonal = False
                    break

            for j in range(1, 4, 1):
                try:
                    if not self._fields[x_final + 1][y_final + 1].occupied():
                        if x_final + 1 in list_0_to_4 and y_final + 1 in list_0_to_4:
                            x_final = x_final + 1
                            y_final = y_final + 1
                except IndexError:
                    break

        elif x_difference > 0 > y_difference:
            for i in range(abs(x_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start + i + 1][y_start - i - 1].occupied():
                    legit_diagonal = False
                    break

            for j in range(1, 4, 1):
                try:
                    if not self._fields[x_final + 1][y_final - 1].occupied():
                        if x_final + 1 in list_0_to_4 and y_final - 1 in list_0_to_4:
                            x_final = x_final + 1
                            y_final = y_final - 1
                except IndexError:
                    break

        elif x_difference < 0 and y_difference > 0:  # MAIN
            for i in range(abs(x_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start - i - 1][y_start + i + 1].occupied():
                    legit_diagonal = False
                    break

            for j in range(1, 4, 1):
                try:
                    if not self._fields[x_final - 1][y_final + 1].occupied():
                        if x_final - 1 in list_0_to_4 and y_final + 1 in list_0_to_4:
                            x_final = x_final - 1
                            y_final = y_final + 1
                except IndexError:
                    break

        elif x_difference < 0 and y_difference < 0:
            for i in range(abs(x_difference)):  # Checa se o caminho esta livre
                if self._fields[x_start - i - 1][y_start - i - 1].occupied():
                    legit_diagonal = False
                    break

            for j in range(1, 4, 1):
                try:
                    if not self._fields[x_final - 1][y_final - 1].occupied():
                        if x_final - 1 in list_0_to_4 and y_final - 1 in list_0_to_4:
                            x_final = x_final - 1
                            y_final = y_final - 1
                except IndexError:
                    break

        return legit_diagonal, x_final, y_final

    def moveResults(self, player, legit_move, x_start, x_final, y_start, y_final):
        if legit_move:
            self._fields[x_start][y_start].empty()
            if player:
                    self._aMovePiece = None
                    self._fields[x_final][y_final].setOccupant(player)
            else: # move o neutron
                    self._fields[x_final][y_final].setOccupant(self._neutron)
                    self._neutronPosition = [x_final, y_final]

    def proceedMove(self, aMove):
        # Realiza a jogada, e testa qual condica
        selectedField = self.getField(aMove)
        enabledPlayer = self.getEnabledPlayer()
        disabledPlayer = self.getDisabledPlayer()
        status = self.getStatus()
        if status == -1:
            self.setStatus(0)
            self.setMessage(1)

        else:
            if not selectedField.occupied():  # CLIQUE EM LOCAL VAZIO
                if status == 0:  # x + na  vez selecionar peça time
                    self.setMessage(2)

                elif status == 2:  # move o neutron
                    couldMove = self.moveNeutron(aMove)
                    if couldMove:
                        enabledPlayer.disable()
                        newMove = disabledPlayer.enable()
                        self.setStatus(0)
                        self.setMessage(1)
                        if newMove.getLine() != 0:
                            self.proceedMove(newMove)
                    else:
                        self.setMessage(11)


                elif status == 1:  # Move a peca do time
                    if self.getPassedFirstMatch():
                        couldMove = self.movePiece(aMove, enabledPlayer)
                        if couldMove:
                            self.setStatus(2)
                            self.setMessage(20)
                    else:  # Primeira rodada - não tem status 2 (neutron)
                        couldMove = self.movePiece(aMove, enabledPlayer)
                        if couldMove:
                            self.setFirstMatch(True)
                            enabledPlayer.disable()
                            newMove = disabledPlayer.enable()
                            self.setStatus(0)
                            self.setMessage(1)
                            if (newMove.getLine() != 0):
                                self.proceedMove(newMove)


            elif selectedField.getOccupant() == enabledPlayer:  # Clicou na peça do mesmo time

                if status == 0:  # X + selecionou peça certa
                    self.setMessage(10)
                    self.setStatus(1)
                    self._aMovePiece = aMove

                else:  # X + devia ser para onde VAZIO
                    self.setMessage(11)

            elif selectedField.getOccupant() == self._neutron:  # Clicou no Neutron
                self.setMessage(31)
            else:  # Sobra apenas clicar no oponente
                self.setMessage(30)

    def startMatch(self):
        # Comeca uma nova partida
        self.reset()
        self.setFirstMatch(False)
        if random.randint(1, 2) == 1:
            aMove = self._player1.enable()
            self.proceedMove(aMove)
        else:
            aMove = self._player2.enable()
            self.proceedMove(aMove)

    def click(self, line, column):
        # Realiza os processos ao jogador clicar em uma posicao
        if self.getStatus() == -1:
            self.startMatch()
        else:
            aMove = move.Move(line, column)
            self.proceedMove(aMove)

    def reset(self):
        # Reinicia o tabuleiro com todas posicoes vazias
        for x in range(5):
            for y in range(5):
                self._fields[x][y].empty()
        self._player1.reset()
        self._player2.reset()
        self.initialPieces()

