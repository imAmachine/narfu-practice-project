// document.querySelectorAll('.room__number__btn').forEach(el => {
//     el.addEventListener('click', function() {
//         document.querySelectorAll('.room__number__btn').forEach(btn => btn.classList.remove('room__number__btn_active'));
//         this.classList.add('room__number__btn_active');
//     });
// });

function clickRoom(btn) {
    document.querySelectorAll('.room__number__btn').forEach(btn => btn.classList.remove('room__number__btn_active'))
    btn.classList.add('room__number__btn_active')
}