# ASSESSMENT.md

## Aanspreken

Ik ben erg trots op de functie `show_fitnesschema` in app.py vanwege de efficiëntie ervan. Deze functie haalt gegevens op over een fitnesschema op basis van het meegegeven ID en structureert deze gegevens op een overzichtelijke manier. Eerst wist ik niet hoe ik deze functie zou aanpakken, maar toen viel het mij op dat de ID eigenlijk ook getallen zijn. Waarom verwijs ik niet daarnaar? Daarnaast maakt deze functie ook gebruik van hulpfuncties zoals `get_exercises_by_section_and_day`, `get_all_sets``, en `get_sets`` om de code modulair te houden en de functionaliteit beter te organiseren. Ik wilde niet dat de code te lang zou worden, dus heb ik hulpfuncties gebruikt. In deze functie heb ik ook aandacht besteed aan de opmaak van de data. Met behulp van hulpfuncties worden de oefeningen en instructies beter weergegeven in het fitnesschema.

Ik ben ook erg trots op de fitnesschema.html pagina. De informatie op de pagina is gestructureerd. Het gebruik van CSS-styling geeft de pagina een professionele uitstraling. Daarnaast zijn de tabellen duidelijk en goed georganiseerd, wat bijdraagt aan de visuele aantrekkelijkheid van de pagina. Het vele gebruik van Jinja2-sjablonen om de gegevens van het fitnesschema te genereren, heeft hier ook aan bijgedragen. Ik ben ook blij met de gedetailleerde informatie over het fitnesschema, waaronder oefeningen, sets, instructies, en overwegingen, die ik ook heb kunnen laten zien.

Ik ben ook trots op mijn fitnesschema_form.html en mijn `fitnesschema_form` functie in app.py. Ik ben super tevreden over de lay-out van die HTML-pagina. Het script werkt goed met het selecteren van bullet points. Ik heb echt heel veel tijd aan deze pagina besteed. De functie heb ik gelukkig simpeler gekregen. Ik wilde eerst met CSV-bestanden werken, maar dat was gewoon overbodige code, omdat ik direct met de antwoorden van de request kon beginnen.

## Beslissingen

## In Fitnesschema_form

*Beslissing 1*

#### Python code 

```bash
#Check if the fitnesschema is already in the profile
        fitnesschema_in_profile = Fitnesschema.query.filter(
            Fitnesschema.id == schema_id,
            Fitnesschema.profiles.any(id=profile.id)
        ).first()
```
#### Models.py
```bash
# Intermediate class for the many-to-many relationship between Profile and Fitnesschema
profile_fitnesschema_association = db.Table('profile_fitnesschema_association',
    db.Column('profile_id', db.Integer, db.ForeignKey('profiles.id')),
    db.Column('fitnesschema_id', db.Integer, db.ForeignKey('fitnesschemas.id'))

class Profile(db.Model):
    """Stores user profile information."""
    __tablename__ = "profiles" 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100))
    age = db.Column(db.String(10))
    weight = db.Column(db.String(10))
    height = db.Column(db.String(10))
    experience_level = db.Column(db.String(50))
    goal = db.Column(db.String(50))
    goal_string = db.Column(db.String(100))
    user = db.relationship("User", back_populates="profile")
    fitnesschemas = db.relationship('Fitnesschema', secondary='profile_fitnesschema_association', back_populates='profiles')
)
```
1. Waarom heb je de beslissing genomen?
Ik heb besloten om een many-to-many relatie te maken tussen de tabel 'profiel' en 'fitnesschema'. Dit besluit kwam voort uit eerdere fouten die ik tegenkwam toen ik probeerde de tabel 'profiel' en 'fitnesschema' rechtstreeks aan elkaar te koppelen. Door een many-to-many relatie te creëren, kon ik een flexibeler en schaalbaarder gegevensmodel ontwikkelen, waardoor gebruikers meerdere fitnesschema's aan één profiel konden koppelen en vice versa.
2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Het vorige ontwerpidee om een aparte tabel 'user_sportschema' aan te maken die 'profiel_id' en 'fitnesschema_id' combineerde, bleek niet zo handig te zijn. Dit ontwerp leidde tot complexiteit en beperkingen in het beheren van gegevens, omdat het niet mogelijk was om gemakkelijk meerdere fitnesschema's aan één profiel te koppelen, of om een enkel fitnesschema aan meerdere profielen toe te wijzen. Dit ontwerp beperkte de flexibiliteit van het gegevensmodel en zorgde voor problemen bij het beheren van relaties tussen profielen en fitnesschema's.
3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing met een many-to-many relatie tussen 'profiel' en 'fitnesschema' is beter omdat het een flexibeler gegevensmodel biedt. Het stelt gebruikers in staat om meerdere fitnesschema's aan één profiel te koppelen en maakt het mogelijk om een enkel fitnesschema aan meerdere profielen toe te wijzen, waardoor de functionaliteit van het systeem wordt verbeterd. Nu het project is afgelopen, blijft deze benadering beter omdat het gegevensmodel goed is ontworpen en het systeem soepel blijft werken zonder de beperkingen van het vorige ontwerp.

*Beslissing 2*
#### html code 
```html
<div class="fitness-form">
    <div class="fitness-form_box" id="fitness-form_box1"></div>
</div>
```
### css code:
```css
#fitness-form {
    max-width: 500px;
    text-align: left;
    padding: 20px;
    border: 3px solid rgb(247, 103, 74);
    padding: 20px;
    border-radius: 10px;
    background-color: #8fcfef;
    color: rgb(37, 34, 34);
}

#fitness-form .input-element {
    margin-bottom: 20px;
}

.fitness-form {
    display: flex;
    height: 120vh;
    justify-content: center;
    margin-left: auto;
    margin-right: auto;
    max-width: 800px;
}

.fitness-form_box {
    width: 600px;
    height: 118vh;
    font-size: 1em;
    text-align: center;
    border-radius: 15px;
}

#fitness-form_box1 {
    padding: 20px;
    margin: 20px;
    overflow: hidden;
}
```
1. Waarom heb je de beslissing genomen?
Ik heb besloten om CSS Flexbox te gebruiken op bijna elke html pagina van mijn project, inclusief de `fitnesschema_form`, vanwege de verbetering van de layout van mijn HTML-pagina's. Met de complexiteit van een navbar en een sidebar op mijn pagina's moest ik een methode vinden om ervoor te zorgen dat de rest van de layout goed werd verwerkt. CSS Flexbox bood de mogelijkheid om elementen flexibel te positioneren en te ordenen, waardoor een betere en meer responsieve layout mogelijk was.
2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Het vorige ontwerpidee om de fitnesschema_form op de HTML-pagina te krijgen, bleek niet effectief te zijn. Ondanks pogingen om de form naar links te schuiven door het toevoegen van CSS-regels, zoals marge en padding, resulteerde dit niet in de gewenste oplossing. De form bleef samenvallen met de sidebar, wat leidde tot problemen met de lay-out en de algehele gebruikerservaring.
3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing, het gebruik van CSS Flexbox, was beter omdat het een meer flexibele en responsieve lay-out mogelijk maakte. Door gebruik te maken van Flexbox kon ik elementen op een voorspelbare en gecontroleerde manier rangschikken, waardoor problemen met overlapping en uitlijning werden opgelost. Het gebruik van Flexbox heeft geleid tot een betere gebruikerservaring en heeft het gemakkelijker gemaakt om de lay-out aan te passen aan eventuele wijzigingen in de toekomst.


*Beslissing 3*

### Javascript

 ```javascriptcode 
 <script>
                function showQuestions() {
                    const form = document.getElementById('fitness-form');
                    const goal = form.querySelector('input[name="goal"]:checked');
                    const level = form.querySelector('input[name="level"]:checked');
                    const krachtOef = form.querySelector('input[name="krachtOef"]:checked');
                    const cardioOef = form.querySelector('input[name="cardioOef"]:checked');
                    const krachtQuestions = document.getElementById('krachtQuestions');
                    const krachtQuestions1 = document.getElementById('krachtQuestions1');
                    const krachtQuestions2 = document.getElementById('krachtQuestions2');
                    const krachtQuestions3 = document.getElementById('krachtQuestions3');
                    const krachtQuestions4 = document.getElementById('krachtQuestions4');
                    const schemaQuestions = document.getElementById('schemaQuestions');
                    const daysQuestion = document.getElementById('daysQuestion');
                    const dropdown = document.getElementById('dropdown');
                    const days = form.querySelector('select[name="days"]').value;
                    const schemas = document.getElementById('schemas');

                    // Modify krachtOef-menu based on the goal
                    if (goal && goal.value === 'Conditie') {
                        krachtQuestions.style.display = 'block';
                        krachtQuestions1.style.display = 'none';
                        krachtQuestions2.style.display = 'none';
                        krachtQuestions3.style.display = 'none';
                        krachtQuestions4.style.display = 'block';
                    } else if (goal && (goal.value === 'Kracht' || goal.value === 'Spieropbouw')) {
                        krachtQuestions.style.display = 'block';
                        krachtQuestions1.style.display = 'block';
                        krachtQuestions2.style.display = 'block';
                        krachtQuestions3.style.display = 'block';
                        krachtQuestions4.style.display = 'none';
                    } else {
                        krachtQuestions.style.display = 'none';
                    }

                    // Check if all questions 1 to 4 are filled in
                    if (goal && level && cardioOef) {
                        schemaQuestions.style.display = 'block';
                    } else {
                        schemaQuestions.style.display = 'none';
                    }
                    
                    // Get the selected value from the dropdown
                    let selectedValue = dropdown.value;
                    let selectedSchema = schemas.value; 

                    // Modify the dropdown menu based on goal and level.
                    if (goal.value === 'Kracht') {
                        if (level.value === 'Beginner') {
                            dropdown.innerHTML = `
                                <option value="1">1</option>
                                <option value="2">2</option>`;
                        } else if (level.value === 'Semi-gevorderd') {
                            dropdown.innerHTML = `
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>`;
                        }
                    } else if (goal.value === 'Spieropbouw') {
                        if (level.value === 'Beginner') {
                            dropdown.innerHTML = `
                                <option value="1">1</option>
                                <option value="2">2</option>`;
                        } else if (level.value === 'Semi-gevorderd') {
                            dropdown.innerHTML = `
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>`;
                        } 
                    } else if (goal.value === 'Conditie') {
                        if (level.value === 'Beginner') {
                            dropdown.innerHTML = `
                                <option value="1">1</option>
                                <option value="2">2</option>
                                <option value="3">3</option>`;
                        } else if (level.value === 'Semi-gevorderd') {
                            dropdown.innerHTML = `
                                <option value="2">2</option>
                                <option value="3">3</option>
                                <option value="4">4</option>`;
                            } 
                    }

                    // Set the dropdown value to the selected value
                    dropdown.value = selectedValue; 

                    // Modify the dropdown menu based on goal and level for training schedule
                    if ( goal && level && days) {
                        if (goal.value === 'Conditie' && (level.value === 'Beginner' || level.value === 'Semi-gevorderd')) {
                            schemas.innerHTML = `
                                <option value="Geen optie">Geen optie</option>`;
                        }
                        else if ((goal.value === 'Kracht' || goal.value === 'Spieropbouw') && level.value === 'Beginner') {
                            schemas.innerHTML = `
                                <option value="Full body">Full body</option>`;
                        }
                        else if ((goal.value === 'Kracht' || goal.value === 'Spieropbouw') && level.value === 'Semi-gevorderd' && dropdown.value === "2") {
                            schemas.innerHTML = `
                                <option value="Full body">Full body</option>
                                <option value="Upper body en lower body">Upper body en lower body</option>`;
                        }
                        else if ((goal.value === 'Kracht' || goal.value === 'Spieropbouw') && level.value === 'Semi-gevorderd' && dropdown.value === "3") {
                            schemas.innerHTML = `
                                <option value="Full body">Full body</option>
                                <option value="Splitschema">Splitschema</option>
                                <option value="Push/pull/legsschema">Push/pull/legsschema</option>`;
                        }
                        else if ((goal.value === 'Kracht' || goal.value === 'Spieropbouw') && level.value === 'Semi-gevorderd' && dropdown.value === "4") {
                            schemas.innerHTML = `
                                <option value="Full body">Full body</option>
                                <option value="Upper body en lower body">Upper body en lower body</option>`;
                        }
                    }

                    // Set the value of schemas to the selected schema
                    schemas.value = selectedSchema;
                }

                // Add event listeners for dropdown and schemas on DOMContentLoaded event
                document.addEventListener('DOMContentLoaded', () => {
                    document.getElementById('dropdown').addEventListener('change', showQuestions);
                    document.getElementById('schemas').addEventListener('change', showQuestions);
                });
            </script>
```
1. Waarom heb je de beslissing genomen?
De beslissing om de showQuestions-functie te implementeren werd genomen om de gebruikerservaring te verbeteren door alleen relevante vragen weer te geven op basis van de keuzes die de gebruiker maakt in het formulier. Hierdoor wordt voorkomen dat de gebruiker wordt overweldigd door te veel informatie en wordt het proces gestroomlijnd, met als resultaat dat de juiste schema's worden gecreëerd op basis van de gekozen opties.
2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Vóór het implementeren van de showQuestions-functie, werden alle vragen standaard weergegeven op het formulier, ongeacht de keuzes van de gebruiker. Dit maakte het formulier onnodig lang en verwarrend voor de gebruiker, omdat ze door alle vragen moesten bladeren, zelfs als sommige niet relevant waren voor hun situatie.
3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing, geïmplementeerd met de showQuestions-functie, is beter omdat het de gebruikerservaring verbetert door alleen relevante vragen te tonen op basis van de keuzes van de gebruiker. Dit maakt het invullen van het formulier sneller en gemakkelijker voor de gebruiker. Deze benadering blijft beter, zelfs nadat het project is afgerond, omdat het de basis legt voor een gebruiksvriendelijke interface die gemakkelijk kan worden aangepast en uitgebreid in de toekomst.

*Beslissing 4*
```javascriptcode
// Get the selected value from the dropdown
                    let selectedValue = dropdown.value;
                    let selectedSchema = schemas.value; 
// Set the dropdown value to the selected value
                    dropdown.value = selectedValue; 
// Set the value of schemas to the selected schema
                    schemas.value = selectedSchema;
```
1. Waarom heb je de beslissing genomen?
De beslissing om de geselecteerde waarden van de dropdown-menu's op te halen en op te slaan, werd genomen om ervoor te zorgen dat deze waarden beschikbaar blijven voor verdere verwerking in de functie. Hierdoor kunnen we later in de code gemakkelijk toegang krijgen tot de geselecteerde waarden zonder deze opnieuw te hoeven ophalen.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Voorheen werden de geselecteerde waarden niet expliciet vastgelegd en opgeslagen in variabelen. Dit betekende dat telkens wanneer we de waarde nodig hadden, we opnieuw naar de HTML-structuur moesten gaan om deze op te halen. Dit kan inefficiënt zijn en leiden tot onnodige manipulatie van de HTML-structuur.
3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing is beter omdat het de efficiëntie verbetert door de geselecteerde waarden van de dropdown-menu's slechts één keer op te halen en op te slaan voor later gebruik. Vroeger werden de dropdown-menu's niet automatisch bijgewerkt op basis van de ingevulde keuzes van de gebruiker, wat het gebruik van de applicatie minder intuïtief en toegankelijk maakt. Met de nieuwe aanpak kan de dropdown-menu's dynamisch bijwerken op basis van de interacties van de gebruiker, waardoor de toegankelijkheid aanzienlijk wordt verbeterd.

*Beslissing 5*
```javascriptcode 
 // Add event listeners for dropdown and schemas on DOMContentLoaded event
                document.addEventListener('DOMContentLoaded', () => {
                    document.getElementById('dropdown').addEventListener('change', showQuestions);
                    document.getElementById('schemas').addEventListener('change', showQuestions);
                });
```
1. Waarom heb je de beslissing genomen?
De beslissing om luisteraars toe te voegen aan de dropdown-menu's werd genomen om ervoor te zorgen dat de showQuestions-functie wordt uitgevoerd telkens wanneer de gebruiker een keuze maakt in een van de dropdown-menu's. Dit zorgt ervoor dat de vragen dynamisch worden bijgewerkt op basis van de gemaakte keuzes, waardoor een interactieve gebruikerservaring wordt gecreëerd.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Zonder luisteraars toe te voegen aan de dropdown-menu's, zou de showQuestions-functie alleen worden uitgevoerd wanneer de pagina voor het eerst wordt geladen. Dit betekent dat de vragen niet zouden worden bijgewerkt op basis van latere keuzes van de gebruiker, hierdoor werden dan niet alle antwoorden weergeven.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing is beter omdat het zorgt voor een dynamische en interactieve gebruikerservaring, waarbij de vragen in realtime worden bijgewerkt op basis van de keuzes van de gebruiker. Dit verbetert de bruikbaarheid van de applicatie en maakt het gemakkelijker voor gebruikers om het gewenste fitnessschema te genereren. Deze aanpak blijft beter, omdat anders de form niet goed kan worden ingevuld door de gebruiker.

## In fitnesschema

*Beslissing 6*
### python code 

```bash
for day in range(1, fitnesschema.number_of_days + 1):
        warming_up_exercises[day] = get_exercises_by_section_and_day(id, 'warming_up', day)
        stretching_exercises[day] = get_exercises_by_section_and_day(id, 'stretching', day)
        strength_training_exercises[day] = get_exercises_by_section_and_day(id, 'strength_training', day)
        cardio_exercises[day] = get_exercises_by_section_and_day(id, 'cardio', day)
        cooling_down_exercises[day] = get_exercises_by_section_and_day(id, 'cooling_down', day)
```
1. Waarom heb je de beslissing genomen?
Ik wilde eerst elke dag apart behandelen omdat het mij hielp dingen netjes te houden. Maar toen realiseerden ik dat dit veel herhaling in de code zou veroorzaken. Dus heb ik ervoor gekozen om alles in één loop te zetten, wat de code eenvoudiger maakt. 
2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Het idee om per dag een aparte functie te schrijven, zou mogelijk hebben geleid tot redundantie in de code. Het zou complexer kunnen zijn geweest om wijzigingen aan te brengen die van toepassing zijn op alle functies, omdat elke functie individueel zou moeten worden bijgewerkt. Dit zou ook de leesbaarheid van de code hebben vermindert, omdat er veel vergelijkbare functies zouden zijn met mogelijk kleine variaties.
3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De beslissing om één lus te gebruiken om alle oefeningen voor alle dagen op te halen en te verwerken, biedt een meer gestroomlijnde en efficiënte benadering. Het vermindert redundantie en maakt de code gemakkelijker te onderhouden. Door de oefeningen op deze manier te verwerken, blijft de code overzichtelijk en gemakkelijk te begrijpen, zelfs na de afronding van het project. Dit maakt het gemakkelijker om eventuele toekomstige wijzigingen aan te brengen of problemen op te lossen.

*Beslissing 7*
```bash
def format_instructions(instructions):
    """Format the instructions to remove braces and split by comma."""
    # Check if instructions are a list containing a single string
    if isinstance(instructions, list) and len(instructions) == 1 and isinstance(instructions[0], str):
        # Extract the string from the list
        instructions = instructions[0]

    # Remove quotes at the beginning and end of the string
    instructions = instructions.strip('"')

    # Remove braces
    instructions = instructions.replace('{', '').replace('}', '')

    # Replace "," with an HTML line break
    instructions = instructions.replace('","', '<br>')
    return instructions
```
1. Waarom heb je de beslissing genomen?
Ik heb ervoor gekozen om een functie te schrijven om de instructies te formatteren, omdat de instructies in een lijst stonden in plaats van als een normale string. Dit maakte het lastig om ze goed weer te geven. Door een speciale functie te maken, kon ik ervoor zorgen dat alle instructies correct werden opgemaakt voor weergave.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
In het verleden, voordat ik deze speciale functie had gemaakt, werden een overschot aan aanhalingstekens en komma's weergeven. Dit maakte het lastig om de informatie goed te tonen aan de gebruiker en zorgde voor verwarring.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing met de speciale functie voor het formatteren van instructies heeft het gemakkelijker gemaakt om alle instructies correct weer te geven. Dit heeft bijgedragen aan een betere gebruikerservaring en zorgt ervoor dat de code er netter uit ziet. 

*Beslissing 8*
### html code 
```html
{% for day in range(1, fitnesschema.number_of_days + 1) %}
                        <table border="1px" width="90%" class="table1">
                            <thead>
                                <tr>
                                    <td colspan="3" style="text-align: center;">Dag {{ day }}</td>
                                </tr>
                            </thead>
                            <tr>
                                <td colspan="3"></td>
                                
                            </tr>
                            <thead>
                                <tr>
                                    <td colspan="3" style="text-align: center;">{{ fitnesschema.level }} &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; {{ fitnesschema.goal }} </td>
                                </tr>
                            </thead>
                            <tr>
                                <td colspan="3"></td>
                                
                            </tr>
                            <tbody>
                                <tr>
                                    <th style="width: 100px;"> </th>
                                    <th style="width: 150px; text-align: center; font-size: 1.2em; font-weight: bold;">Oefeningen</th>
                                    <th style="width: 200px; text-align: center; font-size: 1.2em; font-weight: bold;">Aantal sets</th>
                                    
                                </tr>
                                <tr>
                                    <td style="text-align: center; font-size: 1.2em; font-weight: bold;">Warming_up</td>
                                    <td style="text-align: left";>
                                        <ul>
                                            {% for exercise in warming_up_exercises[day] %}
                                                <li>{{ exercise.name }}</li>
                                            {% endfor %}
                                        </ul>
                                    </td>
                                    <td>
                                        {{ sets.warming_up_sets }}
                                    </td>
```
1. Waarom heb je de beslissing genomen?
De beslissing om één tabel per dag te gebruiken voor het genereren van fitnesschema's werd genomen vanwege de behoefte aan efficiëntie en consistentie in de gebruikerservaring. Door één tabel te gebruiken die dynamisch wordt ingevuld binnen een loop, wordt het proces gestroomlijnd en worden herhaalde codefragmenten vermeden. 

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Het oorspronkelijke idee om voor elke dag een aparte tabel te maken, zou hebben geleid tot redundantie en complexiteit. Het zou moeilijk zijn geweest om consistentie te handhaven tussen de tabellen en om wijzigingen door te voeren die van toepassing zijn op alle tabellen. Dit zou resulteren in inefficiënte code en een minder intuïtieve gebruikerservaring.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing met één dynamisch gegenereerde tabel per dag biedt een gestroomlijnde en consistente gebruikerservaring. Door de code te optimaliseren en te vereenvoudigen, wordt het onderhoud van de applicatie vergemakkelijkt en blijft de codebase overzichtelijk en gemakkelijk te begrijpen. Deze aanpak verbetert nog steeds de schaalbaarheid en onderhoudbaarheid van de applicatie, zelfs na afronding van het project.

## profiel
*Beslissing 9*
### python code 
```bash
if existing_profile:
                for key, value in profile_data.items():
                    # Update only if there's a new value
                    if value:
                        setattr(existing_profile, key, value)
                db.session.commit()
                flash("Profiel succesvol bijgewerkt!", "success")
```
1. Waarom heb je de beslissing genomen?
Ik heb de beslissing genomen om ervoor te zorgen dat alleen de gegevens die zijn ingevuld, worden gewijzigd, zodat gebruikers niet per ongeluk bestaande informatie overschrijven met lege waarden. Dit verbetert de nauwkeurigheid van het profiel en voorkomt dat waardevolle gegevens verloren gaan.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
De vorige ontwerpideeën zouden alle waarden in het profiel kunnen bijwerken, zelfs als sommige invoervelden leeg zijn gebleven. Dit zou ertoe kunnen leiden dat bestaande gegevens onbedoeld worden overschreven met lege of onvolledige waarden, wat frustrerend zou zijn voor de gebruiker en de integriteit van de gegevens zou kunnen schaden.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing is beter omdat deze ervoor zorgt dat alleen de gegevens die daadwerkelijk zijn ingevoerd door de gebruiker worden bijgewerkt, waardoor de kans op onbedoeld gegevensverlies wordt verminderd. Dit maakt de applicatie gebruiksvriendelijker en betrouwbaarder. Ook na voltooiing van het project blijft deze aanpak beter, omdat het de nauwkeurigheid en integriteit van de gebruikersprofielen behoudt, wat cruciaal is voor een duurzame en betrouwbare applicatie.


*Beslissing 10*
### html code 
```html
<div class="profile-box" id="profile-box3">
            <h2 class="mt-5">Fitnesschemas</h2>
            <ul class="list-group">
                {% if profile.fitnesschemas %}
                    {% for fitnesschema in profile.fitnesschemas %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        <a href="{{ url_for('show_fitnesschema', id=fitnesschema.id) }}">Fitnesschema {{ fitnesschema.id }}</a>
                        <form action="{{ url_for('delete_fitnesschema', id=fitnesschema.id) }}" method="POST" style="display:inline;">
                            <button type="submit" class="btn btn-sm btn-danger">Verwijder</button>
                        </form>
                    </li>
                    {% endfor %}
                {% else %}
                    <li class="list-group-item">Geen fitnesschema's gevonden</li>
                {% endif %}
            </ul>
        </div>
```
1. Waarom heb je de beslissing genomen?
De beslissing om elke fitnessschema een verwijderknop en een link te geven om naar het schema te navigeren, werd genomen om de gebruikerservaring te verbeteren door gebruikers eenvoudig beheer en toegang tot hun fitnessschema's te bieden. Dit zorgt ervoor dat gebruikers ongewenste schema's snel kunnen verwijderen en gemakkelijk naar specifieke schema's kunnen navigeren voor verdere details of aanpassingen.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Bij de vorige ontwerpideeën ontbraken de expliciete verwijderknoppen en navigatielinks. Dit betekende dat gebruikers een omslachtige en tijdrovende procedure moesten volgen om een schema te verwijderen of te bekijken, wat de efficiëntie en gebruiksvriendelijkheid van de applicatie aanzienlijk verminderde. Gebruikers moesten mogelijk door meerdere pagina's of menu's navigeren, wat verwarrend en frustrerend kon zijn.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing is beter omdat het de gebruiksvriendelijkheid en efficiëntie aanzienlijk verbetert. Door elke fitnessschema een verwijderknop en een directe link te geven, kunnen gebruikers snel en eenvoudig ongewenste schema's verwijderen en direct naar het gewenste schema navigeren. Dit maakt de applicatie intuïtiever en minder tijdrovend om te gebruiken.

## index
*Beslissing 11*
### html code 
```html
{% block flash_messages %}{% endblock %}

{% block sidebar %}

    {% if get_flashed_messages() %}
    <div class="alert alert-primary mb-0 text-center" role="alert">
        {{ get_flashed_messages() | join(" ") }}
    </div>
    {% endif %}
```
1. Waarom heb je de beslissing genomen?
De beslissing om de Flask-berichten standaard in de layout op de juiste plek weer te geven, werd genomen om de gebruikerservaring te verbeteren door ervoor te zorgen dat belangrijke feedbackberichten altijd zichtbaar en goed gepositioneerd zijn. Dit helpt gebruikers om direct relevante informatie te zien, zoals bevestigingen van acties, foutmeldingen of waarschuwingen.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Bij de vorige ontwerpideeën werden de Flask-berichten mogelijk niet consistent of op een logische plek weergegeven. Dit kon leiden tot verwarring bij de gebruiker, omdat berichten niet altijd zichtbaar waren of op onverwachte plaatsen verschenen. Dit maakte het moeilijker voor gebruikers om de applicatie te navigeren en te begrijpen welke acties succesvol waren of welke fouten er optraden.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing is beter omdat het zorgt voor een consistente en intuïtieve weergave van belangrijke berichten, waardoor gebruikers direct feedback krijgen over hun acties. Door de berichten standaard op een vaste plek in de layout weer te geven, wordt de kans geminimaliseerd dat gebruikers belangrijke informatie missen. 



## import1.py
*Beslissing 12*
```bash
def import_csv_to_db(csv_file):
    with open(csv_file, newline='') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip the header row if necessary

        for row in reader:
            goal, level, kracht_oef, cardio_oef, days_per_week, schema, warming_up, stretching, strength_training, cardio, cooling_down = row
            
            # Create a new Fitnesschema record
            fitnesschema = Fitnesschema(
                goal=goal,
                level=level,
                kracht_oef=kracht_oef,
                cardio_oef=cardio_oef,
                number_of_days=int(days_per_week),
                type_of_schedule=schema,
                warming_up=warming_up if warming_up else None,
                stretching=stretching if stretching else None,
                strength_training=strength_training if strength_training else None,
                cardio=cardio if cardio else None,
                cooling_down=cooling_down if cooling_down else None
            )
            db.session.add(fitnesschema)
            db.session.commit()  # Commit so the fitnesschema gets an ID

            # Add exercises to the correct sections
            sections = {
                'warming_up': warming_up,
                'stretching': stretching,
                'strength_training': strength_training,
                'cardio': cardio,
                'cooling_down': cooling_down
            }
            
            for section_name, exercises_per_day in sections.items():
                if exercises_per_day:
                    days_exercises = exercises_per_day.split(') (')
                    days_exercises = [day.strip('() ') for day in days_exercises]  # Remove parentheses and spaces

                    for day, exercise_ids in enumerate(days_exercises, start=1):
                        exercise_ids_list = [
                            int(ex_id.strip()) for ex_id in exercise_ids.split(',') if ex_id.strip().isdigit()
                        ]
                        
                        for order, exercise_id in enumerate(exercise_ids_list):
                            exercise_order = FitnesschemaExerciseOrder(
                                sportschema_id=fitnesschema.id,
                                section_name=section_name,
                                exercise_id=exercise_id,
                                exercise_order=order,
                                day=day
                            )
                            db.session.add(exercise_order)

            db.session.commit()
```
1. Waarom heb je de beslissing genomen?
De beslissing om informatie uit een CSV-bestand in twee tabellen te verdelen werd genomen om de gegevens in de eerste tabel (het fitnessschema) ordelijker en overzichtelijker weer te geven. Door de gegevens te splitsen, kunnen specifieke details gescheiden worden weergegeven, waardoor de hoofdgegevens gemakkelijker te interpreteren en te beheren zijn.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Bij de vorige ontwerpideeën werden alle gegevens in één enkele tabel geplaatst, wat leidde tot een rommelige en onoverzichtelijke presentatie. Dit maakte het moeilijk om snel relevante informatie te vinden en kon verwarring veroorzaken door de hoeveelheid informatie die in één tabel werd weergegeven. Dit verminderde de leesbaarheid van de applicatie.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing is beter omdat het de gegevens opsplitst in twee tabellen, waardoor de hoofdgegevens (zoals de fitnessschema's) gescheiden worden van aanvullende informatie. Dit verbetert de leesbaarheid en zorgt voor een meer gestructureerde en georganiseerde weergave. Gebruikers kunnen sneller en efficiënter de informatie vinden die ze nodig hebben, wat de algehele gebruikerservaring verbetert.

## models.py
*Beslissing 13*
```bash
class Sets(db.Model):
    """Stores sets information."""
    __tablename__ = "sets"
    id = db.Column(db.Integer, primary_key=True)
    goal = db.Column(db.String, nullable=False)
    level = db.Column(db.String, nullable=False)
    warming_up_sets = db.Column(db.String, nullable=True)
    stretching_sets = db.Column(db.String, nullable=True)
    strength_training_sets = db.Column(db.String, nullable=True)
    cardio_sets = db.Column(db.String, nullable=True)
    cooling_down_sets = db.Column(db.String, nullable=True)
    considerations = db.Column(db.String, nullable=False)


    def __init__(self, goal, level, considerations, warming_up_sets=None, stretching_sets=None, strength_training_sets=None, cardio_sets=None, cooling_down_sets=None):
        self.goal = goal
        self.level = level
        self.warming_up_sets = warming_up_sets
        self.stretching_sets = stretching_sets
        self.strength_training_sets = strength_training_sets
        self.cardio_sets = cardio_sets
        self.cooling_down_sets = cooling_down_sets
        self.considerations = considerations 
```
1. Waarom heb je de beslissing genomen?
De beslissing om een __init__-methode te implementeren in de Sets-klasse is genomen om zowel verplichte als optionele velden op een gestructureerde manier te initialiseren. Hierdoor kunnen sommige kolommen leeg blijven als er geen gegevens voor beschikbaar zijn, terwijl de verplichte velden altijd worden ingevuld. Dit zorgt voor flexibiliteit bij het creëren van objecten van de Sets-klasse.

2. Wat was er niet zo handig aan de vorige ontwerpideeën?
Bij eerdere ontwerpideeën zonder de __init__-methode zou het instellen van optionele velden omslachtig en foutgevoelig zijn. Zonder een constructor zou je handmatig elke eigenschap moeten instellen, inclusief controle op optionele velden, wat tot onnodige complexiteit en mogelijke fouten zou kunnen leiden.

3. Waarom is de nieuwe oplossing beter (en is het nog steeds beter, nu je project is afgelopen?)
De nieuwe oplossing met de __init__-methode is beter omdat het het proces vereenvoudigt en duidelijker maakt. Door optionele parameters met standaardwaarden (None) te voorzien, kan de __init__-methode lege kolommen opvangen zonder extra code.
