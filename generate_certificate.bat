@echo off


make generate_ca NAME=RootCA DIR=./ssl

make generate_intermediate_ca NAME=ServerCA ROOT=RootCA DIR=./ssl


for /L %%i in (1,1,3) do (
    make generate_cert NAME=server%%i ROOT=ServerCA DIR=./ssl/server
)


make generate_intermediate_ca NAME=ClientCA ROOT=RootCA DIR=./ssl


for /L %%i in (1,1,50) do (
    make generate_cert NAME=client%%i ROOT=ClientCA DIR=./ssl/client
)


copy /b ssl\RootCA\RootCA.pem + ssl\ClientCA\ClientCA.pem ssl\RootCA\RootCA_with_ClientCA.pem
copy /b ssl\RootCA\RootCA.pem + ssl\ServerCA\ServerCA.pem ssl\RootCA\RootCA_with_ServerCA.pem


pause
