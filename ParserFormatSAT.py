class ParserFormatSAT:

    def __init__(self, fuente):
        self.fuente=fuente
        self.__valores={}
        self.__items={}
        self.__validos=['EVENTTARGET', '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE']

    def __procesar(self):
        self.__valores=self.fuente.split('|')

    def __ordenaValores(self):
        name=''
        self.__ordenados={}
        for index in range(len(self.__valores)):
            item=self.__valores[index]
            if item in self.__validos:
                name=item
                index+=1
                item=self.__valores[index]
                self.__items[name]=item
                name=''

    def obtenerValoresFormulario(self):
        self.__procesar()
        self.__ordenaValores()
        return self.__items
