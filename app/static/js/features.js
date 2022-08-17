page = document.querySelector('.mg');
page.style.display = 'none';

document.addEventListener('DOMContentLoaded', () => {
    page.style.display = 'block';
    const features = document.querySelectorAll('.admin-feature').forEach((feature) => {
        feature.onclick = () => load_page(feature.dataset.page);
        return false
    })

    function load_page(page) {
        const request = new XMLHttpRequest();
        request.open('GET', `/admin/${page}`);

        request.onload = () => {
            const data = request.responseText;
            document.querySelector('div.box').innerHTML = data;
        }
        request.send();
    }

});
