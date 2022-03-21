function add(item){
    console.log(item);
    var htmlList = document.getElementById("playlistList");
    var element = document.createElement("li");
    num = htmlList.children.length + 1;
    element.setAttribute("id", num);

    var brightness = createBrightness();
    var colorPicker = createColorPicker();
    var delay = createDelay();
    var colorCB = createCheckbox();
    var secondColor = createSecondColor();

    if(item === "colorWipe"){
        element.innerText = "Color Wipe";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
        element.append(delay)
        element.append(colorCB);
        secondColor.style.display = "none"
        element.append(secondColor);
    }
    else if(item === "colorFill"){
        element.innerText = "Color Fill";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
    }
    else if(item === "rColorWipe"){
        element.innerText = "Reverse Color Wipe";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
        element.append(delay)
    }
    else if(item === "dotFill"){
        element.innerText = "Dot Fill";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
    }
    else if(item === "fade"){
        element.innerText = "Fade";
        element.append(brightness);
        element.append(colorPicker);
    }
    else if(item === "theaterChase"){
        element.innerText = "Theater Chase";
        element.append(brightness);
        element.append(colorPicker);
    }
    else if(item === "twinkle"){
        element.innerText = "Twinkle";
        element.append(brightness);
        element.append(colorPicker);
    }
    else if(item === "disco"){
        element.innerText = "Disco";
        element.append(brightness);
        element.append(colorPicker);
    }
    
    

    htmlList.appendChild(element);
}

function createObject(list){
    var list = document.getElementById("playlistList");
    var items = list.getElementsByTagName("li")
    console.log(items);
    console.log(items.length);
    var brightness = 100;
    var color1;
    var color2;
    var delay = 0;
    // elem = {};
    
    for(var i = 0; i < items.length; i++){
        console.log(items[i]);  
        for(var j = 0; j < items[i].children.length; j++){
            console.log(items[i].children[j]);
            if(items[i].children[j].name === "brightness"){
                brightness = items[i].children[j].value;
            }
            if(items[i].children[j].name === "color1"){
                color1 = items[i].children[j].value;
            }
            if(items[i].children[j].name === "delay"){
                delay = items[i].children[j].value;
            }
        }
        if(items[i].innerText === "Color Wipe"){
            console.log("creating colorWipe object")
            elem = {
                name: items[i].innerText,
                method: "color_wipe",
                brightness: brightness,
                color1: color1,
                options: {
                    option1: {
                        choice: "delay",
                        value: delay
                    }
                }
            }
        }
        else if(items[i].innerText === "Color Fill"){
            elem = {
                name: items[i].innerText,
                method: "color_fill",
                brightness: brightness,
                color1: color1,
                options: {

                }
            }
        }
        else if(items[i].innerText === "Reverse Color Wipe"){
            elem = {
                name: items[i].innerText,
                method: "reverse_color_wipe",
                brightness: brightness,
                color1: color1,
                options: {
                    option1: {
                        choice: "delay",
                        value: delay
                    }
                }
            }
        }
        else if(items[i].innerText === "Dot Fill"){
            elem = {
                name: items[i].innerText,
                method: "dot_fill",
                brightness: brightness,
                color1: color1,
                options: {
                    
                }
            }
        }

        console.log(elem);
        addToSequence(elem);
    }

    // sequence = JSON.stringify(sequence);
    
    $.ajax({
        type: "POST",
        url: "/playlists/playlistsChange",
        data: JSON.stringify(sequence),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            console.log("Result:");
            console.log(result);
        }  
    });

}

sequence = [];
function addToSequence(elem){
    sequence.push(elem);
    console.log(sequence);
}

function createColorPicker(){
    var colorPicker = document.createElement('input');
    colorPicker.setAttribute("type", "color");
    colorPicker.setAttribute("name", "color1");
    colorPicker.setAttribute("value", "#ff0000");
    return colorPicker;
}

function createSecondColor(){
    var secondColor = document.createElement('input');
    secondColor.setAttribute("type", "color");
    secondColor.setAttribute("name", "color2");
    secondColor.setAttribute("value", "#ff0000");
    // secondColor.setAttribute("id", "color2");
    return secondColor;
}

function createCheckbox(){
    var cb = document.createElement("input");
    cb.setAttribute("type", "checkbox");
    return cb
}

function createBrightness(){
    var brightness = document.createElement("input");
    brightness.setAttribute("type", "range");
    brightness.setAttribute("min", 1);
    brightness.setAttribute("max", 100);
    brightness.setAttribute("value", 100);
    brightness.setAttribute("name", "brightness");
    return brightness;
}

function createDelay(){
    var delay = document.createElement("input");
    delay.setAttribute("type", "text");
    delay.setAttribute("value", 0);
    delay.setAttribute("maxLength", 4);
    delay.setAttribute("size", 1);
    delay.setAttribute("name", "delay");
    return delay;
}
