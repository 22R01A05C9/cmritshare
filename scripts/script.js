window.addEventListener('load', function () {
    document.querySelector('#preLoader').style.display = "none";
})
document.querySelectorAll('.box').forEach(ele => {
    ele.style.background = ele.getAttribute('data-clr');
});
// const scroll = new LocomotiveScroll({
//     el: document.querySelector('#main'),
//     smooth: true
// });
const url_area = document.querySelector('.url_area'),
    box1 = document.querySelector('#box_1'),
    box2 = document.querySelector('#box_2');

url_area.addEventListener('mousemove', (e) => {
    let cord_x = e.clientX
    box1.style.marginLeft = cord_x / 4 + 'px';
    box1.style.marginLeft = cord_x / 4 + 'px';
    box2.style.marginTop = -cord_x / 4 + 'px';
    box1.style.marginTop = cord_x / 4 + 'px';
});
function animations() {

    gsap.from('.logo', {
        y: -20,
        delay: .5,
        opacity: 0,
        duration: .5,
    });
    gsap.from('.nav-link', {
        y: -20,
        delay: .1,
        opacity: 0,
        duration: .5,
        stagger: .5
    });
    gsap.from('.btn-login', {
        y: 10,
        scale: 0,
        delay: .5,
        opacity: 0,
        duration: 1,
    });
    gsap.from('.main-title', {
        y: 50,
        opacity: 0,
        delay: 0.5,
        duration: 0.5
    });
    gsap.from('.small-title', {
        opacity: 0,
        duration: .8,
        scale: 0,
        delay: .8
    });
}
animations()
let deviceWidth = window.innerWidth;
let finalPath = `M ${deviceWidth * .1} 100 Q ${deviceWidth * 0.5} 100 ${deviceWidth * 0.9} 100`;
function setSvgPath() {
    let deviceWidth = window.innerWidth;
    let finalPath = `M ${deviceWidth * .1} 100 Q ${deviceWidth * 0.5} 100 ${deviceWidth * 0.9} 100`
    document.querySelector('svg path').setAttribute('d', finalPath);
}
setSvgPath()
window.addEventListener('resize', function () {
    setSvgPath()
})
document.querySelector('.svg-area').addEventListener('mousemove', (e) => {
    let deviceWidth = window.innerWidth;
    let path = `M ${deviceWidth * .1} 100 Q ${deviceWidth * 0.5} ${e.offsetY} ${deviceWidth * 0.9} 100`
    gsap.to("svg path", {
        duration: 0.3,
        attr: { d: path },
        ease: "elastic.out(1, 0.2)",
    });
});
document.querySelector('.svg-area').addEventListener('mouseleave', (e) => {
    gsap.to("svg path", {
        attr: { d: finalPath },
        ease: "elastic.out(1, 0.2)",
        duration: 1.5,
    });
});
document.querySelectorAll('.use-area i').forEach(ele => {
    ele.style.background = ele.getAttribute('data-clr')
});
let inputs = document.querySelectorAll('.login input');
inputs.forEach(ele => {
    ele.addEventListener('focus', () => {
        let parentElement = ele.parentElement;
        parentElement.classList.add('focus')
    })
    ele.addEventListener('blur', () => {
        let parentElement = ele.parentElement;
        parentElement.classList.remove('focus')
    })
});
let contextBox = document.querySelector('.context_menu');
window.addEventListener('contextmenu', (event) => {
    event.preventDefault();
    let x = event.x,
        y = event.y;
    contextBox.style.display = "block";
    contextBox.style.left = x + "px";
    contextBox.style.top = y + "px";
    contextBox.querySelectorAll('li').forEach(ele => {
        addEventListener('click', (e) => {
            contextBox.style.display = "none";
        })
    });
});

let navbar = document.querySelector('.navbar'),
    toggleThumb = document.querySelector('#toggler');
toggleThumb.addEventListener('click', function () {
    navbar.classList.toggle('visible');
});
document.querySelector('#main').style.overflow = "hidden";


const text = document.querySelector('.text p');
text.innerHTML = text.innerText.split('').map(
    (char, i) => `<span style="transform: rotate(${i * 7}deg);"> ${char} </span>`
).join('');