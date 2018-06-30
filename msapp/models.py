from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from math import sqrt



# Create your models here.
class Usuario(models.Model):
    user 		= models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
    	return self.username


class Modelo1(models.Model):
	nombre_producto		= models.CharField(max_length=50)
	categoria	= models.CharField(max_length=50)
	usuario 	= models.ForeignKey(User, on_delete=models.CASCADE)

	#stock actual
	#stock 		= models.IntegerField(verbose_name = "Stock actual", default=100)
	
	#Tiempo de simulacion
	tiempo 	= models.FloatField(default=1)

	#Tasa de demanda (unidades por unidad de tiempo)
	d		= models.IntegerField(verbose_name='Demanda Total', validators=[MinValueValidator(0)])

	#Costo de preparación correspondiente 
	#a la colocación de un pedido ($/pedido)		
	k 		= models.FloatField(verbose_name='Costo de Preparación de Pedido', validators=[MinValueValidator(0)])		

	#Costo de almacenamiento 
	#($ por unidad en inventario por unidad de tiempo)
	h 		= models.FloatField(verbose_name='Costo Unitario de Almacenamiento', validators=[MinValueValidator(0)])

			
	
	def __str__(self):
		return self.nombre_producto

	def inventario_promedio(self):
		return self.d / 2
	ip = property(inventario_promedio)

	def lote_optimo_compra(self):

		resultado = round(sqrt((2*self.k*self.d)/self.h)) 
		
		if (resultado > self.d):
			return self.d

		return resultado
	loc = property(lote_optimo_compra)

	def longitud_ciclo(self):
		lc = self.loc / (self.d/self.tiempo)

		if(lc < 1):
			lc = lc * 365 #paso a dias		

		return	format(lc, '.2f')

	lc 	= property(longitud_ciclo)

	def costo_inventario(self):
		yy = self.loc
		dd = self.d
		kk = self.k
		hh = self.h
		yd = yy/dd
		termino1 = kk / yd
		termino2 = hh * (yy/2)
		return round(termino1 + termino2) 
	ci = property(costo_inventario)