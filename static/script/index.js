const prevs = document.getElementById("prev");
const nexts = document.getElementById("next");
const rasmlar = document.querySelector('.section_top_left_top_ul')
const rasm = document.querySelectorAll('.section_top_left_top_ul_li')
let count = 0;
prevs.style.display = `flex`

function ChangeImage() {


    if (count > rasm.length / 4) {
        count = 0
    } else if (count <= 0) {
        count = rasm.length / 4
    }
    prevs.style.display = `flex`
    nexts.style.display = `flex`
    rasmlar.style.transform = ` translateX(${-count * 78}px)`
    rasmlar.style.transition = '0.5s'
    console.log(count)
}


nexts.addEventListener("click", () => {
    count++;
    ChangeImage()
})
prevs.addEventListener("click", () => {
    count--;
    ChangeImage()
})
const video = document.querySelectorAll('.section_top_left_bottom_bottom_video');
const height = document.querySelectorAll('.section_top_left_bottom');
const topes = document.querySelector('.section_top')
const add = document.querySelectorAll('.comissis')
const close = document.querySelectorAll('.close')
const madalni = document.querySelectorAll('.madal')
topes.style.height = `${height.length * 650 + 200}`
console.log(add.length)
function togglePlay() {
    video.forEach((item, id) => {
        item.addEventListener('click', () => {

            if (video[id].paused) {
                video[id].play();
            } else {
                video[id].pause();
            }
        })
    })
}

add.forEach((item, id) => {
    item.addEventListener('click', () => {
        madalni[id].style.display = `flex`
        console.log(id)
    })
})
close.forEach((item, id) => {
    item.addEventListener('click', () => {
        madalni[id].style.display = `none`
        console.log(id)
    })
})
togglePlay()
const divcha = document.querySelector('.div'),
    search = document.querySelector('.search'),
    insta = document.querySelector('.div_top_instagram'),
    qora = document.querySelector('.qora'),
    sections=document.querySelector('.section')
search.addEventListener('click', () => {
    divcha.style.borderRight = `none`
    divcha.style.width = `50px`
    divcha.style.overflow = `hidden`
    insta.style.opacity = `0`
    qora.style.left = `50px`
    qora.style.opacity = `1`
    qora.style.zIndex = `1`
})
sections.addEventListener('click', () => {
    divcha.style.borderRight = `0.3px solid rgb(38, 38, 38)`
    divcha.style.width = `244.8px`
    divcha.style.overflow = `visible`
    insta.style.opacity = `1`
    qora.style.left = `-300px`
    qora.style.opacity = `0`
    qora.style.zIndex = `0`
})