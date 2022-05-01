function add(item){
    console.log(item);
    var htmlList = document.getElementById("playlistList");
    var element = document.createElement("li");
    num = htmlList.children.length + 1;
    element.setAttribute("id", num);
    element.setAttribute("class", "playlistItems");
    // element.setAttribute("draggable", "true");

    var brightness = createBrightness();
    // brightness.innerHTML = '<i class="material-icons">brightness_medium</i>';
    var colorPicker = createColorPicker();
    var delay = createDelay();
    var cycles = createCycles();
    var colorCB = createCheckbox(element.id);
    var secondColor = createSecondColor(element.id);
    secondColor.style.display = "none"
    colorCB.onclick = function() { displayColor2(colorCB, secondColor); };
    var deleteBtn = createDeleteBtn();
    deleteBtn.onclick = function() { removeElement(element.id); };
    console.log(deleteBtn.onclick);

    if(item === "colorWipe"){
        element.innerText = "Color Wipe";
        element.name = "colorWipe";
        element.append(brightness);
        element.append(colorPicker);
        label = createLabel("Delay:", delay.name);
        element.append(label);
        element.append(delay)
        element.append(colorCB);
        element.append(secondColor);
        element.prepend(deleteBtn);
    }
    else if(item === "colorFill"){
        element.innerText = "Color Fill";
        element.name = "colorFill";
        element.append(brightness);
        element.append(colorPicker);
        element.append(colorCB);
        element.append(secondColor);
        element.prepend(deleteBtn);
    }
    else if(item === "rColorWipe"){
        element.innerText = "Reverse Color Wipe";
        element.name = "rColorWipe";
        element.append(brightness);
        element.append(colorPicker);
        element.append(colorCB);
        element.append(secondColor);
        label = createLabel("Delay:", delay.name);
        element.append(label);
        element.append(delay)
        element.prepend(deleteBtn);
    }
    else if(item === "dotFill"){
        element.innerText = "Dot Fill";
        element.name = "dotFill";
        element.append(brightness);
        element.append(colorPicker);
        element.prepend(deleteBtn);
    }
    else if(item === "pause"){
        element.innerText = "Pause";
        element.name = "pause";
        delay.setAttribute("name", "pause");
        element.append(delay)
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
        element.prepend(deleteBtn);
    }
    else if(item === "twinkle"){
        element.innerText = "Twinkle";
        element.name = "twinkle";
        element.append(brightness);
        element.append(colorPicker);
        element.append(colorCB);
        element.append(secondColor);
        label = createLabel("Delay:", delay.name);
        element.append(label);
        delay.setAttribute("value", 1000);
        element.append(delay)
        label = createLabel("Cycles:", cycles.name);
        element.append(label);
        element.append(cycles);
        element.prepend(deleteBtn);
    }
    else if(item === "disco"){
        element.innerText = "Disco";
        element.name = "disco";
        element.append(brightness);
        element.append(colorPicker);
        element.append(colorCB);
        element.append(secondColor);
        label = createLabel("Delay:", delay.name);
        element.append(label);
        delay.setAttribute("value", 50);
        element.append(delay);
        label = createLabel("Cycles:", cycles.name);
        element.append(label);
        element.append(cycles);
        element.prepend(deleteBtn);
    }
    htmlList.appendChild(element);

    makeDraggable();
}

function createObject(list){
    sequence = [];
    var list = document.getElementById("playlistList");
    var items = list.getElementsByTagName("li")
    console.log(items);
    var brightness = 100;
    var color1;
    var color2 = "None";
    var delay = 0;
    var cycles = 1;
    pause = 0;
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
            if(items[i].children[j].name == "color2CB"){
                if(items[i].children[j].checked){
                    color2 = items[i].children[j+1].value;
                }
                if(items[i].children[j].checked == false){
                    color2 = "None";
                }
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
            elem = {
                name: items[i].name,
                method: "color_wipe",
                brightness: brightness,
                color1: color1,
                options: {
                    option1: {
                        choice: "delay",
                        value: delay
                    },
                    option4: {
                        choice: "2Colors",
                        color1: color1,
                        color2: color2
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
                    option4: {
                        choice: "2Colors",
                        color1: color1,
                        color2: color2
                    }
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
                    },
                    option4: {
                        choice: "2Colors",
                        color1: color1,
                        color2: color2
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
                    },
                    option4: {
                        choice: "2Colors",
                        color1: color1,
                        color2: color2
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
                    },
                    option4: {
                        choice: "2Colors",
                        color1: color1,
                        color2: color2
                    }
                }
            }
        }

        console.log(elem);
        addToSequence(elem);
    }
    // console.log(sequence);

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
    // console.log(sequence);
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
    secondColor.setAttribute("class", "color2");
    secondColor.setAttribute("value", "#ff0000");
    // secondColor.style.display = "inline-block";
    return secondColor;
}

function createCheckbox(){
    var cb = document.createElement("input");
    cb.setAttribute("type", "checkbox");
    cb.setAttribute("class", "color2CB");
    cb.setAttribute("name", "color2CB");
    return cb
}

function createBrightness(){
    var brightness = document.createElement("input");
    brightness.setAttribute("type", "range");
    brightness.setAttribute("min", 1);
    brightness.setAttribute("max", 100);
    brightness.setAttribute("value", 15);
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
    btn.style.backgroundColor = "rgb(12, 143, 112)";
    btn.style.color = "white";
    btn.style.borderRadius = "15%";
    btn.style.border = "1px solid black";
    btn.setAttribute("name", "delBtn");
    btn.addEventListener("mouseenter", function( event ) {   
        event.target.style.backgroundColor = "rgb(41, 233, 159)";
    }, false);
    btn.addEventListener("mouseleave", function( event ) {   
        event.target.style.backgroundColor = "rgb(12, 143, 112)";
    }, false);

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

function displayColor2(cb, color2){
    if(cb.checked == false){
        color2.style.display = "none";
    }
    if(cb.checked){
        color2.style.display = "inline-block";                    
    }
}

function getControlsData(){
    // var form = new FormData();
    // form.get("controlsForm");
    // console.log(form);
}

function sendAudioTimeStamps(audio, color, brightness){
    console.log("Sending song");
    console.log(audio)
    currentTime = Math.round(audio.currentTime * 10)/10;
    src = audio.children[0].src
    console.log(currentTime)

    song = {
        name: src,
        currentTime: currentTime,
        color: color,
        onsets: audio.id,
        brightness: brightness
    }

    $.ajax({
        type: "POST",
        url: "/musicSync/musicChange",
        data: JSON.stringify(song),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            console.log("Result:");
            console.log(result);
        }  
    });
}

function shutdownRebootAlert(choice){
    if(choice === "shutdown"){
        if(confirm("Shutdown the Pi?")){
            console.log("yes")
            sendPiCommand("shutdown")
        }
        else{
            console.log("no")
        }
    }
    else if(choice === "reboot"){
        if(confirm("Reboot the Pi?")){
            console.log("yes")
            sendPiCommand("reboot")
        }
        else{
            console.log("no")
        }
    }
}

function sendPiCommand(choice){
    piControl = {
        choice: choice
    }

    $.ajax({
        type: "POST",
        url: window.location.pathname,
        data: JSON.stringify(piControl),
        contentType: "application/json",
        dataType: 'json',
        success: function(result) {
            console.log("Result:");
            console.log(result);
        }  
    });
}


// The following code was taken from https://web.dev/drag-and-drop/
// It enables the ability to drag and drop playlist items in order
// to reorganize them in the list. It was altered slightly to be 
// compatible with my code.
// function handleDragStart(e) {
//     this.style.opacity = '0.4';

//     dragSrcEl = this;

//     e.dataTransfer.effectAllowed = 'move';
//     e.dataTransfer.setData('text/html', this.innerHTML);
// }

// function handleDragEnd(e) {
//     this.style.opacity = '1';
//     let items = document.querySelectorAll('.playlistItems');
//     items.forEach(function (item) {
//         item.classList.remove('over');
//     });

//     var list = document.getElementById("playlistList");
//     var li = list.getElementsByTagName("li")
//     for(var i = 0; i < li.length; i++){
//         // console.log("list = " + list);
//         // console.log("li[i]" = + li[i]);
//         // console.log("li[i].id = " + li[i].id);  
//         for(var j = 0; j < li[i].children.length; j++){
//             if(li[i].children[j].name === "delBtn"){
//                 li[i].children[j].removeAttribute("onclick");
//                 e = document.getElementById(li[i].id);
//                 console.log("e = " + e);
//                 console.log("li[i].children[j] = " + li[i].children[j]);
//                 console.log(li[i].getAttribute("id"));
//                 li[i].children[j].onclick = function() { removeElement(e.id); };
//                 console.log(li[i].children[j].onclick);
//             }
//         }
//     }
// }

// function handleDragOver(e) {
//     if (e.preventDefault) {
//         e.preventDefault();
//     }
//     return false;
// }

// function handleDragEnter(e) {
//     this.classList.add('over');
// }

// function handleDragLeave(e) {
//     this.classList.remove('over');
// }

// function handleDrop(e) {
//     e.stopPropagation();
//     // console.log(e);

//     if (dragSrcEl !== this) {
//         dragSrcEl.innerHTML = this.innerHTML;
//         this.innerHTML = e.dataTransfer.getData('text/html');
//     }

//     return false;
// }

// function makeDraggable(){
//     let items = document.querySelectorAll('.playlistItems');
//     // console.log(items);
//     items.forEach(function(item) {
//         item.addEventListener('dragstart', handleDragStart);
//         item.addEventListener('dragover', handleDragOver);
//         item.addEventListener('dragenter', handleDragEnter);
//         item.addEventListener('dragleave', handleDragLeave);
//         item.addEventListener('dragend', handleDragEnd);
//         item.addEventListener('drop', handleDrop);
//     });
// }
//END code from https://web.dev/drag-and-drop/
