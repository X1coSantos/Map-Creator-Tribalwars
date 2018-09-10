from PIL import Image, ImageDraw
from urllib.request import urlopen, unquote
from pprint import pprint
from time import time

class MapaMundiTribos():
    """ Classe que trata mapa do tribos """

    def __init__(self):
        """ Função inicializadora """

        # Configs do mapa
        self.NCONTINENTES = 10
        self.TAMANHOCONTINENTES = 100
        self.ALTURA = self.NCONTINENTES * self.TAMANHOCONTINENTES
        self.LARGURA = self.NCONTINENTES * self.TAMANHOCONTINENTES

        # Configs das aldeias
        self.mostrarBarbaras = True
        self.mostrarTodasAldeias = False
        self.marcadoresMaiores = False
        self.tamanhoMarcadores = 2

        # Dados do mapa
        self.aldeias    = {}
        self.jogadores  = {}
        self.conquistas = {}

        # Marcadores do mapa
        self.marcasTribos    = {}
        self.marcasJogadores = {}

        # Cores
        self.cor = {}
        self.cor['branco']   = (255, 255, 255)
        self.cor['preto']    = (0, 0, 0)
        self.cor['vermelho'] = (255, 0, 0)
        self.cor['azul']     = (0, 0, 255)
        self.cor['cinzenta'] = (190, 190, 190)
        self.cor['verde']    = (0, 255, 0)
        self.cor['amarelo']  = (255, 255, 0)
        self.cor['castanho']  = (210,105,30)

        # Inicia imagem
        self.img = Image.new('RGB', (self.ALTURA, self.LARGURA), self.cor['preto'])

        # Desenhar na imagem
        self.imgDraw = ImageDraw.Draw(self.img)

        # Logs
        self.log = True

    def guardarImagem(self, nome="imagem"):
        """ Guarda a imagem """
        self.doLog("A GUARDAR IMAGEM ... ")
        self.img.save(nome+".png", "PNG")
        self.doLog("IMAGEM GUARDADA")

    def linha(self, x, y, dx, dy):
        """ Desenha uma linha, a começar em (x, y) e a acabar em (dx, dy) """
        self.imgDraw.line([(x,y), (dx, dy)], fill=self.cor['branco'], width=1)

    def desenhaLinhasContinenteHorizontais(self):
        """ Desenha linhas horizontais dos continentes """

        self.doLog("A CRIAR LINHAS HORIZONTAIS...")

        # Define o y inicial
        y = 0

        # Desenha o numero de linhas necessárias conforme o numero de continentes
        for linha in range(self.NCONTINENTES + 1):
            # Desenha a linha
            self.linha(0, y, self.LARGURA, y)
            # Avança o numero de pixels necessários
            y += self.TAMANHOCONTINENTES

        self.doLog("LINHAS HORIZONTAIS CRIADAS")


    def desenhaLinhasContinenteVerticais(self):
        """ Desenha linhas verticais dos continentes """

        self.doLog("A CRIAR LINHAS VERTICAIS...")

        # Define o x inicial
        x = 0

        # Desenha o numero de linhas necessárias conforme o numero de continentes
        for linha in range(self.NCONTINENTES + 1):
            # Desenha a linha
            self.linha(x, 0, x, self.LARGURA)
            # Avança o numero de pixels necessários
            x += self.TAMANHOCONTINENTES

        self.doLog("LINHAS VERTICAIS CRIADAS")

    def escreveTexto(self, x, y, txt):
        """ Escreve texto em (x, y) """
        self.imgDraw.text((x + 78,y + 87), txt, fill=(self.cor['branco']))

    def escreveContinentes(self):
        """ Escreve o nome dos continentes """

        self.doLog("A ESCREVER NOMES DOS CONTINENTES...")

        # Inicializa o x e o y
        x, y = 0, 0

        for linhaVertical in range(self.NCONTINENTES):
            for linhaHorizontal in range(self.NCONTINENTES):
                kx = str(x)[-3] if x >= 100 else '0'
                ky = str(y)[-3] if y >= 100 else '0'
                continente = "K" + ky + kx
                self.escreveTexto(x, y, continente)
                x += self.TAMANHOCONTINENTES
            x = 0
            y += self.TAMANHOCONTINENTES

        self.doLog("NOMES DOS CONTINENTES ESCRITOS")

    def desenhaAldeia(self, x, y, cor='vermelho'):
        """ Desenha uma aldeia """
        x = int(x)
        y = int(y)
        coord = (x, y)
        self.imgDraw.point(coord, fill=self.cor[cor])

    def importarFiles(self):
        """ Importa uma file txt """

        self.doLog("A IMPORTAR ALDEIAS...")

        # faz a requisição dos dados das aldeias e decoda
        data_villages = urlopen(f"https://pt60.tribalwars.com.pt/map/village.txt").read().decode()

        # Passa por cada aldeia e guarda os dados dentro do dicionario principal
        for row in data_villages.splitlines():
            aldeia = row.split(',')
            self.aldeias[aldeia[0]] = [aldeia[0], aldeia[1], aldeia[2],
                                       aldeia[3], aldeia[4], aldeia[5], aldeia[6]]

        self.doLog("ALDEIAS CARREGADAS")

        self.doLog("A IMPORTAR JOGADORES...")

        # faz a requisição dos dados dos players e decoda
        data_jogadores = urlopen(f"https://pt60.tribalwars.com.pt/map/player.txt").read().decode()

        # Passa por cada jogador e guarda os dados dentro do dicionario principal
        for row in data_jogadores.splitlines():
            jogador = row.split(',')
            self.jogadores[int(jogador[0])] = [jogador[0], jogador[1], jogador[2],
                                       jogador[3], jogador[4], jogador[5]]
        self.doLog("JOGADORES CARREGADOS")

        self.doLog("A IMPORTAR ULTIMAS CONQUISTAS...")

        # faz a requisição dos dados dos players e decoda
        tempo = int(time()) - (3600 * 23)
        data_conquistas = urlopen(f"https://pt60.tribalwars.com.pt/interface.php?func=get_conquer&since={tempo}")\
                         .read().decode()

        # Passa por cada jogador e guarda os dados dentro do dicionario principal
        for row in data_conquistas.splitlines():
            conquista = row.split(' ')[0].split(',')
            self.conquistas[int(conquista[0])] = [int(conquista[0]), conquista[1], conquista[2],
                                                  conquista[3]]
        self.doLog("ULTIMAS CONQUISTAS CARREGADAS")

    def desenhaAldeias(self):
        """ Desenha as aldeias guardadas na classe """

        self.doLog("A DESENHAR ALDEIAS...")

        # Loop pelas aldeias
        for aldeia in self.aldeias:
            x = int(self.aldeias[aldeia][2])
            y = int(self.aldeias[aldeia][3])

            # Printa conforme a cor

            # ID do player da aldeia atual
            idPlayer = int(self.aldeias[aldeia][4])

            # ID da tribo da aldeia atual
            if idPlayer != 0:
                idTribo = int(self.jogadores[idPlayer][2])
            else:
                idTribo = 0

            # Printa todas as aldeias, se forem barabas de uma cor, se nao de outra, caso self.mostrarTodasAldeias for
            # verdadeiro
            if self.mostrarTodasAldeias:
                if idPlayer == 0 and self.mostrarBarbaras:
                    if self.marcadoresMaiores:
                        self.marcadorAldeia(x, y, cor="cinzenta")
                    else:
                        self.desenhaAldeia(x, y, cor="cinzenta")
                elif idPlayer != 0:
                    self.desenhaAldeia(x, y)


            # Para cada cor, printa as tribos
            if idTribo != 0:
                for key in self.marcasTribos:
                    if idTribo in self.marcasTribos[key]:
                        if self.marcadoresMaiores:
                            self.marcadorAldeia(x, y, cor=key)
                        else:
                            self.desenhaAldeia(x, y, cor=key)

            # Para cada cor, printa os jogadores
            for key in self.marcasJogadores:
                if idPlayer in self.marcasJogadores[key]:
                    if self.marcadoresMaiores:
                        self.marcadorAldeia(x, y, cor=key)
                    else:
                        self.desenhaAldeia(x, y, cor=key)

        self.doLog("ALDEIAS DESENHADAS")

    def marcarTribo(self, idTribos, cor):
        """ Adiciona uma tribo para ser marcada """

        self.doLog("A MARCAR TRIBOS")

        # Para cada jogador a ser marcado
        for id in idTribos:
            # Se já existir a cor do jogador, apenas adiciona, senao, cria primeiro a cor e adiciona o jogador
            if cor in self.marcasTribos:
                self.marcasTribos[cor].append(id)
            else:
                self.marcasTribos[cor] = []
                self.marcasTribos[cor].append(id)

        self.doLog("JOGADORES MARCADOS")

    def marcarJogador(self, idJogadores, cor):
        """ Adiciona um jogador aos marcadores """

        self.doLog("A MARCAR JOGADORES")

        # Para cada jogador a ser marcado
        for id in idJogadores:
            # Se já existir a cor do jogador, apenas adiciona, senao, cria primeiro a cor e adiciona o jogador
            if cor in self.marcasJogadores:
                self.marcasJogadores[cor].append(id)
            else:
                self.marcasJogadores[cor] = []
                self.marcasJogadores[cor].append(id)

        self.doLog("JOGADORES MARCADOS")

    def marcadorAldeia(self, x, y, cor="vermelho"):
        """ Cria um marcador para uma aldeia x, y"""
        x1 = x - self.tamanhoMarcadores
        y1 = y + self.tamanhoMarcadores
        x2 = x + self.tamanhoMarcadores
        y2 = y - self.tamanhoMarcadores
        fator = 0.55
        rgb_borda = (int(self.cor[cor][0] * fator),int(self.cor[cor][1] * fator),int(self.cor[cor][2] * fator))
        self.imgDraw.rectangle([(x1, y1), (x2, y2)], outline=rgb_borda, fill=self.cor[cor])

    def ultimasConquistas(self):
        """ Retorna os ids das aldeias das ultimas conquistas do mundo """

        # Ultima aldeias conquistadas
        ultimasAldeiasConquistadas = []
        for aldeia in self.conquistas:
            ultimasAldeiasConquistadas.append(aldeia)
        return ultimasAldeiasConquistadas

    def marcarUltimasAldeiasConquistadas(self):
        """ Marca as ultimas conquistas """

        # Ultimas conquistas
        ultimasAldeiasConquistadas = self.ultimasConquistas()

        # Loop pelas aldeias das ultimasConquistas
        for idAldeia in ultimasAldeiasConquistadas:
            idAldeia = str(idAldeia)
            x = int(self.aldeias[idAldeia][2])
            y = int(self.aldeias[idAldeia][3])

            # Id do player
            idPlayer = int(self.aldeias[idAldeia][4])

            # ID da tribo da aldeia atual
            if idPlayer != 0:
                idTribo = int(self.jogadores[idPlayer][2])
            else:
                idTribo = 0

            # Caso todas as aldeias estejam a ser mostradas
            if self.mostrarTodasAldeias:
                if int(idAldeia) in ultimasAldeiasConquistadas:
                    self.marcadorAldeia(x, y, cor="cinzenta")

            # Para cada cor, printa as tribos
            if idTribo != 0:
                for key in self.marcasTribos:
                    if idTribo in self.marcasTribos[key]:
                        if int(idAldeia) in ultimasAldeiasConquistadas:
                            self.marcadorAldeia(x, y, cor=key)

            # Para cada cor, printa os jogadores
            for key in self.marcasJogadores:
                if idPlayer in self.marcasJogadores[key]:
                    if int(idAldeia) in ultimasAldeiasConquistadas:
                        self.marcadorAldeia(x, y, cor=key)

    def doLog(self, txt):
        """ cria um log com uma ação e mostra caso esteja ativo! """
        if self.log:
            print(f"[LOG]: {txt}")

    def desenhaMapa(self):
        """ Desenha as linhas continentais vertivais e horizontais """
        # Base do mapa
        self.desenhaLinhasContinenteHorizontais()
        self.desenhaLinhasContinenteVerticais()
        self.escreveContinentes()
        # Importa as coisas
        self.importarFiles()
        # Adiciona jogador
        # self.marcarJogador([2749502,778057], cor="azul")
        # Adiciona Tribos
        self.marcarTribo([58, 2722], cor="branco")
        self.marcarTribo([534, 659], cor="castanho")
        self.marcarTribo([773], cor="verde")
        self.marcarTribo([176], cor="amarelo")
        self.marcarTribo([1047], cor="azul")
        # Desenha as aldeias
        self.desenhaAldeias()
        # Desenha ultimas conquistas
        self.marcarUltimasAldeiasConquistadas()
        # Guarda imagem
        self.guardarImagem("mapaTeste")


# Inicia instancia
mapa1 = MapaMundiTribos()
# Manda desenhar
mapa1.desenhaMapa()
