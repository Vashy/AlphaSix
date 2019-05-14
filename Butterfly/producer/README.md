# Producer

Il Producer è il componente che resta in ascolto degli webhook provenienti dal suo applicativo specifico (e.g. Redmine, GitLab). Ha lo scopo di immettere i messaggi su Kafka in formato JSON, conservando solo i campi di interesse e aggiungendone eventualmente di propri.

Prima di lanciare un Producer bisogna configurare l'ambiente di [Butterfly](https://github.com/Vashy/AlphaSix/blob/master/README.md).


## GitLab Producer

Il Producer di GitLab si occupa di ascoltare gli webhook provenienti dai progetti di GitLab che hanno configurato la porta relativa al componente, e di immettere nella coda "gitlab" di Kafka i messaggi.

## Redmine Producer

Il Producer di Redmine si occupa di ascoltare gli webhook provenienti dai progetti di Redmine che hanno configurato la porta relativa al componente, e di immettere nella coda "redmine" di Kafka i messaggi.
