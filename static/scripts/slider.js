let img = document.querySelector('.main__wrapper__img');
let address = document.querySelector('.main__wrapper__subheader');
let text = document.querySelector('.main__wrapper__text');

document.addEventListener('DOMContentLoaded', async function() {
  //=================================================
  // Обработка работы слайдера
  //=================================================
  let sliderWrapper = document.getElementsByClassName("slider__wrapper")[0];
  let btnLeft = document.getElementsByClassName('slider__btn_left')[0];
  let btnRight = document.getElementsByClassName('slider__btn_right')[0];
  let sliderImages = document.querySelectorAll('.slider__img');

  let imgWidth = sliderImages[0].offsetWidth; // Получение ширины одного изображения
  let counter = 1;
  let startShift = 0;
  let gap = 10;

  let countVisible = Math.floor(sliderWrapper.offsetWidth / (imgWidth + gap)); // Вычисление количества видимых изображений

  let sliderShiftRight = () => {
      if (counter < sliderImages.length - countVisible) {
          counter += 1;
          startShift -= imgWidth + gap;
          sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`);
      } else if (counter === sliderImages.length - countVisible) {
          counter = 1; // Сбрасываем счетчик на начало
          startShift = 0; // Сбрасываем смещение
          sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`);
      }
  };

  let sliderShiftLeft = () => {
      if (counter > 1) {
          counter -= 1;
          startShift += imgWidth + gap;
          sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`);
      } else if (counter === 1) {
          counter = sliderImages.length - countMinus + 1;
          startShift = -(imgWidth + gap) * (sliderImages.length - countMinus);
          sliderImages.forEach(el => el.style.transform = `translateX(${startShift}px)`);
      }
  };

  btnLeft.onclick = sliderShiftLeft;
  btnRight.onclick = sliderShiftRight;

  // Обновление параметров при изменении размера окна
  window.addEventListener('resize', () => {
    countVisible = Math.floor(sliderWrapper.offsetWidth / (imgWidth + gap));
  });

  //=================================================
  // Обработка событий на форме выбора общежития и комнаты
  //=================================================
  // создание объекта для формирования заявки на заселение в общежитие
  let application = {
    "dormitory_id": null,
    "room_id": null
  }

  // Добавление обработчика событий на нажатие кнопки общежития в слайдере
  let btns_rooms = document.querySelector('.room__number__btns');
  let dormitoryImages = document.querySelectorAll('.slider__img');
  let room_img = document.querySelector('.room__img');
  dormitoryImages.forEach(function(image) {
    image.addEventListener('click', async function() {
      btns_rooms.innerHTML = ''; // Очистка блока с кнопками комнат
      // получение привязанного объекта общежития
      const dormitory = JSON.parse(image.getAttribute('data-object').replace(/'/g, '"'));
      // заполнение данных формы из объекта
      formDormitory = {
        "main__wrapper__header": document.querySelector('.main__wrapper__header'),
        "main__wrapper__img": document.querySelector('.main__wrapper__img'),
        "main__wrapper__subheader": document.querySelector('.main__wrapper__subheader'),
        "main__wrapper__title": document.querySelector('.main__wrapper__title'),
        "main__wrapper__text": document.querySelector('.main__wrapper__text'),
      };
      formDormitory['main__wrapper__header'].textContent = dormitory.name;
      formDormitory['main__wrapper__img'].setAttribute("src", dormitory.photo)
      formDormitory['main__wrapper__subheader'].textContent = 'Адрес: ' + dormitory.address;
      formDormitory['main__wrapper__text'].textContent = dormitory.description;

      // добавление в заявку выбранного общежития
      application['dormitory_id'] = dormitory.dormitory_id;

      await fetch(`/api/rooms/${dormitory.dormitory_id}`)
        .then(function(response) {
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(function(data) {
          if (data.length > 0) {
            // Обработка всех кнопок комнат выбранного общежития
            data.forEach(function(room) {
              let btn = document.createElement('button');
              btn.innerHTML = '№' + room.room_number + '<br>' + room.occupied + '/' + room.total_places;
              btn.disabled = room.status;
              btn.classList.add('room__number__btn');
              if (room.status) {
                btn.classList.add('room__number__btn_disable');
              }
              btns_rooms.appendChild(btn);
            });
          }
          return data;
        })
        .then(function(data) {
          // Получение списка свободных к заселению комнат
          let arr_available_rooms = Array.from(btns_rooms.children).filter(function(el) {
            return !el.classList.contains('room__number__btn_disable');
          });

          // перебор всех доступных к заселению комнат(кнопок)
          arr_available_rooms.forEach(function(btn) {
            // добавление обработчика события нажатия для кнопок
            btn.addEventListener('click', function() {
              // по клику удаляется класс room__number__btn_active со всех кнопок
              arr_available_rooms.forEach(function(avail_btn) {
                avail_btn.classList.remove('room__number__btn_active');
              });
              // по клику добавляется класс room__number__btn_active
              this.classList.add('room__number__btn_active');

              // Получение данных, относящихся к выбранной комнате
              let roomNumber = this.textContent.split('№')[1][0].trim(); // Получение номера комнаты из текста кнопки
              let selectedRoom = Array.from(data).filter(function(room) {
                return room.room_number === roomNumber;
              })[0];

              // добавление в заявку выбранной комнаты
              application['room_id'] = selectedRoom.room_id;
              // вставка изображения к выбранной комнате
              let photo_link = selectedRoom.photo != null ? selectedRoom.photo : "../static/img/unknown.png";
              room_img.setAttribute('src', photo_link);
            });
            // Автоматический выбор первой незаполненной комнаты
            if (arr_available_rooms.length > 0) {
              arr_available_rooms[0].click();
            }
          });
        })
        .catch(function(error) {
          console.error('Error:', error);
        });
    });
  });
  // Обработка нажатия кнопки "Создать заявку"
  let btnSubmit = document.querySelector('.room__number__btnSelect');
  if (btnSubmit) {
    btnSubmit.addEventListener('click', function() {
      // Получение значений dormitory_id и room_id из объекта application
      let dormitoryId = application.dormitory_id;
      let roomId = application.room_id;

      // Создание объекта для отправки данных на сервер
      let data = {
        dormitory_id: dormitoryId,
        room_id: roomId
      };

      // Отправка POST-запроса на сервер
      fetch(`/api/add_application/${dormitoryId}/${roomId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      .then(function(response) {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(function(data) {
        // Обработка успешного ответа от сервера
        console.log(data.message); // Вывод сообщения в консоль
        // Дополнительные действия по успешному созданию заявки
      })
      .catch(function(error) {
        // Обработка ошибки
        console.error('Error:', error);
        // Дополнительные действия при ошибке
      });
    });
  }
});

