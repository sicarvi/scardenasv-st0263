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
    DiaNegro.run()