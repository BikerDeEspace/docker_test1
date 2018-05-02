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
            //Try connect to database 
            while($bdd == null){
                try{
                    $bdd = new PDO('mysql:host=db:3306;dbname=app', 'app', 'app');
                    $bdd->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
                } catch(Exception $e){
                    echo "<script>console.log( 'Initialisation base de données' );</script>";
                    sleep(10);
                }
            }

            //Create table if not exist
            $bdd->exec("CREATE TABLE IF NOT EXISTS test(
                id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                libelle VARCHAR(40) NOT NULL);"
            );

            //Insert test element
            $bdd->exec("INSERT INTO test(libelle) VALUES('Libelle dans la base');");
            
            //Get test element
            $req = $bdd->query("SELECT * FROM test;")->fetch();
            
            //print test element
            echo $req['libelle'];
        ?>
    </body>
</html>

