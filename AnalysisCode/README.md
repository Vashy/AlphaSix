PER SONARQUBE

Scaricare e unzippare:

	https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-6.7.6.zip

Dare da terminale il percorso fino a sonar.sh seguito dal comando start, ad esempio:

    $ /home/laura/Downloads/sonarqube-6.7.6/bin/linux-x86-64/sonar.sh start

(dovrebbe dare Started SonarQube.)

Andare da browser su localhost:9000 e accedere con utente admin password admin

Scaricare e unzippare:
	https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-3.3.0.1492-linux.zip

e mettere questa cartella in AnalysisCode al posto della cartella incompleta con lo stesso nome.

Posizionarsi nella cartella AnalysisCode e dare il comando:

    $ sonar-scanner-cli-3.3.0.1492-linux/sonar-scanner-3.3.0.1492-linux/bin/sonar-scanner

Ora su localhost:9000, nella sezione projects, è possibile vedere il progetto Butterfly.
