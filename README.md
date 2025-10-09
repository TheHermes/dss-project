# Spel Rekommendationssystem

I detta projekt utvecklas ett rekommendationsystem på basis av data från spel platformen Steam.

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

Jag bestämmer mig för att testa med två olika storleks data, en med 1 000 användare och en med 10 000 användare.

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

**OBS!!!** Vi trimmade ner vår data ner så att vi har 50 000 rekommendationer som finns för dom 1 000 användarna i users_trimmed.csv

- 50 000 rekommendationer/rader / 500 000 för 10 000 användare
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

Vi har implementerat ett innehållsbaserat system.

Vi uttnyttjar, spelets tittel och tags som finns i data. Vi håller båda, eftersom ett antal spel har inte tags så då kan vi rekommendera spel i samma franchise.

### Exempel körning

<details>

<summary>Visa</summary>

![Exempel 1](/images/{E4F68CBD-9F55-4AF1-96B2-7C2DA4ADE716}.png)

Dying Light 2 Stay Human har inga tags så systemet rekommenderar dlc för spelet, vilket är typiskt för steam att också gör.

![Exempel 2](/images/{4A053EE6-5F6D-4DC3-A56E-70C7FB75153A}.png)

Systemet dock är bristfälligt vi rekommenderar spel på basis av hur nära deras tittel + tags är varandra. Detta kan leda lätt till att vi rekommenderar endast spel som är i samma franchise eller dlc när man kanske vill se spel istället. Det blir klart och tydligt varför ett spel rekommenderas, eftersom om du tycker om Call of Duty så rekommenderar den liknande spel eller andra COD spel. Vi kan också redan börja rekommendera spel, ingen coldstart men de här systemet tar inte i beaktande användar partiskhet och åsikter, det kommer till näst.

</details>

## Rekommendationssystem med Samarbetsbaserad filtrering

Det finns ingen egentlig rating kolumn men vi har timmar som spelats och om användaren rekommenderar spelet. Vi kan kombinera dom två och räkna ut en rating på basis av:

$$
\text{score} = 0.7 \times \text{is-recommended} + 0.3 \times \text{hours-played}
$$

Varav score är ett tal mellan 0-1 desto större värde desto bättre rating. Vi sätter stor vikt på om användaren rekommenderar spelet och lite mindre på hur många timmar en har spelat. Här kan man säkert hitta ett bättre sätt att göra det här.

```Python
df["rating"] = (0.7 * df["is_recommended"]) + (0.3 * df["hours_normalized"])
```

Vårt system nu baserar rekommendationer på basis av vad användaren har tyckt om. Vi får då diverse spel och möjligen oförväntade spel som inte alls liknar vad en användare typiskt tycker om.

Nya användare dock kommer inte att kunna dra nytta av detta, eftersom det inte finns data att jämföra med. Vi har också ett problem med populäritets partiskhet, eftersom populära spel förekommer oftare i datan.

### Exempel Körning

<details>

<summary>Visa</summary>

#### 1 000 användar datan

![Exempel 1](/images/{60C83F4C-0378-40AF-AF4E-992175D6F2B0}.png)

#### 10 000 användar datan

![Exempel 2](/images/{4B2DDA3B-2774-4F33-B479-748A588B5ECA}.png)

</details>

## Hybrid-Rekommendationssystem

Gör först med perus content_based + collaborative

Sen kanske det som är här under:

Weighted Hybrid (Score Blending)

Combine the predicted scores from each model using weights:

final_score(u,i)= α × CF_score(u,i) + (1−α) × CB_score(i)

where:

CF_score(u,i) = how much the collaborative model thinks user u will like game i

CB_score(i) = how similar the game is to what they’ve already liked

α controls the balance (e.g. 0.7 CF / 0.3 CB)

## Evaluering och verifikation

Precision@k, coverage och novelty

## Analys och tankar
