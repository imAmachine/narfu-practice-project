let img = document.querySelector('.main__wrapper__img')
let address = document.querySelector('.main__wrapper__subheader')
let text = document.querySelector('.main__wrapper__text')

document.addEventListener('DOMContentLoaded', async function() {
  let sliderWrapper = document.getElementsByClassName("slider__wrapper")[0]
  let response = await fetch('/api/dormitories')
  if (response.ok) {
    let jsonDormitory = await response.json()
    jsonDormitory.forEach(el => {
      let img = document.createElement('img')
      img.className = 'slider__img'
      img.src = el['photo']
      img.id = el['dormitory_id']
      sliderWrapper.appendChild(img)
    })

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

    sliderImages.forEach(el => el.addEventListener('click', () => getInfo(el.id - 1)));

    async function getInfo(id) {
      let header = document.getElementsByClassName('main__wrapper__header')[0]
      let btns = document.querySelector('.room__number__btns')
      btns.innerHTML = ""

      header.innerHTML = jsonDormitory[id]['name']
      header.id = jsonDormitory[id]['dormitory_id']
      img.src = jsonDormitory[id]['photo']
      address.innerHTML = jsonDormitory[id]['address']
      text.innerHTML = jsonDormitory[id]['description']

      let response = await fetch(`/api/rooms/${header.id}`)
      if (response.ok) {
        let jsonRooms = await response.json()
        if (jsonRooms.length > 0) {
          jsonRooms.forEach(el => {
            let btn = document.createElement('button')
            if (el['status'] == true) {
              btn.className = 'room__number__btn room__number__btn_disable'
              btn.disabled = true
            }
            else {
              btn.className = 'room__number__btn room__number__btn_mozhno'
              btn.addEventListener('click', () => clickRoom(btn))
              // document.getElementsByClassName('room__number__btn_mozhno')[0].classList.add('room__number__btn_active')
            }
            btn.innerHTML = `№ ${el['room_number']}<br> ${el.occupied} / ${el['total_places']}`
            btns.appendChild(btn)
          })
        }
        document.querySelector('.room__img').src = jsonRooms[id]['photo']
      }
    }
    getInfo(0)
  }
  else alert("Ошибка HTTP: " + response.status)
})