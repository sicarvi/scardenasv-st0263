from mrjob.job import MRJob
from statistics import mean

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
