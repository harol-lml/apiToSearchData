import requests
import copy

from mongodb import mongo_db

dbname = mongo_db()

json_data = {
    'numeroCausa': '',
    'actor': {
        'cedulaActor': '',
        'nombreActor': '',
    },
    'demandado': {
        'cedulaDemandado': '',
        'nombreDemandado': '',
    },
    'provincia': '',
    'numeroFiscalia': '',
    'recaptcha': 'verdad',
    'first': 1,
    'pageSize': 10,
}

params = {
    'page': '1',
    'size': '10',
}

urlBase = f"https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion"


class get_data:

    def getById(id, per, page):

        if per == '0':
            json_data['actor']['cedulaActor'] = id

        elif per == '1':
            json_data['demandado']['cedulaDemandado'] = id

        else:
            return {'error':'person tipe no valid'}

        tp = 'actor' if per == '0' else 'demandado'

        datam = man.getDataMongo(id, tp)

        if(len(datam)>0):   return datam

        params['page'] = page
        response = requests.post(
            urlBase+"/buscarCausas",
            params=params,
            json=json_data,
        )
        # Verificamos que la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            procesos = response.json()
            for proceso in procesos:
                idJuce  = proceso['idJuicio']
                detail  = man.getDetailProcess(idJuce)
                proceso['detail'] = detail
                upJuice = man.getUpdateProcess(proceso)
                proceso['updates'] = upJuice
                dt = copy.deepcopy(proceso)
                dt['idUser'] = id
                dt['type'] = 'actor' if per == '0' else 'demandado'
                man.saveData(dt)
            return (procesos)
        else:
            error = 'Error al cargar la página:'. response.status_code
            return (error)

    def getDetailProcess(self, id):
        urlDetail = f"https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/{id}"
        response = requests.get(urlDetail)
        if response.status_code == 200:
            detalles = response.json()
            return (detalles)
        else:
            return (response)
        return urlDetail

    def getUpdateProcess(self, dataDetail):
        datajs = {
            "idMovimientoJuicioIncidente": dataDetail['detail'][0]['lstIncidenteJudicatura'][0]['idMovimientoJuicioIncidente'],
            "idJuicio": dataDetail['idJuicio'],
            "idJudicatura": dataDetail['detail'][0]['idJudicatura'],
            "idIncidenteJudicatura": dataDetail['detail'][0]['lstIncidenteJudicatura'][0]['idIncidenteJudicatura'],
            "aplicativo": "web",
            "nombreJudicatura": dataDetail['detail'][0]['nombreJudicatura'],
            "incidente": dataDetail['detail'][0]['lstIncidenteJudicatura'][0]['incidente']
        }
        response = requests.post(
            urlBase+"/actuacionesJudiciales",
            json=datajs,
        )

        if response.status_code == 200:
            updates = response.json()
            return updates
        else:
            print(datajs)

    def getDataMongo(self, id, per):
        return dbname.getById(id, per)

    def saveData(self, data):
        return dbname.postProcess(data)
man = get_data()