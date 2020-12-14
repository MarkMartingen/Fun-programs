'''
Simuation of how bacteria may develop on a 2 dimensional grid.
Each point that has exactly two adjacent bacteria will develop a bacteria in the next time step.
Other points, will be bacteria free in the following time step

PRESS SPACE BAR to move onto the next time step.
'''

import numpy as np
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, KEYDOWN, K_ESCAPE, RLEACCEL, K_SPACE

############################ ZMIENNE GLOBALNE ##############################3
plik = 'mapa3.txt'
n = 4
m = 5
RECT_SIZE = 50
SCREEN_WIDTH = RECT_SIZE * m
SCREEN_HEIGHT = RECT_SIZE * n
SPEED = 1
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])


class Mapa:
	def __init__(self, tablica):
		self.tablica = tablica #Pytanie jak zaimplementować tą tablicę. Jest biblioteka do pracy z tablicami i ona nazywa się numpy
		
	def akutalizuj(self):
		T = np.zeros(self.tablica.shape)
		for i in range(self.tablica.shape[0]):
			for j in range(self.tablica.shape[1]):
				ilosc_sasiadow = 0
				if i > 0 and j > 0:
					if self.tablica[i-1,j-1] ==1:
						ilosc_sasiadow += 1
				if i>0:
					if self.tablica[i-1,j] == 1:
						ilosc_sasiadow += 1

				if i > 0  and j < self.tablica.shape[1]-1:
					if self.tablica[i-1,j+1] == 1:
						ilosc_sasiadow += 1

				if j < self.tablica.shape[1]-1:
					if self.tablica[i, j+1] == 1:
						ilosc_sasiadow += 1

				if i < self.tablica.shape[0]-1 and j < self.tablica.shape[1]-1:
					if self.tablica[i+1,j+1] == 1:
						ilosc_sasiadow += 1

				if i < self.tablica.shape[0]-1:
					if self.tablica[i+1, j] == 1:
						ilosc_sasiadow += 1

				if j > 0 and i < self.tablica.shape[0]-1:
					if self.tablica[i+1, j - 1] == 1:
						ilosc_sasiadow += 1

				if j > 0:
					if self.tablica[i, j-1] == 1:
						ilosc_sasiadow += 1
				if ilosc_sasiadow == 2:
					T[i,j] = 1
				else:
					T[i, j] = 0
		self.tablica = T

	def drukuj(self):
		n = self.tablica.shape[0]
		m = self.tablica.shape[1]


		for i in range(n):
			for j in range(m):
				if self.tablica[i,j]  == 1:
					pygame.draw.rect(screen, (0, 255, 0),
									 (j*RECT_SIZE,i*RECT_SIZE,(j+1)*RECT_SIZE, (i+1)*RECT_SIZE))
				else:
					pygame.draw.rect(screen, (0, 0, 0),
									 (j * RECT_SIZE, i * RECT_SIZE, (j + 1) * RECT_SIZE, (i + 1) * RECT_SIZE))
		for i in range(m):
			pygame.draw.line(screen, (0, 255, 0), ((SCREEN_WIDTH * i) / m, 0), ((SCREEN_WIDTH * i) / m, SCREEN_HEIGHT))
		for i in range(n):
			pygame.draw.line(screen, (0, 255, 0), (0, (SCREEN_HEIGHT * i) / n), (SCREEN_WIDTH, (SCREEN_HEIGHT * i) / n))

		pygame.display.flip()
		return None


def zaladuj(plik, n, m):
	tablica = np.zeros((n,m))
	j = 0
	f = open(plik, 'r')
	for word in f:
		i = 0
		for letter in list(word):
			if letter != '\n' and int(letter) != 0 and i < m and j < n:
				tablica[j, i] = 1
			i += 1
		j += 1

	f.close()
	return Mapa(tablica)
	
if __name__ == '__main__':
	Mapa = zaladuj(plik, n, m)
	Mapa.drukuj()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == KEYDOWN and event.key == pygame.K_SPACE:
				Mapa.akutalizuj()
				Mapa.drukuj()
			elif event.type == QUIT:
				running = False

