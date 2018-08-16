<?php 
?>

<!DOCTYPE html>
<html>
    <head>
        <title>Test Docker-compose</title>
    </head>

    <body>
        Ceci est un test - BDD active
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
            $bdd->exec("CREATE TABLE IF NOT EXISTS test1(
                id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
                libelle VARCHAR(40) NOT NULL);"
            );

            //Insert test element
            $bdd->exec("INSERT INTO test(libelle) VALUES('Libelle dans la base');");
            $req = $bdd->query("SELECT * FROM test;")->fetch();
            echo '<p>'. $req['libelle'] . '</p>';

            $bdd->exec("INSERT INTO test1(libelle) VALUES('test1');");
            $req = $bdd->query("SELECT * FROM test1;")->fetch();
            echo '<p>'. $req['libelle']. '</p>';
        ?>
    </body>
</html>

