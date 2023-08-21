let addd = document.getElementById('add'),
    closes = document.getElementById('close'),
    madal = document.querySelector('.madalnias'),
    next = document.getElementById('next'),
    inputss = document.getElementById('fileInput'),
    transforms = document.getElementById('mad2'),
    masad = document.querySelector('.masads'),
    videocha = document.getElementById('video')

addd.addEventListener('click', (event) => {
    madal.style.display = `flex`
})

inputss.addEventListener('change', () => {
    masad.style.width = '850px'
    transforms.style.transform = `translateX(-550px)`
    let file = inputss.files[0];
    const reader = new FileReader();
    reader.onload = function (e) {
        const content = e.target.result;
        videocha.src = `${content}`
    }

    reader.readAsDataURL(file);
});

closes.addEventListener('click', (event) => {
    madal.style.display = `none`
         masad.style.width = '550px'
    transforms.style.transform = `translateX(0)`

})
