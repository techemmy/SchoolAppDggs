document.addEventListener('DOMContentLoaded', () => {
    const msg = document.querySelector(".flashed-msg");
    setInterval(() => {
        msg.innerHTML = '';
    }, 4000)

})