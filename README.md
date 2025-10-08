# Egentliga Slut projekt med steam

[Data länk](https://www.kaggle.com/datasets/antonkozyriev/game-recommendations-on-steam/data)

## Data

Vi har 4 olika data filer:

- games.csv, innehåller information om spel på steam
- games_metadata.json, innehåller metadata gällande spelen, t.ex. tags
- users.csv, information om steam användare
- recommendations.csv, rekommandtioner från användare på steam

Vi borde kombinera games.csv med games_metadata.json för att lättare kunna ta tags och description. Sedan borde vi kombinera users.csv med recommendations.csv och lite trimma på fil storleken. Recommendations.csv är nästan 2 gb stor eller 41 miljoner rader och kan säkert skapa en väldigt bra rekommendationssystem men vi måste beakta att vi jobbar med inte så bra hårdvara och vi vill komma fram till resultat snabbare.

Users.csv har 14 miljoner användare/rader så vi kan bårt en hel del. Vi minskar mägnden till 1 000 och skapar bins för storlekar på 100.

#### Bins: 

(hur många reviews per användare, den tar t.ex. 100 users med reviews mellan 26-35, så här får vi en diverse user base med olika mängder reviews, utan att behöva använda 2gb fil)

(5, 15), (16, 25), (26, 35), (36, 45), (46, 55), (56, 65), (66, 75), (76, 85), (86, 95), (96, 120)

Efter att vi trimmat/slagit ihop filerna har vi dom här filerna i data katalogen:

- games_merged.csv
- users_real.csv
- recommendations_real.csv

## EDA

Vi analyserar och  utforskar vår data.

### Games.csv (games_merged.csv)

**OBS!!!** Vi satt redan ihop games.csv med games_metadata.json för att skapa en tydling och fylld csv fil

- 50872 unika spel
- 15 kolumner, t.ex. app_id, title, date_release mm.
- description kolumnen är den ända av alla data som har inga värde, vi ser till att beakta detta, antingen droppar vi dom eller fyller med något som passar. Spel med ingen description antaglien är inte så värst påbjudande till många

![alt text](/images/{20944469-4343-4D16-8FDD-91EF9501DD5F}.png)

### Users.csv (users_trimmed.csv)

**OBS!!!** Vi minska vår storlek på hur många users vi har, endast 1 000

- 1.4 miljoner användare i ursprungliga datan, 1 000 efter att vi trimmat
- 3 kolumner: user_id, products (hur många produkter man äger) och reviews (hur många recensioner man gjort)

![alt text](/images/{777AF8EE-22EC-493D-8A9C-1D4C9165E894}.png)

### Recommendations.csv (recommendations_trimmed.csv)

**OBS!!!** Vi trimmade ner vår data ner så att vi har 40 000 rekommendationer som finns för dom 1 000 användarna i users_trimmed.csv

- 40 000 rekommendationer/rader
- 9 kolumner, app_id

![alt text](/images/{8DA4F1BB-21A0-44A5-ADEB-EC861A99FBC8}.png)

### Visualiseringar

Det ända datasättet som kan utforskas bra visuellt är games.csv, users.csv har endast data i sig inget, intressant att visualisera. Samma med recommendations, data om rekommendationerna.

Jag blev inspirerad och tog många av [detta projekts exempel](https://www.kaggle.com/code/sohaibahmedbsds2021/game-recommendation-system) visualiserings exempel.

#### Antal spel utsläppta peer år

![Antal spel utsläppta peer år](/images/{CE8A3979-EBD9-4D27-9F4D-FE2C08DA9492}.png)

#### Spel per platform

![Spel per platform](/images/{C618106C-C738-4CE5-B2A0-E6494EF6E859}.png)

![Spel per platform utan steamdeck](/images/{A651FF16-79DD-4C71-9947-9FD6414DF30C}.png)

#### Distribution av spel betyg

![Distribution av spel betyg](/images/{4DFDDD0D-8E83-417C-A84D-610B1499B55F}.png)

#### Hur många reviews finns det per spel?



## Innehålls baserad rekommendationssystem

## Rekommendationssystem med Samarbetsbaserad filtrering

## Hybrid-Rekommendationssystem

## Evaluering och verifikation

## Analys och tankar