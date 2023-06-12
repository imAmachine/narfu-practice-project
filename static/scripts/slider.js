let img = document.querySelector('.main__wrapper__img')
let address = document.querySelector('.main__wrapper__subheader')
let text = document.querySelector('.main__wrapper__text')

document.addEventListener('DOMContentLoaded', async function() {
  let sliderWrapper = document.getElementsByClassName("slider__wrapper")[0]
  let response = await fetch('/api/dormitories')
  if (response.ok) {
    let json = await response.json()
    json.forEach(el => {
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

      header.innerHTML = json[id]['name']
      header.id = json[id]['dormitory_id']
      img.src = json[id]['photo']
      address.innerHTML = json[id]['address']
      text.innerHTML = json[id]['description']

      let response = await fetch(`/api/rooms/${header.id}`)
        if (response.ok) {
          let json = await response.json()
          if (json.length > 0) {
            json.forEach(el => {
              let btn = document.createElement('button')
              if (el['occupied'] == el['total_places']) {
                btn.className = 'room__number__btn room__number__btn_disable'
                btn.disabled = true
              }
              else {
                btn.className = 'room__number__btn'
                btn.addEventListener('click', () => clickRoom(btn))
              }
              btn.innerHTML = `№ ${el['room_number']}<br> ${el['occupied']} / ${el['total_places']}`
              btns.appendChild(btn)
            })
          }
        }
      // smallImg.src = json[id]['photo']
      // нужна фотка комнаты и описание комнаты
    }

    getInfo(0)
  }
  else alert("Ошибка HTTP: " + response.status)

//   var form = document.getElementById('myForm');

// // Обработчик события отправки формы
//   form.addEventListener('submit', async function(event) {
//     event.preventDefault(); // Предотвращаем обычное поведение отправки формы

//     // Создание объекта FormData и добавление данных из формы
//     var formData = new FormData(form);
    
//     var jsonObject = {};
//     formData.forEach(function(value, key) {
//         jsonObject[key] = value;
//     });

//     // Отправка данных на сервер с использованием fetch()
//     await fetch('/api/registrate_user', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json;charset=utf-8'
//       },
//       body: JSON.stringify(jsonObject)
//     })
//     .then(response => response.json())
//     .then(data => {
//       // Обработка ответа от сервера
//       console.log(data);
//     })
//     .catch(error => {
//       // Обработка ошибок
//       console.error(error);
//     });
//   });
})