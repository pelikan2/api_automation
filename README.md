# API automation using python, pytest and jenkins pipelines

Tento sluzi na automatizaciu volne dostupnych APIs z https://petstore.swagger.io/, APIs su rozdelene do 3 sekcii
alebo ak chcete "features", kde si mozete precvicit rozne druhy API testov.
Tento konkretny projekt vyuziva na automatizaciu python a jeho kniznicu pytest.

# Prvotne nastaveenia

V prvom rade treba nainstalovat python do vasho PC, link https://www.python.org/downloads/.
Potom naklonovat projekt z greyson gitlabu, link tu: https://gitlab.com/vladimir.pelikan/api_testing.git
do vasho oblubeneho IDE.
V subore :requirements.txt" sa nachadzaju kniznice, ktore treba do projektu nainstalovat, preto do teminalu zadajte 
prikaz:
MacOS: pip3 install -r requirements.txt,
Windows: pip3 install -r requirements.txt

# Praca s testami

V projekte si mozete vsimnut, ze niektore funkcie maju pred nazvom slovo test_,
Takto pytest rozlisuje, ci je funkcia bezna (pomocna), teda bez zaciatocneho nazvu test_
alebo funkcia s test_, ktoru berie ako vnima ako automatizovany test
Teraz by malo byt vsetko nastavene a je mozne spustat testy, da sa to viacerymi sposobmi:

1. Spustanie pomocou buttonu "play", ktory sa nachadza na lavo od funkcie s oznacenim "test_"
2. pomocou terminalu:
- ak je treba spustit vsetky testy na to funguje prikaz, macOS: python3 -m pytest -v -s, windows: python -m pytest -v -s, ktory spusti vsetky testy a vypise, ktore testy padli a ktore nie + pri failed testoch aj miesto, kde je problem.
- v projekte su pouzite tzv. tagy, ktorymi su oznacene jednotlive features, ak teda je nutne stustit len jednu feature, potom bude prikaz nasledovny: pytest -m <tag> -v. 


# Nastavenie Jenkins lokalne a vytvorenie fungujucej pipeline pre macOS

V prvom rade treba nainstalovat homebrew, link: https://brew.sh/
Instalacia jenkinsu: brew install jenkins-lts
Start jenkinsu: brew services start jenkins-lts, po zadani tohto prikazu by ste mali dostat link na localhost, kde sa vas jenkins nachadza,
zadajte ho do browsera, spusti sa jenkins, bude od vas chiet heslo, ktore najdete v logoch pri starte, prikaz: 
cat /var/log/jenkins/jenkins.log

Priamo v jenkinse uz treba vytvorit len novu pipeline. Na dashboarde je moznost "novy", zadate pipeline a nazov.
Otvori sa nastavenie tejto pipeline, jedine co vas tu bude zaujimat je pipeline script (uplne dole)
Cely skript sa sklada z niekolkych "stages":
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
                sh 'python3 -m pytest -m user -v -s'
                echo 'The job has been tested'
            }
        }
    }
}
Toto je priklad ako by taky script pre pipeline mohol vyzerat.
V prvom rade je treba sa checkoutnut na branchu, ktoru chcete testovat.
Potom nainstalovat potrebne kniznice a nakoniec prichadza na rad samotne testovanie.