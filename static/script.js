function get_answers(queston_id) {
    answersDiv = document.getElementById("answers-div");
    answersDiv.innerHTML = "";
    $.ajax({
        url: "/api/v1/questions/" + queston_id + "/answers",
        method: 'GET',
        success: function (data) {
            //console.log(data);
            if (data === undefined) { return; }

            data.forEach(function(answer) {
                console.log(answer);

                var answerDiv = document.createElement('div')
                answerDiv.className = "section-margin"
                answerDiv.setAttribute('answer-id', answer.id);

                var content_p = document.createElement('p');
                content_p.style = "white-space: pre-wrap;"
                content_p.innerHTML = answer['content'];
                answerDiv.appendChild(content_p);

                var user_p = document.createElement('p');
                user_p.className = "smaller-font";
                user_p.innerHTML = "By: <strong>" + answer.user_name + "</strong>, " + answer.user_email;
                answerDiv.appendChild(user_p);

                answersDiv.appendChild(answerDiv);
            });
        }
    });
}

$(document).ready(function() {
    $("#answer_form").submit(function(e) {
        e.preventDefault();

        var formData = $(this).serializeArray();
        var myJson = {};
        formData.forEach(function(field) {
            myJson[field.name] = field.value;
        });

        question_id = myJson['question_id'];
        var url = "/api/v1/questions/" + question_id + "/answers/";
        delete myJson['question_id'];

        $.ajax({
            url: url,
            method: 'PUT',
            data: JSON.stringify(myJson),
            //processData: false,
            success: function() {
                get_answers(question_id);
            }
        });
    });
});
