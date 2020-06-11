
function getSlider(){
    let values = slider1.noUiSlider.get();
    let low = Math.round(values[0]);
    let up = Math.round(values[1]);
    return low + ";" + up;
}


function getSlider2(){
    let values = slider2.noUiSlider.get();
    let low = Math.round(values[0]);
    let up = Math.round(values[1]);
    return low + ";" + up;
}

console.log(document.getElementById('slider1'));
let slider1 = document.getElementById('slider1');
noUiSlider.create(slider1, {
    start: [{{ slider.0.0 }}, {{ slider.0.1 }}], // Handle start position
    step: {{  slider.0.4 }}, // Slider moves in increments of '10'
    margin: 5, // Handles must be more than '20' apart
    connect: true, // Display a colored bar between the handles
    orientation: 'horizontal', // Orient the slider vertically
    //behaviour: 'tap-drag', // Move handle on tap, bar is draggable
    range: { // Slider can select '0' to '100'
         'min': {{ slider.0.2 }},
        'max': {{ slider.0.3 }}
    },
    pips: { // Show a scale with the slider
        mode: 'steps',
        density: 10
    }
});

slider1.noUiSlider.on('change', function(handle ) {
        if ( handle ) {
            console.log("now in handling uislider1");
            let lowup = getSlider();
            console.log(lowup);
    document.getElementById("id_slider1").value = lowup;
    }
    });




    function getSlider2(){
    let values = slider2.noUiSlider.get();
    let low = Math.round(values[0]);
    let up = Math.round(values[1]);
    return low + ";" + up;
}

console.log(document.getElementById('slider2'));
let slider2 = document.getElementById('slider2');
noUiSlider.create(slider2, {
    start: [{{ slider.1.0 }}, {{ slider.1.1 }}], // Handle start position
    step: {{ slider.1.4 }}, // Slider moves in increments of '10'
    margin: {{ slider.1.4 }}, // Handles must be more than '20' apart
    connect: true, // Display a colored bar between the handles
    orientation: 'horizontal', // Orient the slider vertically
    //behaviour: 'tap-drag', // Move handle on tap, bar is draggable
    range: { // Slider can select '0' to '100'
        'min': {{ slider.1.2 }},
        'max': {{ slider.1.3 }}
    },
    pips: { // Show a scale with the slider
        mode: 'steps',
        density: {{ slider.1.4}}
    }
});

slider2.noUiSlider.on('change', function(handle ) {
        if ( handle ) {
            console.log("now in handling uislider2");
            let uplow = getSlider2();
            console.log(uplow);
    document.getElementById("id_slider2").value = uplow;
    }
    });
