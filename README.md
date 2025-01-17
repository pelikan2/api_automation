# API automation using python, pytest and jenkins pipelines

Tento sluzi na automatizaciu volne dostupnych APIs z https://petstore.swagger.io/, APIs su rozdelene do 3 sekcii
alebo ak chcete "features", kde si mozete precvicit rozne druhy API testov.
Tento konkretny projekt vyuziva na automatizaciu python a jeho kniznicu pytest.

# Prvotne nastavenia

V prvom rade treba nainstalovat python do vasho PC, link https://www.python.org/downloads/.
Potom naklonovat projekt z greyson gitlabu, link tu: https://gitlab.com/vladimir.pelikan/api_testing.git
do vasho oblubeneho IDE.
V subore :requirements.txt" sa nachadzaju kniznice, ktore treba do projektu nainstalovat, preto do teminalu zadajte 
prikaz:

<br>MacOS: pip3 install -r requirements.txt </br>
<br>Windows: pip install -r requirements.txt </br>

# Praca s testami

V projekte si mozete vsimnut, ze niektore funkcie maju pred nazvom slovo test_,
Takto pytest rozlisuje, ci je funkcia bezna (pomocna), teda bez zaciatocneho nazvu test_
alebo funkcia s test_, ktoru berie ako vnima ako automatizovany test
Teraz by malo byt vsetko nastavene a je mozne spustat testy, da sa to viacerymi sposobmi:

1. Spustanie pomocou buttonu "play", ktory sa nachadza na lavo od funkcie s oznacenim "test_"
2. pomocou terminalu:
- ak je treba spustit vsetky testy na to funguje prikaz, macOS: python3 -m pytest -v -s, windows: python -m pytest -v -s, ktory spusti vsetky testy a vypise, ktore testy padli a ktore nie + pri failed testoch aj miesto, kde je problem.
- v projekte su pouzite tzv. tagy, ktorymi su oznacene jednotlive features, ak teda je nutne stustit len jednu feature, potom bude prikaz nasledovny: pytest -m <tag> -v. 


# Nastavenie Jenkins lokalne a vytvorenie fungujucej pipeline

MacOS:

V prvom rade treba nainstalovat homebrew, link: https://brew.sh/
Instalacia jenkinsu: brew install jenkins-lts
Start jenkinsu: brew services start jenkins-lts, po zadani tohto prikazu by ste mali dostat link na localhost, kde sa vas jenkins nachadza,
zadajte ho do browsera, spusti sa jenkins, bude od vas chiet heslo, ktore najdete v logoch pri starte, prikaz: 
cat /var/log/jenkins/jenkins.log

Priamo v jenkinse uz treba vytvorit len novu pipeline. Na dashboarde je moznost "novy", zadate pipeline a nazov.
Otvori sa nastavenie tejto pipeline, jedine co vas tu bude zaujimat je pipeline script (uplne dole)
Cely skript sa sklada z niekolkych "stages":


    pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: '2103ce3c-6b16-4b38-a6f1-93225fdf84e9', url: 'https://gitlab.com/vladimir.pelikan/api_testing.git']])
            }
        }
        stage('Build') {
            steps {
                sh 'pip3 install pytest'
                sh 'pip3 install requests'
            }    
        }
        stage('Test') {
            steps {
                sh 'python3 -m pytest -m pet -v -s'
                echo 'The job has been tested'
            }
        }
    }
    }

Toto je priklad ako by taky script pre pipeline mohol vyzerat.
V prvom rade je treba sa checkoutnut na branchu, ktoru chcete testovat.
Potom nainstalovat potrebne kniznice a nakoniec prichadza na rad samotne testovanie.

Windows:

Stiahnite najnovsiu verziu java JDK na oficialnej stranke, link: https://www.oracle.com/java/technologies/downloads/
potom stiahnite jenkins.war subor z jenkins oficialnej stranky, link: https://www.jenkins.io/download/, ulozte .war subor niekde, kde ho nepriehliadnete.
Otvorte terminal v zlozke, kde sa nachadza jenkins.war subor a zadajte: java -jar jenkins.war.
Potom otvorte prehliadac a zadajte link http://localhost:8080/. Jenkins od vas bude vyzadovat Admin heslo, ktore najdete
v err txt subore v zlozke jenkins, skopirujte a kliknite na continue. Kliknite na install suggested plugins, potom si
vytvorte ucet a mozete pouzivat jenkins.
link na setup: https://www.jenkins.io/doc/book/installing/windows/

Priamo v jenkinse uz treba vytvorit len novu pipeline. Na dashboarde je moznost "novy", zadate pipeline a nazov.
Otvori sa nastavenie tejto pipeline, jedine co vas tu bude zaujimat je pipeline script (uplne dole)
Cely skript sa sklada z niekolkych "stages":

    pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: '2103ce3c-6b16-4b38-a6f1-93225fdf84e9', url: 'https://gitlab.com/vladimir.pelikan/api_testing.git']])
            }
        }
        stage('Build') {
            steps {
                bat 'pip install pytest'
                bat 'pip install requests'
            }    
        }
        stage('Test') {
            steps {
                bat 'python -m pytest -m pet -v -s'
                echo 'The job has been tested'
            }
        }
    }
    }


Toto je priklad ako by taky script pre pipeline mohol vyzerat.
V prvom rade je treba sa checkoutnut na branchu, ktoru chcete testovat.
Potom nainstalovat potrebne kniznice a nakoniec prichadza na rad samotne testovanie.

# Spustenie testov na Docker image

Testy sa daju spustat aj na tzv. docker image, vyhodou je napriklad, ze tak nezahlcuje pamat PC oproti napriklad virtualke.
Na to, aby ste vedeli spustat testy cez Docker si potrebujete stiahnut Docker, link: https://docs.docker.com/desktop/install/mac-install/
Vytvorit si ucet na Docker a potom v projekte, ktory chcete pouzit vytvorit "Dockerfile", nazov treba dodrzat, lebo system ho vie prave podla toho nazvu rozpoznat.
***
<br>FROM python:3.11-slim-buster  -pouzivame python 3.11 </br>
<br>WORKDIR /python_api_automation - vytvorime novu zlozku pre docker build </br>
<br>COPY requirements.txt ./ - do novej zlozky skopirujeme requirements.txt </br>
<br>RUN pip install --no-cache-dir -r requirements.txt - nainstalujeme requirementy </br>
<br>COPY . . - skopirujeme zvysok  lokalnych suborov z api_testing no zlozky s novym Docker image </br>
<br>CMD ["pytest", "test_steps.py"] - spustime testy </br>

***

Toto je jednoduchy priklad co by mohol obsahovat Dockerfile.

<br> Prikaz na vybuildenie: docker build -t nazov_image . </br>
<br> Potom uz staci len spustit na Docker aplikacii vas novo vytvoreny docker image alebo do terminalu treba zadat  docker run nazov_image </br>

# Generovanie Allure Reportov

Na generovanie allure reportov pre pytest projekt je potrebne nainstalovat kniznoci allure-pytest, ktora uz je obsiahnuta v subore requirements.txt
a nainstalovat allure do systemu
<br> MacOS: brew install allure </br>
<br> Windows: instalacia balika scoop, link: https://scoop.sh/, instalacia allure: scoop install allure</br>

Potom treba pouzit allure v testoch tak, ako je napriklad pouzity na tomto projekte.
<br> vygenerovanie .json suborov pre kazdy test na vytvorenie allure reportu: pytest -v -s --alluredir=reportallure </br>, tento prikaz spusti testy, ktorych vysledky sa ulozia do json suborov do zlozky reportallure
<br> allure serve reportallure\ - vygeneruje allure report, ktory najdete v prehliadaci</br>


# Dokumentacie

<br> Python dokumentacia: https://docs.python.org/3/ </br>
<br> Dokumentacia na pytest: https://docs.pytest.org/en/7.1.x/contents.html </br>
<br> Dokumentacia na kniznicu requests: https://requests.readthedocs.io/en/latest/ </br>
<br> Dokumentacia na allure: https://allurereport.org/docs/gettingstarted-installation/ </br>


