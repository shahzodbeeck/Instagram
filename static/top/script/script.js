const addds = document.querySelectorAll('.section_divs .section_divs_div')
const closess = document.querySelector('.close')
const madalni = document.querySelector('.madalni')
addds.forEach((item, id) => {
    item.addEventListener('click', () => {
        madalni.style.display = `flex`
    })
})
closess.addEventListener('click', () => {
    madalni.style.display = `none`
})
const videos = document.querySelectorAll('.section_top_left_bottom_bottom_video');

function togglePlay() {
    videos.forEach((item, id) => {
        item.addEventListener('click', () => {

            if (videos[id].paused) {
                videos[id].play();
            } else {
                videos[id].pause();
            }
        })
    })
}

togglePlay()


const nexts = document.getElementById("next");
const prevs = document.getElementById("prev");
const slides = document.querySelectorAll('.madd');

function nextSlide() {
    const current = document.querySelector(".current");
    current.classList.remove("current");
    if (current.nextElementSibling) {
        current.nextElementSibling.classList.add("current");
    } else {
        slides[0].classList.add("current");
    }
}

function prevSlide() {
    const current = document.querySelector(".current");
    current.classList.remove("current");
    if (current.previousElementSibling) {
        current.previousElementSibling.classList.add("current");
    } else {
        slides[slide.length - 1].classList.add("current");
    }
}

nexts.addEventListener("click", () => {
    nextSlide();
});
prevs.addEventListener("click", () => {
    prevSlide();
});