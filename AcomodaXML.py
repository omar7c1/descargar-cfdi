import glob, os, errno, moment, shutil
from xml.dom import minidom
from dateutil.parser import parse

class AcomodaXML:
    def __init__(self, direccionOrigen, direccionDestino):
        self.__direccionOrigen=direccionOrigen
        self.__direccionDestino=direccionDestino

    def __mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

    def __getFiles(self, directory):
        file_paths = []
        for root, directories, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
#                print("Cargando archivo: " + filepath)
        return file_paths

    def ordenar(self, formato):
        archivosOrigen=self.__getFiles(self.__direccionOrigen)
        for filename in archivosOrigen:
            xmldoc = minidom.parse(filename)
            cfdiComprobante = xmldoc.getElementsByTagName('cfdi:Comprobante')
            tfdTimbreFiscal = xmldoc.getElementsByTagName('tfd:TimbreFiscalDigital')
            cfdiEmisor = xmldoc.getElementsByTagName('cfdi:Emisor')
            cfdiReceptor = xmldoc.getElementsByTagName('cfdi:Receptor')
            
            #Obtener valores para generar cadena de remplazo
            UUID=tfdTimbreFiscal[0].attributes['UUID'].value
            emisorRFC=cfdiEmisor[0].attributes['rfc'].value
            emisorNombre=cfdiEmisor[0].attributes['nombre'].value
            receptorRFC=cfdiReceptor[0].attributes['rfc'].value
            receptorNombre=cfdiReceptor[0].attributes['nombre'].value

            #Traemos ano y mes de factura
            fecha=cfdiComprobante[0].attributes['fecha'].value
            oFecha=moment.date(fecha, '%Y-%m-%dT%H:%M:%S') # 2014-08-03T16:30:33
            ano=oFecha.format('YYYY')
            mes=oFecha.format('M')
            dia=oFecha.format('D')
            #print("Parcer date: " +fecha+" - " +ano+" - " +mes+" - " +dia)

            #Generando cadena de localizacion para copiar
            formatoDST=formato.replace('@UUID@', UUID)
            formatoDST=formatoDST.replace('@emisorRFC@', emisorRFC)
            formatoDST=formatoDST.replace('@emisorNombre@', emisorNombre)
            formatoDST=formatoDST.replace('@receptorRFC@', receptorRFC)
            formatoDST=formatoDST.replace('@receptorNombre@',receptorNombre)
            formatoDST=formatoDST.replace('@fecha@', fecha)
            formatoDST=formatoDST.replace('@ano@', ano)
            formatoDST=formatoDST.replace('@mes@', mes)
            formatoDST=formatoDST.replace('@dia@', dia)

            #Definimos ruta destino de archivo
            destinoXML=self.__direccionDestino+formatoDST
            destinoDirectorio=os.path.dirname(destinoXML)

            #Creando directorio destino
            if not os.path.exists(destinoDirectorio):
                self.__mkdir_p(destinoDirectorio)

            #Copiando archivo 
            shutil.copy(filename, destinoXML)
            #print(UUID + '---' + destinoXML)














