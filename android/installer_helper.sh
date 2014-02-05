#!/bin/sh

SL4A=/sdcard/SL4A

echo "1 - Instale no Android SL4A(http://code.google.com/p/android-scripting/)
2 - Abra o SL4A va em View>>Interprets>>Add e baixe Python
3 - Abra o Python e aperte Install
PRESSIONE ENTER PARA CONTINUAR INSTALAÇÃO APENAS QUANDO INSTALADO"
read

wget -c http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.2.1.tar.gz
tar zxf BeautifulSoup-3.2.1.tar.gz
cp BeautifulSoup-3.2.1/BeautifulSoup.py .
rm -rf BeautifulSoup-3.2.1
rm -rf BeautifulSoup-3.2.1.tar.gz

wget -c http://pypi.python.org/packages/source/m/mechanize/mechanize-0.2.5.tar.gz
tar zxf mechanize-0.2.5.tar.gz
cp -rf mechanize-0.2.5/mechanize .
rm -rf mechanize-0.2.5
rm mechanize-0.2.5.tar.gz
#adb push bs4 $SL4A/scripts/bs4
adb push mechanize $SL4A/scripts/mechanize
adb push renewer.py $SL4A/scripts/
adb push ../unicap_br/unicap_br.py $SL4A/scripts/
adb push BeautifulSoup.py $SL4A/scripts/
echo "Digite a matricula(apenas numeros): "
read MATRICULA
echo "Digite a senha: "
read SENHA
echo $MATRICULA > unicap.txt
echo $SENHA >> unicap.txt
adb push unicap.txt $SL4A/
rm unicap.txt
rm -rf mechanize
rm BeautifulSoup.py
