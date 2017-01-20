# -*- coding: UTF-8 -*-
'''
Se describen los tipos de aeronaves donde la clase base es Nave y la adoptan 
todas las naves de tipo civil-neutral. Las clases Smuggler y Patrulla heredan
a Nave.
'''

from time import strftime


# Estas son las constantes de escala cuando se grafican las naves
H_ESCALA = 1.0/500
V_ESCALA = 1.0/100	

	
class Nave(object):
	def __init__(self, 		nombre='Cessna',	pos=0,
				 altitud=0,	direccion='e',		fuel=1000,
				 Vmax=450,	Carga=500,			status='landed',
				 vel=0,		piloto='Paul',		potencia=0):
		self.nombre = nombre
		self.pos = pos
		self.alt = altitud
		self.direc = direccion
		self.fuel = fuel 
		self.Vmax = Vmax * (1000.0/3600)		# Internamente se trabaja mks
		self.Carga = Carga 
		self.status = status
		self.vel = vel * (1000.0/3600)
		self.piloto = piloto
		self.h = int(altitud * V_ESCALA) 		# Son las coordenadas 
		self.x = int(pos * H_ESCALA)			# para graficar
		self.P = potencia
		if self.status == 'landed': self.brakes = True
		if self.status == 'flying': self.brakes = False
		if self.fuel > 1: self._fuel = True 	
		self._msg = ''
		self._evento = False					# Cuando algo va al monitor
		self.d_alt = 0							# Delta de altitud 
		if self.status == 'landed': self.gear = True
		else: self.gears = False
			
	def __str__(self):
		cadena = 'Neutral'
		return cadena	
	
	def formateador(self, msg):	
		ts = strftime('[%H:%M:%S]: ')
		self._msg = ts+msg
		self._evento = True
		
	def combustible(self):
		if self.fuel > 1:
			self._fuel = True
		elif self.fuel <= 1:
			self._fuel = False
			self.fuel = 0
		self.fuel -= 0.05 * self._fuel*self.P	
	
	# Las funciones de velocidad no tienen aproximación física
	def Volar(self, ):
		self.vel = ((self.Vmax * (self._fuel*self.P /100.0)) + 2*self.vel) / 3
		if self.direc == 'e':
			self.pos += self.vel
		elif self.direc == 'w':
			self.pos -= self.vel 	
		self.x = int(self.pos * H_ESCALA)
		self.alt -= self.d_alt * self.vel * 0.08 / 4
		self.h = int(self.alt * V_ESCALA) 
		
	def Rodar(self):
		if self.brakes == True: 
			if self.vel <= 4:
				pass
			elif self.vel > 4: 
				self.vel = 	((self.Vmax * (self._fuel*self.P /100.0)) 
							+ self.vel) / 4
		elif self.brakes == False:	
			self.vel = ((self.Vmax * (self._fuel*self.P /100.0)) 
						+ 2*self.vel) / 3
		self.pos += self.vel 	
		self.x = int(self.pos * H_ESCALA)
		if self.vel > 0.6 * self.Vmax:
			self.alt -= self.d_alt * self.vel * 0.08 / 4
			self.h = int(self.alt * V_ESCALA) 

	
	def Chocar(self, terreno):
		if self.h <= terreno[self.x]:
			self.status = 'crashed'
			msg = '%s estrellado.' % self.nombre
			self.formateador(msg)
			return 
		elif self.h > terreno[self.x]:
			return
			
		
class Smuggler(Nave):
	def __init__(self, **kwargs):
		super(Cartel, self).__init__(**kwargs)
	
	def __str__(self):
		cadena = 'Cartel'
		return cadena	

class Patrulla(Nave):
	def __init__(self, **kwargs):
		super(Patrulla, self).__init__(**kwargs)
		
	def __str__(self):
		cadena = 'DEA'	
		return cadena
		
	def Radar(self,aviones):
		if self.direc == 'e':
			rad = self.x + 2
		elif self.direc == 'w':
			rad = self.x -2
		
		for avion in aviones:
			if avion.__str__() == 'Cartel':
				if ((avion.x == rad) & 
				   ((avion.h == self.h) ^ (avion.h == self.h-1))):
					msg = '%s Arrestado!' % avion.nombre
					self.formateador(msg)

	
	
						
			
