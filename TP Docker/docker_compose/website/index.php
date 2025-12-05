<html>
    <head>
        <title>My Shop</title>
    </head>
    <body>
        <h1>Liste des produits disponibles :</h1>
        <ul>
            <?php
            $json = file_get_contents('http://product-service:80/');
            $obj = json_decode($json);

            $products = $obj->products;
            foreach ($products as $product){
                echo "<li>$product</li>";
            }
            ?>
        </ul>
    </body>
</html>
