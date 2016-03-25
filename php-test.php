<?php


    function proxyDrupalLogin($object){
        $json = json_encode( $object );
        $json = http_build_query($object);
        $ch = curl_init();

        curl_setopt( $ch, CURLOPT_URL, 'https://emammal.si.edu/emammal_api/deployment/login' );
        curl_setopt( $ch, CURLOPT_USERAGENT, 'eMammal_API/1.0' );
        curl_setopt( $ch, CURLOPT_CUSTOMREQUEST, 'POST' );
        curl_setopt( $ch, CURLOPT_POSTFIELDS, $json );
        curl_setopt( $ch, CURLOPT_VERBOSE, 1 );
        curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1 );
        curl_setopt( $ch, CURLOPT_SSL_VERIFYPEER, 0 );

        $response = curl_exec( $ch );
        print_r($response);
        //$json = json_decode( $response );
        //curl_close( $ch );

        return $json;

    }

    proxyDrupalLogin(array(
        'username' => 'aallegretti',
        'password' => 'BlueRaster2014!',
        'exclude_deployments' => True,

    ))

?>

