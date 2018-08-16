# Image mysql:5.7
FROM mariadb

RUN sed -i 's/^innodb_flush_method/#innodb_flush_method/' /etc/mysql/my.cnf

# Encryption config
COPY encryption.cnf /etc/mysql/conf.d/encryption.cnf 

#
COPY .key /etc/mysql/.key

# Expose port 3306
EXPOSE 3306
