function toggleAnswerBox() {
    form = document.getElementById("answer_form");
    display_value = form.style.display;
    form.style.display = display_value === 'none' ? '' : 'none'
}
