let checkedBoxes = document.querySelectorAll('input[name=energysource]');
let g = $("#gas");
let c = $("#coal");
let l = $("#lignite");

function getBoxes() {
    checkedBoxes = document.querySelectorAll('input[name=energysource]');
    console.log("codegeneration");
    let code = 0; // catch case if user set every checkbox to zero
    let lookup = {gas: 1, coal: 2, lignite: 6};
    for (let elem of checkedBoxes) {
        let checked = elem.checked;
        if (checked) {
            code += lookup[elem.id];
        }
    }
    console.log(code);
    if (code === 0) {
        code = 9;
    }
    return code;
}

function handleBoxes() {
    let url = getUrl();
    window.location.href = url;
}

g.change(function() {
    handleBoxes();
});

c.change(function() {
    handleBoxes();
});

l.change(function() {
    handleBoxes();
});

function getSlider(){
    let values = slider.noUiSlider.get();
    let low = Math.round(values[0]);
    let up = Math.round(values[1]);
    return low + "-" + up;
}

function getUrl() {
    let base = window.location.href;
    let base_l = base.split("/");

    let url = "";
    base_l.pop();
    let parent = base_l.pop();
    console.log(base_l);
    if (parent === "blocks") {
        url += "./"
    } else if (parent === "plantmaster") {
        url += "blocks"
    } else {
        url += "../"
    }

    url += getSlider();
    url += "-" + getBoxes();
    console.log(url);
    return url;
}

console.log(document.getElementById('slider'));
let range = document.getElementById('slider');
noUiSlider.create(range, {
    start: [{{ lower }}, {{ upper }}], // Handle start position
    step: 5, // Slider moves in increments of '10'
    margin: 5, // Handles must be more than '20' apart
    connect: true, // Display a colored bar between the handles
    orientation: 'horizontal', // Orient the slider vertically
    //behaviour: 'tap-drag', // Move handle on tap, bar is draggable
    range: { // Slider can select '0' to '100'
        'min': 1960,
        'max': 2020
    },
    pips: { // Show a scale with the slider
        mode: 'steps',
        density: 10
    }
});

range.noUiSlider.on('change', function(handle ) {
        if ( handle ) {
            console.log("now in handling uislider");
            let url = getUrl();
            console.log(url);
            window.location.href = url;
        }
    });