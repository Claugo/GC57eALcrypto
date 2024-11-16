Questo software è solo a titolo dimostrativo per mettere in evidenza la proprietà matematica GC57 sulla fattorizzazione di grandi semiprimi.
Il programma così com'è non funzionerà se non verranno create alcune cartelle contenenti i semiprimi e le chiavi di fattorizzazione. Se siete interessati fatene richiesta e fornirò tutti i dati di cui necessita il programma. Naturalmente tutto in modo gratuito.
Spiegazione del programma:
La criptazione dei dati avviene tramite un processo randint, e per questo motivo non viene ritenuto sicuro dai software di analisi, che però non tengono conto di un fattore importante e cioè la capacità di gestire numeri primi molto grandi in un tempo inferiore a un secondo.
Il programma utilizza la fattorizzazione GC57 prendendo, all'interno di file precedentemente creati e che contengono semiprimi di 8000 bit e oltre, un semiprimo a caso e lo fattorizza estraendo i due numeri primi.
Il numero primo "p" verrà diviso in pacchtti di 3 che daranno un seme pseudo casuale a randint. Il testo da criptare verrà diviso in caratteri e simboli e ogni carattere e simbolo trasformato in decimale.
Facciamo un esempio numerico: "a"=65, pacchetto estratto dal numero primo "p"=634, seed(634) x=65+634+randint(10000,30000). La nostra x avrà un valore di 5 cifre.
Dal numero primo "q" creiamo dei pacchetti di 5 cifre che ci restituiranno dei numeri pseudo casuali.
I numeri ricavati dal procedimento "p" e i numeri ricavati dal procedimento "q" verranno trasformati in bit e mantenuti tutti alla stessa lunghezza di 17 bit. 
Il passo successivo sarà quello di eseguire uno XOR tra questi due numeri e memorizzare il risultato in un file utilizzando JSON.

Questa è solo una piccola panoramica, ma come ho già accennato, il programma non vuole mettere in evidenza il metodo di criptazione ma quello del GC57 la cui proprietà di fattorizzazione è unica.
