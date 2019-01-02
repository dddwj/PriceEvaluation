<html>
<head>
    <title>评估结果</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>Handle_form Page</h1>
    <?php

    //[post] URL中不带参数

    ini_set('dispaly_erors', 1);

    error_reporting(E_ALL|E_STRICT);


    $address = $_POST['address'];
    $floor = $_POST['floor'];
    $square = $_POST['square'];
    $direction = $_POST['direction'];
    $height = $_POST['height'];
    $buildyear = $_POST['built_year'];

    if (strlen($buildyear) == 0) {
        $buildyear = 2000;
    }

    if (strlen($address) == 0 or strlen($floor) == 0 or strlen($square) == 0 or strlen($direction) == 0 or strlen($height) == 0){
        print "\nEmpty Input!";
    }
    else {
        // [get] URL中带参数
        /*
        ini_set('dispaly_erors', 1);

        error_reporting(E_ALL|E_STRICT);

        $address = $_GET['address'];
        $floor = $_GET['floor'];
        $square = $_GET['square'];
        $direction = $_GET['direction'];
        */
        /*
        print "<p>address is $address</p>
               <p>floor is $floor</p>
               <p>square is $square</p>
               <p>direction is $direction</p>
               ";
        */

        $txt = $address . ',' . $floor . ',' . $direction . ',' . $square . ',' . $height . ',' . $buildyear;
        /*  写入txt文档

        $myfile = fopen("elements.txt", "w");
        fwrite($myfile, $txt);
        fclose($myfile);

        */

        echo "Got Elements in PHP!", $txt;
        echo "<br/>";

        /* 执行python文件 */
        //print ("Execute Python");
        //exec("~/anaconda3/bin/python ~/PyCharmProjects/PriceEvaluation/php/php_exec.py $txt encoding='utf-8'", $arr, $returnVal);
        // 【linux服务器上】同 $result = shell_exec("~/anaconda3/bin/python ~/PyCharmProjects/PriceEvaluation/php/php_exec.py $txt");
        $result = shell_exec("~/anaconda3/bin/python ~/PyCharmProjects/PriceEvaluation/php/php_exec.py $txt");
        sleep(5);
        $file = '/Users/dddwj/PyCharmProjects/PriceEvaluation/php/php_result.txt'; //先读取文件
        $cbody = file($file); //file（）函数作用是返回一行数组，txt里有三行数据，因此一行被识别为一个数组，三行被识别为三个数组
        for($i=0;$i<count($cbody);$i++){ //count函数就是获取数组的长度的，长度为3 因为一行被识别为一个数组 有三行
            echo "<h3>$cbody[$i]</h3>";
            echo "<br/>"; //最后是循环输出每个数组，在每个数组输出完毕后 ，输出一个换行，这样就可以达到换行效果
        }

//        print ("<xmp>");
//             print_r($arr);
//        print ("</xmp>");
//        echo "<br>" . $returnVal . "<br>";
    }

?>


</body>
</html>
