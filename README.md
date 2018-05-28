# docker_test1
Application multi containers Apache / MySQL

Ports: 80

# Containers
## Application principale
Nom: app
Ports: 80
Image: php:7.0-apache

## Base de données
Nom: bdd
Image: mysql:5.7
Port: 3306
