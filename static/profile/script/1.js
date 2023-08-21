let sss = document.querySelectorAll('.madd'),
    asassa=document.querySelectorAll('.section_bottom_bottom_left_div')
 sss[0].classList.add("current");
asassa.forEach((item, id) => {
    item.addEventListener('click', (event) => {
        console.log(id)
        let curre = document.querySelector(".current");
        curre.classList.remove("current");
        sss[id].classList.add('current')
    })
})
let ssdsdssds = document.querySelectorAll('.madd'),
    asassssa=document.querySelectorAll('.section_bottom_bottom_right_div')
 ssdsdssds[0].classList.add("current");
asassssa.forEach((item, id) => {
    item.addEventListener('click', (event) => {

        let curre = document.querySelector(".current");
        curre.classList.remove("current");
        ssdsdssds[id].classList.add('current')
    })
})