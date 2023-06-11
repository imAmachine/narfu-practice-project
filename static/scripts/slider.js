document.addEventListener('DOMContentLoaded', async function() {
  let sliderWrapper = document.getElementsByClassName("slider__wrapper")[0]
  let response = await fetch('/api/dormitories')
  if (response.ok) {
    let json = await response.json()
    for(let i=0; i<json.length; i++) {
      let img = document.createElement('img')
      img.className = 'slider__img'
      img.src = json[i]['photo']
      img.id = json[i]['dormitory_id']
      sliderWrapper.appendChild(img)
    }

    let btnLeft = document.getElementsByClassName('slider__btn_left')[0]
    let btnRight = document.getElementsByClassName('slider__btn_right')[0]
    let sliderImages = document.querySelectorAll('.slider__img')
    // let imgLength = document.querySelector('.slider__img').offsetWidth
    let counter = 1
    let startShift = 0
    let gap = 10
    let countMinus = Math.floor(sliderWrapper.offsetWidth / 200)

    let sliderShiftRight = () => {
      if (counter <= sliderImages.length - countMinus) {
        counter += 1
        startShift -= 200 + gap
        sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`)
      }
    }

    let sliderShiftLeft = () => {
      if (counter > 1) {
        counter -= 1
        startShift += 200 + gap
        sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`)
      }
    }

    btnLeft.onclick = sliderShiftLeft
    btnRight.onclick = sliderShiftRight

    sliderImages.forEach(el => el.addEventListener('click', () => getInfo(el.id)));

    let getInfo = id => {
      console.log(id)
    }
  }
  else alert("Ошибка HTTP: " + response.status)
})