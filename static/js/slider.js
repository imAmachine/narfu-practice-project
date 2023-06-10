let btnLeft = document.getElementsByClassName('slider__btn_left')[0]
let btnRight = document.getElementsByClassName('slider__btn_right')[0]
let sliderImages = document.querySelectorAll('.slider__img')
let imgLength = document.getElementsByClassName('slider__img')[0].offsetWidth
let counter = 1
let startShift = 0
let gap = 10

let sliderWrapper = document.getElementsByClassName("slider__wrapper")[0]
let countMinus = Math.floor(sliderWrapper.offsetWidth / imgLength)
let sliderShiftRight = () => {
  if (counter <= sliderImages.length - countMinus) {
    counter += 1
    startShift -= imgLength + gap
    sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`)
  }
}

let sliderShiftLeft = () => {
  if (counter > 1) {
    counter -= 1
    startShift += imgLength + gap
    sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`)
  }
}

btnLeft.onclick = sliderShiftLeft
btnRight.onclick = sliderShiftRight