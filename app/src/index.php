<?php 
?>

<!DOCTYPE html>
<html>
    <head>
        <title>Test Docker-compose</title>
    </head>

    <body>
        <?php 
            $bdd = null; 
            while($bdd == null){
                try{
                    $bdd = new PDO('mysql:host=db:3306;dbname=app', 'app', 'app');
                    $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                } catch(Exception $e){
                    sleep(10);
                }
            }
            $bdd->exec("CREATE TABLE IF NOT EXISTS test(
                id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                libelle VARCHAR(40) NOT NULL);"
            );
            $bdd->exec("INSERT INTO test(libelle) VALUES('Libelle dans la base');");
            
            $req = $bdd->query("SELECT * FROM test;")->fetch();
            echo $req['libelle'];
        ?>
    </body>
</html>

