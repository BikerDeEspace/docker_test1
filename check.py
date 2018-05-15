import os
import sys
import re

ERRORS = {  "101":"Fichier Docker-compose.yml introuvable", 
            "102":"Aucun service renseigné",
            "103":"Image du service introuvable", 
            "104":"Aucune Image ou Dockerfile associé au service ",
            "105":"Aucun service ne communique avec la machine hôte", 

            "201":"Fichier Dockerfile introuvable",
            "202":"Instructions primaires manquantes",
            "203":"Instructions sans arguments",
            "204":"COPY / ADD : Fichiers spécifiés introuvables",
            "205":"EXPOSE : Port introuvable dans l’instruction ports du fichier Docker-compose.yml"
         }

#------------------
#verif_dockerfile
#------------------

#DEBUT verif_dockerfile
def verif_dockerfile(path, ports):
    errors = list()
    #On vérifie que le Dockerfile existe
    if os.path.exists(path+'/Dockerfile'):
        #On ouvre le fichier
        with open(path+'/Dockerfile', 'r') as file:
            #On récupére le contenu du fichier
            dockerfile = file.read()

            #On extrait les instructions (RegEx)
            instructions = re.findall(r"(?<=\n)[A-Z]+", dockerfile)

            print(instructions)

            #On vérifie que les instructions primaires sont présentes
            if ('FROM' not in instructions) or ('EXPOSE' not in instructions):
                #ERREUR 202
                errors.append('202')

            for instruction in instructions:
                #On vérifie que chaque instruction possède au moins un argument
                if not re.findall(r"(?<={}\s)\S+".format(instruction), dockerfile):
                    #ERREUR 203
                    errors.append('203')

            #On extrait le port exposé par le container (RegEx)
            container_port = re.findall(r"(?<=EXPOSE\s)\S+", dockerfile)

            #On vérifie que le port exposé est bien dans la liste des ports du service si elle existe
            if(ports and (container_port not in ports)):
                #ERREUR 205
                errors.append('205')

            #On vérifie si il existe des instructions COPY ou ADD
            if ('COPY' in instructions) or ('ADD' in instructions):
                #On extrait leurs arguments (RegEx)
                arg_copy_add = re.findall(r"(?<=COPY\s)\S+|(?<=ADD\s)\S+", dockerfile)

                #On parcours les arguments capturés
                for arg in arg_copy_add:
                    #On vérifie que l'emplacement ou le fichier existe
                    if not os.path.exists('{}/{}'.format(path, arg)):
                        #ERREUR 204
                        errors.append('204')
    else:
        #ERREUR 201
        errors.append('201')

    return errors

#FIN verif_dockerfile

#------------------
#verif_docker_compose
#------------------

#DEBUT verif_docker_compose
def verif_docker_compose():
    #SI EXISTE docker-compose.yml ALORS
        # Récupération des services (YAML['service'])
        #SI EXISTE services ALORS
            #TANT QUE services FAIRE
                # Récupération des ports (RegEx)
                #SI EXISTE Ports ALORS
                    #port_hote = VRAI
                #Récupération Image
                #SI EXIST Image ALORS
                    # Vérification Image
                    #SI image non disponible ALORS
                        # ERREUR 103
                #SINON
                    #Récupération Build
                    #SI EXISTE Build ALORS
                        # Appel VerifDockerfile
                    #SINON
                        #ERREUR 104
            #FIN TANT QUE
            #SI port_hote == FAUX
                #ERREUR 105
        #SINON
            #ERREUR 102
    #SINON
        #ERREUR 101
    pass
#FIN verif_docker_compose

#------------------
#verif_logs
#------------------

#DEBUT verif_logs
def verif_logs():
    #TANT QUE container FAIRE
        #Extraction Erreurs fichier de log

        #SI EXISTE Erreurs ALORS
            #Extraction des codes et des messages
    #FIN TANT QUE
    pass
#FIN verif_logs

#------------------
# Main
#------------------

#DEBUT
def main():
    errors = verif_dockerfile('./app', list())

    print(errors)
    #Appel VerifDockerCompose
    #SI NON Erreurs ALORS
        #Exec docker-compose up -d
        #Appel VerifLogs

        #Ecriture des erreurs dans un fichier de log
        #Afficher Erreurs
    pass
#FIN

main()
