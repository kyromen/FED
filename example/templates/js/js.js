
function createObjects() {
    var ul_events=document.getElementById('events');
    var ul_cinemas=document.getElementById('cinemas');
    var child;

    // clear events/cinemas
    while(child = ul_cinemas.firstChild ) ul_cinemas.removeChild(child)
    while(child = ul_events.firstChild ) ul_events.removeChild(child)

    var li, name, br, div;
    var img_place, img_price, img_time;

    for (var i=eventInd; i<eventInd+5 && i<eventsData.length; i++)
    {
        li=document.createElement('li');
        ul_events.appendChild(li);

        name=document.createElement('a');
        name.appendChild(document.createTextNode(eventsData[i].name.slice(0, 35)))
        name.href = eventsData[i].href
        li.appendChild(name);

        br=document.createElement('br');
        li.appendChild(br);

        img_place=document.createElement('img');
        img_place.src = "templates/images/place.png"
        li.appendChild(img_place);

        div=document.createElement('div');
        div.appendChild(document.createTextNode(eventsData[i].place.slice(0, 35)))
        li.appendChild(div);

        if (eventsData[i].price != "") {
            img_price=document.createElement('img');
            img_price.src = "templates/images/images.jpg"
            li.appendChild(img_price);

            div=document.createElement('div');
            div.appendChild(document.createTextNode(eventsData[i].price))
            li.appendChild(div);
        }

        if (eventsData[i].time != "") {
            img_time=document.createElement('img');
            img_time.src = "templates/images/time.png"
            li.appendChild(img_time);

            div=document.createElement('div');
            div.appendChild(document.createTextNode(eventsData[i].time))
            li.appendChild(div);
        }
    }

    for (var i=cinemaInd; i<cinemaInd+11 && i<cinemasData.length; i++)
    {
        var li=document.createElement('li');
        ul_cinemas.appendChild(li);

        var name=document.createElement('a');
        name.appendChild(document.createTextNode(cinemasData[i].name.slice(0, 35)))
        name.href = '#'
        li.appendChild(name);
    }

    // view markers
    if (current == 1) showCinemas();
    else showEvents();
}

function showCinemas()
{
    current = 1;
    var ul_cinemas = document.getElementById('cinemas');
    var ul_events = document.getElementById('events');
    ul_cinemas.style.display = 'block';
    ul_events.style.display = 'none';

    // clear map
    map.removeLayer(objects)
    // initialize markers and points for auto positioning map
    objects = new L.LayerGroup();
    if (cinemasData.length != 0) {
        var points = [];
        for (var i=cinemaInd; i<cinemaInd+11 && i<cinemasData.length; i++)
        {
            if (cinemasData[i].geo)
            {
                L.marker(cinemasData[i].geo)
                    .bindPopup(cinemasData[i].name)
                    .addTo(objects);
                points.push(cinemasData[i].geo);
            }
        }
        var bounds = new L.LatLngBounds(points);
        // auto positioning
        map.fitBounds(bounds);
        // view markers
        objects.addTo(map);
    }
};

function showEvents()
{
    current = 0;
    var ul_cinemas = document.getElementById('cinemas');
    var ul_events = document.getElementById('events');
    ul_cinemas.style.display = 'none';
    ul_events.style.display = 'block';

    // clear map
    map.removeLayer(objects);
    // initialize markers and points for auto positioning map
    objects = new L.LayerGroup();
    if (eventsData.length != 0) {
        var points = [];
        for (var i=eventInd; i<eventInd+5 && i<eventsData.length; i++)
        {
            if (eventsData[i].geo) {
                L.marker(eventsData[i].geo)
                    .bindPopup('<b>' + eventsData[i].place + '</b><br />' + eventsData[i].address)
                    .addTo(objects);
                points.push(eventsData[i].geo);
            }
        }
        var bounds = new L.LatLngBounds(points);
        // auto positioning
        map.fitBounds(bounds);
        // view markers
        objects.addTo(map);
    }
};

function changePage(id)
{
    if (id == 'left')  {
        if (current == 0) {
            if (eventInd-5 >= 0) {
                eventInd -= 5;
                createObjects()
            }
        }
        else {
            if (cinemaInd-11 >= 0) {
                cinemaInd -= 11;
                createObjects()
            }
        }

    }
    else {
        if (current == 0) {
            if (eventInd+5 < eventsData.length) {
                eventInd += 5;
                createObjects()
            }
        }
        else {
            if (cinemaInd+11 < cinemasData.length) {
                cinemaInd += 11;
                createObjects()
            }
        }
	}
};