function add(item){
    console.log(item);
    var htmlList = document.getElementById("playlistList");
    var element = document.createElement("li");
    num = htmlList.children.length + 1;
    element.setAttribute("id", num);

    var brightness = createBrightness();
    var colorPicker = createColorPicker();
    var delay = createDelay();
    var cycles = createCycles();
    var colorCB = createCheckbox();
    var secondColor = createSecondColor();
    var deleteBtn = createDeleteBtn();

    if(item === "colorWipe"){
        element.innerText = "Color Wipe";
        element.name = "colorWipe";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
        label = createLabel("Delay:", delay.name);
        element.append(label);
        element.append(delay)
        element.append(colorCB);
        secondColor.style.display = "none"
        element.append(secondColor);
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
        
    }
    else if(item === "colorFill"){
        element.innerText = "Color Fill";
        element.name = "colorFill";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    else if(item === "rColorWipe"){
        element.innerText = "Reverse Color Wipe";
        element.name = "rColorWipe";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
        label = createLabel("Delay:", delay.name);
        element.append(label);
        element.append(delay)
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    else if(item === "dotFill"){
        element.innerText = "Dot Fill";
        element.name = "dotFill";
        element.append(brightness);
        element.append(colorPicker);
        //need 2 colors
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    else if(item === "pause"){
        element.innerText = "Pause";
        element.name = "pause";
        delay.setAttribute("name", "pause");
        element.append(delay)
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    else if(item === "fade"){
        element.innerText = "Fade";
        element.name = "fade";
        element.append(brightness);
        element.append(colorPicker);
        label = createLabel("Cycles:", cycles.name);
        element.append(label);
        element.append(cycles);
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    else if(item === "theaterChase"){
        element.innerText = "Theater Chase";
        element.name = "theaterChase";
        element.append(brightness);
        element.append(colorPicker);
        label = createLabel("Delay:", delay.name);
        element.append(label);
        element.append(delay);
        label = createLabel("Cycles:", cycles.name);
        element.append(label);
        element.append(cycles);
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    else if(item === "twinkle"){
        element.innerText = "Twinkle";
        element.name = "twinkle";
        element.append(brightness);
        element.append(colorPicker);
        label = createLabel("Delay:", delay.name);
        element.append(label);
        delay.setAttribute("value", 1000);
        element.append(delay)
        label = createLabel("Cycles:", cycles.name);
        element.append(label);
        element.append(cycles);
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    else if(item === "disco"){
        element.innerText = "Disco";
        element.name = "disco";
        element.append(brightness);
        element.append(colorPicker);
        label = createLabel("Delay:", delay.name);
        element.append(label);
        delay.setAttribute("value", 50);
        element.append(delay);
        label = createLabel("Cycles:", cycles.name);
        element.append(label);
        element.append(cycles);
        deleteBtn.onclick = function() { removeElement(element.id); };
        element.prepend(deleteBtn);
    }
    htmlList.appendChild(element);
}

function createObject(list){
    sequence = [];
    var list = document.getElementById("playlistList");
    var items = list.getElementsByTagName("li")
    console.log(items);
    console.log(items.length);
    var brightness = 100;
    var color1;
    var color2;
    var delay = 0;
    var cycles = 1;
    pause = 0;
    // elem = {};
    
    for(var i = 0; i < items.length; i++){
        console.log(items[i]);  
        console.log(items[i].innerText);
        for(var j = 0; j < items[i].children.length; j++){
            console.log(items[i].children[j]);
            if(items[i].children[j].name === "brightness"){
                brightness = items[i].children[j].value;
            }
            if(items[i].children[j].name === "color1"){
                color1 = items[i].children[j].value;
            }
            if(items[i].children[j].name === "delay"){
                if(items[i].children[j].value < 0){
                    items[i].children[j].value = 0;
                }
                delay = items[i].children[j].value;
            }
            if(items[i].children[j].name === "cycles"){
                if(items[i].children[j].value < 1){
                    items[i].children[j].value = 1;
                }
                cycles = items[i].children[j].value;
            }
            if(items[i].children[j].name === "pause"){
                pause = items[i].children[j].value;
            }
        }
        if(items[i].name === "colorWipe"){
            console.log("creating colorWipe object")
            elem = {
                name: items[i].name,
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
        else if(items[i].name === "colorFill"){
            elem = {
                name: items[i].name,
                method: "color_fill",
                brightness: brightness,
                color1: color1,
                options: {

                }
            }
        }
        else if(items[i].name === "rColorWipe"){
            elem = {
                name: items[i].name,
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
        else if(items[i].name === "dotFill"){
            elem = {
                name: items[i].name,
                method: "dot_fill",
                brightness: brightness,
                color1: color1,
                options: {
                    
                }
            }
        }
        else if(items[i].name === "pause"){
            elem = {
                name: items[i].name,
                method: "pause",
                wait: pause
            }
        }
        else if(items[i].name === "fade"){
            elem = {
                name: items[i].name,
                method: "fade",
                brightness: brightness,
                color1: color1,
                options: {
                    option3: {
                        choice: "cycles",
                        value: cycles
                    }
                }
            }
        }
        else if(items[i].name === "theaterChase"){
            elem = {
                name: items[i].name,
                method: "theater_chase",
                brightness: brightness,
                color1: color1,
                options: {
                    option3: {
                        choice: "cycles",
                        value: cycles
                    }
                }
            }
        }
        else if(items[i].name === "twinkle"){
            elem = {
                name: items[i].name,
                method: "twinkle_disco",
                brightness: brightness,
                color1: color1,
                options: {
                    function: "twinkle",
                    option1: {
                        choice: "delay",
                        value: delay
                    },
                    option3: {
                        choice: "cycles",
                        value: cycles
                    }
                }
            }
        }
        else if(items[i].name === "disco"){
            elem = {
                name: items[i].name,
                method: "twinkle_disco",
                brightness: brightness,
                color1: color1,
                options: {
                    function: "disco",
                    option1: {
                        choice: "delay",
                        value: delay
                    },
                    option3: {
                        choice: "cycles",
                        value: cycles
                    }
                }
            }
        }

        console.log(elem);
        addToSequence(elem);
    }
    console.log(sequence);

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
    delay.setAttribute("maxLength", 5);
    delay.setAttribute("size", 1);
    delay.setAttribute("name", "delay");
    return delay;
}

function createCycles(){
    var cycles = document.createElement("input");
    cycles.setAttribute("type", "text");
    cycles.setAttribute("value", 1);
    cycles.setAttribute("maxLength", 4);
    cycles.setAttribute("size", 1);
    cycles.setAttribute("name", "cycles");
    return cycles;
}

function createLabel(text, id){
    var label = document.createElement("label");
    label.innerText = text;
    label.setAttribute("for", id);
    return label
}

function createDeleteBtn(){
    var btn = document.createElement("button");
    btn.innerHTML = '<i class="material-icons">&#xe5cd;</i>';
    return btn;
}

function removeElement(id){
    // console.log(id)
    list = document.getElementById("playlistList");
    item = document.getElementById(id);
    item.parentNode.removeChild(item);

    //reset the IDs of each item so we don't end up with duplicates from removing and adding
    for(var i = 0; i < list.children.length; i++){
        list.children[i].setAttribute("id", i+1)
    }
}

function cancelSequence(){
    cancelTask = {
        cancel: "cancelTask"
    }
    $.ajax({
        type: "POST",
        url: "/playlists/playlistsChange",
        data: JSON.stringify(cancelTask),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            console.log("Result:");
            console.log(result);
        }  
    });
}