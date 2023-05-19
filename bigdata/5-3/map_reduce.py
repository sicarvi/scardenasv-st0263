from mrjob.job import MRJob, MRStep
from statistics import mean
from datetime import datetime
class PromedioSectorEconomico(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        sececon,salario = aux[1], int(aux[2])
        yield sececon,salario

    def reducer(self, sececon, values):
        yield sececon, mean(values)

class PromedioEmpleado(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        idemp,salario = aux[0], int(aux[2])
        yield idemp,salario

    def reducer(self, idemp, values):
        yield idemp, mean(values)

class NumeroSEEmpleado(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        idemp = aux[0]
        yield idemp,1

    def reducer(self, idemp, values):
        yield idemp, sum(values)
#----------------------------------------------------#
class AccionMenorMayor(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        company,price,date = aux[0], float(aux[1]), aux[2]
        yield company,(price,date)

    def reducer(self, company, values):
            lista = list(values)
            min_val = 100000
            max_val = 0
            date_min = ''
            date_max = ''
            for d in lista:
                if d[0] < min_val:
                    min_val = d[0]
                    date_min = d[1]
                if d[0] > max_val:
                    max_val = d[0]
                    date_max = d[1]

            yield company, (date_min, date_max)

class AccionesEstables(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        company,price= aux[0], float(aux[1])
        yield company,price

    def reducer(self, company, values):
            lista = list(values)
            val_anterior = 0
            flag = False
            for d in lista:
               if d > val_anterior or d == val_anterior:
                   val_anterior = d
               else:
                   flag = True
            if not flag:
                yield company, "Estable o en crecimiento"

class DiaNegro(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        date,price= aux[2], float(aux[1])
        yield date,price

    def reducer1(self, date, values):
        lista = list(values)
        suma = sum(lista)
        yield None, [suma, date]

    def reducer2(self, _, date_sum_pairs):
        yield min(date_sum_pairs)

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer1),
            MRStep(reducer=self.reducer2),
        ]
#----------------------------------------------#
class UsuarioPeliculas(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        user,rating = aux[0], int(aux[2])
        yield user,rating

    def reducer(self, user, values):
            lista = list(values)
            yield user, [len(lista), mean(lista)]

class DiaMax(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        date = aux[-1]
        yield date,1

    def reducer1(self, date, values):
        yield None, [sum(values), date]
       
    def reducer2(self, _, date_sum_pairs):
        yield max(date_sum_pairs)

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer1),
            MRStep(reducer=self.reducer2),
        ]

class DiaMin(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        date = aux[-1]
        yield date,1

    def reducer1(self, date, values):
        yield None, [sum(values), date]
       
    def reducer2(self, _, date_sum_pairs):
        yield min(date_sum_pairs)

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer1),
            MRStep(reducer=self.reducer2),
        ]

class PeliculaPromedio(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        movie,rating = aux[1], int(aux[2])
        yield movie, rating

    def reducer(self, movie, values):
            lista = list(values)
            yield movie, [len(lista), mean(lista)]

class PeorDiaRating(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        date,rating = aux[-1], int(aux[2])
        yield date, rating

    def reducer1(self, date, values):
        yield None, [mean(values), date]
       
    def reducer2(self, _, date_avg_pairs):
        yield min(date_avg_pairs)

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer1),
            MRStep(reducer=self.reducer2),
        ]
    
class MejorDiaRating(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        date,rating = aux[-1], int(aux[2])
        yield date, rating

    def reducer1(self, date, values):
        yield None, [mean(values), date]
       
    def reducer2(self, _, date_avg_pairs):
        yield max(date_avg_pairs)

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer1),
            MRStep(reducer=self.reducer2),
        ]
    
class MejorYPeorXGenero(MRJob):

    def mapper(self, _, line):
        aux = line.split(',')
        genre, movie, rating = aux[-2], aux[1], int(aux[2])
        yield genre, [rating, movie]

    def reducer1(self, genre, values):
        lista = list(values)
        sumas = {}
        for c in lista:
            if c[1] not in sumas:
                sumas[c[1]] = c[0]
            else:
                sumas[c[1]] += c[0]

        sumas_tolist = [[v,k] for k,v in sumas.items()]        
        yield genre, sumas_tolist
       
    def reducer2(self, genre, sum_movie_pairs):
        lista = list(sum_movie_pairs)
        lista = lista.pop(0)
        """ min_rating = 100
        max_rating = 0
        min_movie = ''
        max_movie = ''
        for c in lista:
            if c[0][0] < min_rating:
                min_rating = c[0][0]
                min_movie = c[0][1]
            if c[0][0] > max_rating:
                max_rating = c[0][0]
                max_movie = c[0][1] """
        mi = min(lista)
        ma = max(lista)
        yield genre, [mi,ma]

    def steps(self):
        return [
            MRStep(mapper=self.mapper),
            MRStep(reducer=self.reducer1),
            MRStep(reducer=self.reducer2)
        ]
if __name__ == '__main__':
    #con dataempleados.txt
    #Punto 1:
    #PromedioSectorEconomico.run()
    #Punto 2:
    #PromedioEmpleado.run()
    #Punto 3:
    #NumeroSEEmpleado.run()
    #-------------------------------------#
    #con dataempresas.txt
    #Punto 1:
    #AccionMenorMayor.run()
    #Punto 2:
    #AccionesEstables.run()
    #Punto 3:
    #DiaNegro.run()
    #-------------------------------------#
    #con datapeliculas.txt
    #Punto 1
    #UsuarioPeliculas.run()
    #Punto 2
    #DiaMax.run()
    #Punto 3
    #DiaMin.run()
    #Punto 4
    #PeliculaPromedio.run()
    #Punto 5
    #PeorDiaRating.run()
    #Punto 6
    #MejorDiaRating.run()
    #Punto 7
    MejorYPeorXGenero.run()
