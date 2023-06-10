const btn = document.querySelector('.lk__btn')
const inputs = document.querySelectorAll('.lk__input')
const img = document.querySelector('.lk__img')
const file = document.querySelector('.file')

btn.onclick = () => {
    img.classList.toggle('lk__img_active')
    inputs.forEach(el => {
        el.disabled = !el.disabled
        el.classList.toggle('lk__input_active')
    })

    if (btn.innerHTML == 'Сохранить') {
        console.log(file.value)
        btn.innerHTML = 'Изменить'
        img.style = `background-image: url('${file.value}')`
    }
    else btn.innerHTML = 'Сохранить'
}