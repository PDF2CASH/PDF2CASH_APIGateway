#!/bin/bash

apt get install zip
apt get install curl
cd ..
zip -r  ./apigateway.zip ./build
curl -F 'file=@./apigateway.zip' https://pdf2cash-cloudupdater.herokuapp.com/api/system/apigateway/
