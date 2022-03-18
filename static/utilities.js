function add(item){
    console.log(item);
    var htmlList = document.getElementById("playlistList");
    var element = document.createElement("li");
    num = htmlList.children.length + 1;
    element.setAttribute("id", num);

    if(item === "colorWipe"){
        var brightness = createBrightness();
        var colorPicker = createColorPicker();
        var delay = createDelay();
        
        element.innerText = "Color Wipe";
        element.append(brightness);
        element.append(colorPicker);
        element.append(delay)
        
        htmlList.appendChild(element);
    }
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
            elem = {
                name: items[i].innerText,
                brightness: brightness,
                color1: color1,
                delay: delay
            }
        }
        console.log(elem);
        addToSequence(elem);
    }
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
    return colorPicker;
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
