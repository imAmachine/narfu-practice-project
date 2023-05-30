const loginForm = document.querySelector('.loginForm')
const buttonAuth = document.querySelector('.buttonAuth')
const closeImgs = document.querySelectorAll('.close_img')
const registration = document.querySelector('.loginForm__wrapper__registration')
const login = document.querySelector('.loginForm__wrapper__login')



const rotateCardAuth = () => {
  registration.classList.toggle('loginForm__wrapper__registration_rotate')
  login.classList.toggle('loginForm__wrapper__login_rotate')
};

const btns = document.querySelectorAll('.loginForm__wrapper__btn')
btns.forEach(btn => btn.addEventListener('click', rotateCardAuth))

const inputEyes = document.querySelectorAll('.loginForm__wrapper__inputWrapper__eye')
inputEyes.forEach((inputEye, index) => {
  const passwordInput = document.getElementsByClassName('loginForm__wrapper__input')[index * 2 + 1]
  inputEye.addEventListener('click', () => {
    const passwordInputType = passwordInput.getAttribute('type')
    inputEye.src = inputEye.src.includes('_line') ? inputEye.src.replace('_line', '') : inputEye.src.replace('eye', 'eye_line')
    passwordInput.setAttribute('type', passwordInputType === 'password' ? 'text' : 'password')
  });
});

const openCloseForm = () => {
  loginForm.classList.toggle('loginForm_hide')
  document.body.classList.toggle('body__overflowHidden')
};

buttonAuth.addEventListener('click', openCloseForm)
closeImgs.forEach(closeImg => closeImg.addEventListener('click', openCloseForm))