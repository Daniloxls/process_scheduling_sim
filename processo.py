class Processo ():
    def __init__(self,numero, inicio, duracao, prioridade):
        self.n = numero
        self.ini = int(inicio)
        self.dur = int(duracao)
        self.prior = int(prioridade)
        self.time_left = int(duracao)
