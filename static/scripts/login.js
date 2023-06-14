const buttonAuth = document.querySelector('.buttonAuth');
const closeImgs = document.querySelectorAll('.close_img');
const btns = document.querySelectorAll('.loginForm__wrapper__btn');
const inputEyes = document.querySelectorAll('.loginForm__wrapper__inputWrapper__eye');
const images = document.querySelectorAll('.main__wrapper__left__img');


// Изменения поле пароля с text на password и наоборот + смена класса картинки глаза (обычный и зачеркнутый)
const togglePasswordVisibility = (inputEye, passwordInput) => {
  const passwordInputType = passwordInput.getAttribute('type');
  const newInputType = passwordInputType === 'password' ? 'text' : 'password';
  inputEye.src = inputEye.src.includes('_line')
    ? inputEye.src.replace('_line', '')
    : inputEye.src.replace('eye', 'eye_line');
  passwordInput.setAttribute('type', newInputType);
};

const activateImageLink = (img) => {
  images.forEach((img) => img.classList.remove('main__wrapper__left__img_active'));
  img.classList.add('main__wrapper__left__img_active');
};


// переворот картонки при регистрации / авторизации
btns.forEach((btn) => btn.addEventListener('click', rotateCardAuth));

inputEyes.forEach((inputEye, index) => {
  const passwordInput = document.getElementsByClassName('loginForm__wrapper__input')[index * 2 + 1];
  inputEye.addEventListener('click', () => togglePasswordVisibility(inputEye, passwordInput));
});

buttonAuth.addEventListener('click', openCloseForm);
closeImgs.forEach((closeImg) => closeImg.addEventListener('click', openCloseForm));

images.forEach((img) => img.addEventListener('click', () => activateImageLink(img)));
