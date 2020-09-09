document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');

    load_weather();
    load_posts();
});


function load_posts() {
    // Create a array filled with all the posts 
    var arr = [];
    // Initial append when loaded, so it would not repeat twice. Alternatively I can fetch only once.
    var arr2 = [];
    var j = 0;
    var k=0;

    var url = '/load_posts'
        fetch(url)
        .then(response => response.json())
        .then(posts => {
        // Print posts
        console.log(posts);
            // HTML structure before append 
            for (var post in posts) {
                const div = document.createElement('div');
                div.innerHTML = "<b><a href='/profile/" + posts[post].poster + "'>" + posts[post].poster + "</a></b>" +
                    "<div class='timestamp'>" + posts[post].timestamp + "</div>" +
                    "<br>" + posts[post].content;
                div.className = 'message-board-post';
                // Append all div posts into array 
                arr2.push(div);
            }
            
            document.querySelector('#message-board').append(arr2[0],arr2[1],arr2[2],arr2[3],arr2[4],arr2[5],arr2[6],arr2[7]);
            j += 8
        })

        // fetch data
        var url = '/load_posts'
        fetch(url)
        .then(response => response.json())
        .then(posts => {
        // Print posts
        console.log(posts);
            // HTML structure before append 
            for (var post in posts) {
                const div = document.createElement('div');
                div.innerHTML = "<b><a href='/profile/" + posts[post].poster + "'>" + posts[post].poster + "</a></b>" +
                    "<div class='timestamp'>" + posts[post].timestamp + "</div>" +
                    "<br>" + posts[post].content;
                div.className = 'message-board-post';
                // Append all div posts into array 
                arr.push(div);
            }

                // var container = document.getElementById(`message-board`);
                // console.log(container)

                //     if (container.scrollTop + container.innerHeight >= container.scrollHeight) {
                //         console.log(totalScrolled, scrollHeight)
                //     }
            

            // If scrolled to the bottom, load more posts
            window.onscroll = () => {
                if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
                        console.log(j, arr[j]);
                        if(arr[j]==undefined) {
                            
                        } else {
                            var i;
                            // Append x number of times
                            for(i = 0; i < (k + 4); i++, j++){
                                if (arr[j]!=undefined) {
                                    document.querySelector('#message-board').append(arr[j])
                                } else {
                                    end = "Congratulation, you have reached the end!"
                                    document.querySelector('#message-board').append(end)
                                    break
                                }
                            }
                            
                            // restore scroll back up a bit 
                            window.scrollBy(0, -21);
                            // Keeps div scroll to the bottom
                            document.querySelector('#message-board').scrollTop = document.querySelector('#message-board').scrollHeight;

                        }
                    }
                }
        // console.log(arr);
        // document.querySelector('#message-board').append(div);
        })
    //   append_post(arr);
    
}

// function append_post(arr) {

//     var i;
//     for (i = 0; i < (arr.length - arr.length + 1); i++) {
//         document.querySelector('#message-board').append(arr[i]);
//         console.log(arr[i])
//     };

//     append_more(arr)
// }

// function append_more(arr) {

//     window.onscroll = () => {
//         if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
//             var i;
//             var j = 3;
//             for (i = 0; i < j; i++) {
//                 document.querySelector('#message-board').append(arr[i]);
//                 window.scrollBy(0, -3);
//                 document.querySelector('#message-board').scrollTop = document.querySelector('#message-board').scrollHeight;
//             };
//             j++
//             append_more(arr) 
//         } 
//     }
// }

// <b><span class='cap'>
// <a href="{% url 'weather:profile_page' post.poster.username %}">{{ post.poster.username }}</a>
// </span></b>
// <div class='timestamp'>{{ post.timestamp }}</div> <br>

// <form>
// <div class="form-group">
// <span id="content_{{ post.id }}">{{ post.content }}</span>



// Compose post
function compose_post() {
    // Nothing submitted then no actions 
    if (document.querySelector('#compose-body').value == '') {
        document.querySelector('#compose-body').value == ''
    } else {
        const post_body = document.querySelector('#compose-body').value;
        console.log(post_body);

        // Access API, and pass data for the composed post
        fetch('/create_post', {
            method: 'POST',
            body: JSON.stringify({
                body: post_body
            })
        })

        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);
            // Clear form
            document.querySelector('#compose-body').value = '';
            // Refersh
            window.location.href = 'https://leonweatherapp.herokuapp.com';
        });


    }
}

function load_weather() {
    const iconElement = document.querySelector(".weather-icon");
    const tempElement = document.querySelector(".temperature-value p");
    const descElement = document.querySelector(".temperature-description p");
    const locationElement = document.querySelector(".location p");
    const notificationElement = document.querySelector(".notification");
    const feels_like_Element = document.querySelector(".feels-like-value");


    // App data
    const weather = {};

    weather.temperature = {
        unit : "celsius"
    }

    // APP CONSTS and VARS
    const KELVIN = 273;
    // API KEY
    const key = "62ba9f5e1650dc4d547b7c7f83971362"

    // Check if browser supports Geolocation
    if('geolocation' in navigator){
        navigator.geolocation.getCurrentPosition(setPosition, showError);
    }else{
        notificationElement.style.display = "block";
        notificationElement.innerHTML = "<p>Browser doesn't Support Geolocation</p>";
    }

    // SET USER'S POSITION
    function setPosition(position){
        let latitude = position.coords.latitude;
        let longitude = position.coords.longitude;
        
        getWeather(latitude, longitude);
    }

    // Show error if issue with geolocation service
    function showError(error){
        notificationElement.style.display = "block";
        notificationElement.innerHTML = `<p> ${error.message} </p>`;
    }

    // Get weather from API provider
    function getWeather(latitude, longitude){
        let api = `http://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${key}`;
        
        fetch(api)
            .then(function(response){
                let data = response.json();
                return data;
            })
            .then(function(data){
                weather.temperature.value = Math.floor(data.main.temp - KELVIN);
                weather.feels_like = Math.floor(data.main.feels_like - KELVIN);
                weather.humidity = Math.floor(data.main.humidity);
                weather.description = data.weather[0].description;
                weather.iconId = data.weather[0].icon;
                weather.city = data.name;
                weather.country = data.sys.country;
                console.log(data);
            })
            .then(function(){
                displayWeather();
                console.log(weather.temperature.value, weather.feels_like, weather.humidity, weather.description, weather.city, weather.country)
            });
    }

    function displayWeather(){
        iconElement.innerHTML = `<img src="static/weather/icons/${weather.iconId}.png"/>`;
        tempElement.innerHTML = `${weather.temperature.value}°<span>C</span>`;
        descElement.innerHTML = weather.description;
        locationElement.innerHTML = `${weather.city}, ${weather.country}`;
        feels_like_Element.innerHTML = `Feels like: ${weather.feels_like}°<span>C</span>`;
        };
}