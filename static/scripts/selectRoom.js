document.querySelectorAll('.list__number__btn').forEach(el => {
    el.addEventListener('click', function() {
        document.querySelectorAll('.list__number__btn').forEach(btn => btn.classList.remove('list__number__btn_active'));
        this.classList.add('list__number__btn_active');
    });
});