import copy
from nustatymai import *
import sys
import pygame
import numpy as np
import random

pygame.init()
screen = pygame.display.set_mode((plotis, aukstis))
pygame.display.set_caption('Kryžiukai Nuliukai')
screen.fill(lango_spalva)


class Laukas:

    def __init__(self):
        self.squares = np.zeros((eilutes, stulpeliai))
        self.empty_sqrs = self.squares  # [squares]
        self.marked_sqrs = 0

    def final_statusas(self, show=False):
        """
        @return 0 jei niekas nelaimejo
        @return 1 jei laimejo 1
        @return 2 jei laimejo 2
        :return:
        """

        # stulpeliu laimejimai
        for col in range(stulpeliai):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = nuliuko_spalva if self.squares[0][col] == 2 else kryziuko_spalva
                    iPos = (col * langelio_dydis + langelio_dydis // 2, 20)
                    fPos = (col * langelio_dydis + langelio_dydis // 2, aukstis - 20)
                    pygame.draw.line(screen, color, iPos, fPos, linijos_plotis)
                return self.squares[0][col]

        # eiluciu laimejimai
        for row in range(eilutes):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = nuliuko_spalva if self.squares[row][0] == 2 else kryziuko_spalva
                    iPos = (20, row * langelio_dydis + langelio_dydis // 2)
                    fPos = (plotis - 20, row * langelio_dydis + langelio_dydis // 2)
                    pygame.draw.line(screen, color, iPos, fPos, linijos_plotis)
                return self.squares[row][0]

        # istrizai laimejimai

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = nuliuko_spalva if self.squares[1][1] == 2 else kryziuko_spalva
                iPos = (20, 20)
                fPos = (plotis - 20, aukstis - 20)
                pygame.draw.line(screen, color, iPos, fPos, kryziuko_plotis)
            return self.squares[1][1]

        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = nuliuko_spalva if self.squares[1][1] == 2 else kryziuko_spalva
                iPos = (20, aukstis - 20)
                fPos = (plotis - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, kryziuko_plotis)
            return self.squares[1][1]

        # niekas nelaimi
        return 0

    def pazymeti_langeli(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def tuscias_langelis(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(eilutes):
            for col in range(stulpeliai):
                if self.tuscias_langelis(row, col):
                    empty_sqrs.append((row, col))

        return empty_sqrs

    def pilnas_laukas(self):
        return self.marked_sqrs == 9

    def tuscias_laukas(self):
        return self.marked_sqrs == 0


class AI:

    def __init__(self, lygis=1, zaidejas=2):
        self.level = lygis
        self.player = zaidejas

    def rnd(self, laukas):
        tusti_lang = laukas.get_empty_sqrs()
        idx = random.randrange(0, len(tusti_lang))

        return tusti_lang[idx]  # grazina eilute ir stulpeli

    def minimax(self, laukas, max):

        statusas = laukas.final_statusas()

        # 1 zaidejas laimi
        if statusas == 1:
            return 1, None  # eval, move

        # 2 zaidejas laimi
        if statusas == 2:
            return -1, None

        # nebera vietos
        elif laukas.pilnas_laukas():
            return 0, None

        if max:
            max_ejimas = -100
            geriausas_ejimas = None
            tusti_langeliai = laukas.get_empty_sqrs()

            for (eilute, stulpelis) in tusti_langeliai:
                laikinas_laukas = copy.deepcopy(laukas)
                laikinas_laukas.pazymeti_langeli(eilute, stulpelis, 1)
                eval = self.minimax(laikinas_laukas, False)[0]
                if eval > max_ejimas:
                    max_ejimas = eval
                    geriausas_ejimas = (eilute, stulpelis)

            return max_ejimas, geriausas_ejimas

        elif not max:
            min_ejimas = 100
            geriausas_ejimas = None
            tusti_langeliai = laukas.get_empty_sqrs()

            for (eilute, stulpelis) in tusti_langeliai:
                laikinas_laukas = copy.deepcopy(laukas)
                laikinas_laukas.pazymeti_langeli(eilute, stulpelis, self.player)
                eval = self.minimax(laikinas_laukas, True)[0]
                if eval < min_ejimas:
                    min_ejimas = eval
                    geriausas_ejimas = (eilute, stulpelis)

            return min_ejimas, geriausas_ejimas

    def ai_ejimas(self, pagr_laukas):
        if self.level == 0:
            # atsitiktinis pasirinkimas
            ejimas = 'random'
            pasirinkimas = self.rnd(pagr_laukas)
        else:
            # algoritmo pasirinkimas
            ejimas, pasirinkimas = self.minimax(pagr_laukas, False)

        print(f'AI pasirinko langelio pozicija: {pasirinkimas} su laimejimo tikimybe: {ejimas}')

        return pasirinkimas  # grazina eilute , stulpeli


class Zaidimas:

    def __init__(self):
        self.laukas = Laukas()
        self.ai = AI()
        self.zaidejas = 1  # 1 - kryziukas  #2 - nuliukas
        self.rezimas = 'ai'  # pvp arba ai
        self.testi = True
        self.rodyti_eilutes()



    def rodyti_eilutes(self):
        #lango spalva
        screen.fill(lango_spalva)

        #vertikaliai
        pygame.draw.line(screen, liniju_splava, (langelio_dydis, 0), (langelio_dydis, aukstis), linijos_plotis)
        pygame.draw.line(screen, liniju_splava, (plotis - langelio_dydis, 0), (plotis - langelio_dydis, aukstis),
                         linijos_plotis)

        # horizontaliai
        pygame.draw.line(screen, liniju_splava, (0, langelio_dydis), (plotis, langelio_dydis), linijos_plotis)
        pygame.draw.line(screen, liniju_splava, (0, aukstis - langelio_dydis), (plotis, aukstis - langelio_dydis),
                         linijos_plotis)

    def pazymeti_langeli(self, eil, stulp):
        if self.zaidejas == 1:

            # nupiesia kryziuka
            start_desc = (stulp * langelio_dydis + pastumimas, eil * langelio_dydis + pastumimas)
            end_desc = (
            stulp * langelio_dydis + langelio_dydis - pastumimas, eil * langelio_dydis + langelio_dydis - pastumimas)
            pygame.draw.line(screen, kryziuko_spalva, start_desc, end_desc, kryziuko_plotis)

            start_asc = (stulp * langelio_dydis + pastumimas, eil * langelio_dydis + langelio_dydis - pastumimas)
            end_asc = (stulp * langelio_dydis + langelio_dydis - pastumimas, eil * langelio_dydis + pastumimas)
            pygame.draw.line(screen, kryziuko_spalva, start_asc, end_asc, kryziuko_plotis)

        elif self.zaidejas == 2:
            # nupiesia nuliuka
            centras = (stulp * langelio_dydis + langelio_dydis // 2, eil * langelio_dydis + langelio_dydis // 2)
            pygame.draw.circle(screen, nuliuko_spalva, centras, spindulys, nuliuko_plotis)

    def ejimas(self, eil, stulp):
        self.laukas.pazymeti_langeli(eil, stulp, self.zaidejas)
        self.pazymeti_langeli(eil, stulp)
        self.kitas_ejimas()

    def kitas_ejimas(self):
        self.zaidejas = self.zaidejas % 2 + 1

    def change_gamemode(self):
        self.rezimas = 'ai' if self.rezimas == 'pvp' else 'pvp'

    def pabaiga(self):
        return self.laukas.final_statusas(show=True) != 0 or self.laukas.pilnas_laukas()

    def reset(self):
        self.__init__()


# funkcija paleidzianti langa
def main():
    zaidimas = Zaidimas()
    board = zaidimas.laukas
    ai = zaidimas.ai

    while True:

        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # mygtuko paspaudimas
            if event.type == pygame.KEYDOWN:

                # G - pakeicia rezima
                if event.key == pygame.K_g:
                    zaidimas.change_gamemode()

                # R - isvalo zaidimo lauka
                if event.key == pygame.K_r:
                    zaidimas.reset()
                    board = zaidimas.laukas
                    ai = zaidimas.ai

                # Z - atsitiktinis AI
                if event.key == pygame.K_z:
                    ai.level = 0

                # X - protingas AI
                if event.key == pygame.K_x:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                eil = pos[1] // langelio_dydis
                stulp = pos[0] // langelio_dydis

                if board.tuscias_langelis(eil, stulp) and zaidimas.testi:
                    zaidimas.ejimas(eil, stulp)

                    if zaidimas.pabaiga():
                        zaidimas.testi = False

        # iskviecia ai
        if zaidimas.rezimas == 'ai' and zaidimas.zaidejas == ai.player and zaidimas.testi:

            pygame.display.update()

            eil, stulp = ai.ai_ejimas(board)
            zaidimas.ejimas(eil, stulp)

            if zaidimas.pabaiga():
                zaidimas.testi = False

        pygame.display.update()


main()
