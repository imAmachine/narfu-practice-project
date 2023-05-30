const loginForm = document.querySelector('.loginForm');
const buttonAuth = document.querySelector('.buttonAuth');
const closeImgs = document.querySelectorAll('.close_img');
const registration = document.querySelector('.loginForm__wrapper__registration');
const login = document.querySelector('.loginForm__wrapper__login');
const btns = document.querySelectorAll('.loginForm__wrapper__btn');
const inputEyes = document.querySelectorAll('.loginForm__wrapper__inputWrapper__eye');
const images = document.querySelectorAll('.main__wrapper__left__img');

const rotateCardAuth = () => {
  registration.classList.toggle('loginForm__wrapper__registration_rotate');
  login.classList.toggle('loginForm__wrapper__login_rotate');
};

const togglePasswordVisibility = (inputEye, passwordInput) => {
  const passwordInputType = passwordInput.getAttribute('type');
  const newInputType = passwordInputType === 'password' ? 'text' : 'password';
  inputEye.src = inputEye.src.includes('_line')
    ? inputEye.src.replace('_line', '')
    : inputEye.src.replace('eye', 'eye_line');
  passwordInput.setAttribute('type', newInputType);
};

const openCloseForm = () => {
  loginForm.classList.toggle('loginForm_hide');
  document.body.classList.toggle('body__overflowHidden');
};

const activateImageLink = (img) => {
  images.forEach((img) => img.classList.remove('main__wrapper__left__img_active'));
  img.classList.add('main__wrapper__left__img_active');
};

btns.forEach((btn) => btn.addEventListener('click', rotateCardAuth));

inputEyes.forEach((inputEye, index) => {
  const passwordInput = document.getElementsByClassName('loginForm__wrapper__input')[index * 2 + 1];
  inputEye.addEventListener('click', () => togglePasswordVisibility(inputEye, passwordInput));
});

buttonAuth.addEventListener('click', openCloseForm);
closeImgs.forEach((closeImg) => closeImg.addEventListener('click', openCloseForm));

images.forEach((img) => img.addEventListener('click', () => activateImageLink(img)));
