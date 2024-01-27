document.addEventListener('DOMContentLoaded', () => {
    const questionBlocks = document.getElementsByClassName('faq-question-block');
    
    for (let i = 0; i < questionBlocks.length; i++) {
        const button = questionBlocks[i].querySelector('.faq-question');
        const symbol = questionBlocks[i].querySelector('.faq-question > b');

        button.addEventListener('click', () => {
            questionBlocks[i].classList.toggle('active');
            symbol.textContent = symbol.textContent == '+' ? '-' : '+';
        });
    }
});