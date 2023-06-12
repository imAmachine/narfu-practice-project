const btn = document.querySelector('.lk__btn')
const inputs = document.querySelectorAll('.lk__input')

btn.onclick = () => {
    inputs.forEach(el => {
        el.disabled = !el.disabled
        el.classList.toggle('lk__input_active')
    })

    if (btn.innerHTML == 'Сохранить') {
        btn.innerHTML = 'Изменить'
    }
    else {
        btn.innerHTML = 'Сохранить'
    }
}