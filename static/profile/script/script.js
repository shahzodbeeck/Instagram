const add1= document.querySelectorAll('.section_bottom_bottom_left_div')
const add2= document.querySelectorAll('.section_bottom_bottom_center_div')
const add3= document.querySelectorAll('.section_bottom_bottom_right_div')
const close1= document.querySelector('.close')
const madalni = document.querySelector('.madalni')
add1.forEach((item,id)=>{
    item.addEventListener('click',()=>{
madalni.style.display=`flex`
    })
})
add2.forEach((item,id)=>{
    item.addEventListener('click',()=>{
madalni.style.display=`flex`
    })
})
add3.forEach((item,id)=>{
    item.addEventListener('click',()=>{
madalni.style.display=`flex`
    })
})
    close1.addEventListener('click',()=>{
madalni.style.display=`none`
    })
const video1 = document.querySelectorAll('.section_top_left_bottom_bottom_video');
function togglePlay() {
    video1.forEach((item, id) => {
        item.addEventListener('click', () => {

            if (video1[id].paused) {
                video1[id].play();
            } else {
                video1[id].pause();
            }
        })
    })
}
togglePlay()




const next1 = document.getElementById("next");
const prev1 = document.getElementById("prev");
const slide1 = document.querySelectorAll('.madd');

function nextSlide() {
    const currenta = document.querySelector(".current");
    currenta.classList.remove("current");
    if (currenta.nextElementSibling) {
        currenta.nextElementSibling.classList.add("current");
    } else {
        slide1[0].classList.add("current");
    }
}
function prevSlide() {
    const currenta = document.querySelector(".current");
    currenta.classList.remove("current");
    if (currenta.previousElementSibling) {
        currenta.previousElementSibling.classList.add("current");
    } else {
        slide1[slide1.length - 1].classList.add("current");
    }
}

next1.addEventListener("click", () => {
    nextSlide();
});
prev1.addEventListener("click", () => {
    prevSlide();
});
const lefts = document.getElementById('left'),
    suril =document.querySelector('.section_bottom_bottom'),
    center1 =document.getElementById('center'),
    rights=document.getElementById('right')
lefts.addEventListener('click',()=>{
    suril.style.transform=`translateX(0)`
})
center1.addEventListener('click',()=>{
    suril.style.transform=`translateX(-935px)`
})
rights.addEventListener('click',()=>{
    suril.style.transform=`translateX(-1870px)`
})