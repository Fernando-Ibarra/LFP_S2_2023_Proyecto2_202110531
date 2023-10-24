import json
import codecs
from models.Error import errorsList

def processErrors():
    # create a dictionary
    error_dict = dict()
    error_dict['errors'] = []

    # create a json file
    # create a json file with errorList info
    
    with codecs.open('RESULTADOS_202110531.json', 'w', 'utf-8') as error_file:
        for index, error in enumerate(errorsList):
            error_dict['errors'].append({
                "No.": index + 1,
                "descripcion": {
                    "lexema": error.lexema,
                    "tipo": str(error.tipo),
                    "fila": error.row,
                    "columna": error.column
                }
            })
        # error_file.write(str(error_dict))
        json.dump(error_dict, error_file, ensure_ascii=False, indent=4)
