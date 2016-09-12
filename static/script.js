function set_edit_mode(edit_mode_on) {
    header = document.getElementById("editing-header")
    header.innerHTML = edit_mode_on ? "Edit answer" : "Add new answer";
}

function edit_answer(e, question_id, answer_id) {
    e.preventDefault();
    $.ajax({
        url: "/api/v1/questions/" + question_id + "/answers/" + answer_id,
        method: 'GET',
        success: function (data) {
            set_edit_mode(true);
            //document.getElementById('content').innerHTML = data.content;
            ['user_name', 'user_email', 'content'].forEach(function (s) {
                document.getElementById(s).value = data[s];
            });
            document.getElementById('answer_id').value = answer_id;
        }
    });
}

function get_answers(question_id) {
    answersDiv = document.getElementById("answers-div");
    answersDiv.innerHTML = "";
    $.ajax({
        url: "/api/v1/questions/" + question_id + "/answers",
        method: 'GET',
        success: function (data) {
            if (data === undefined || data.length === 0) {
                return;
            }

            var header = document.createElement("h2");
            header.className = "no-bottom-margin";
            header.innerHTML = "Answers";
            answersDiv.appendChild(header);

            data.forEach(function(answer) {
                var answerDiv = document.createElement('div');
                answerDiv.className = "section-margin";
                //answerDiv.setAttribute('answer-id', answer.id);
                //answerDiv.setAttribute('question-id', question_id);

                var content_p = document.createElement('p');
                content_p.style = "white-space: pre-wrap;";
                content_p.innerHTML = answer['content'];
                answerDiv.appendChild(content_p);

                var user_p = document.createElement('p');
                user_p.className = "smaller-font";
                user_p.innerHTML = "By: <strong>" + answer.user_name +
                    "</strong>, " + answer.user_email + " ";

                var editLink = document.createElement('a');
                editLink.onclick = function (e) {
                    edit_answer(e, question_id, answer.id);
                };
                editLink.href = "#";
                editLink.innerHTML = "Edit answer"
                user_p.appendChild(editLink);

                answerDiv.appendChild(user_p);
                answersDiv.appendChild(answerDiv);
            });
        }
    });
}

function clear_form() {
    set_edit_mode(false);
    ['user_name', 'user_email', 'content'].forEach(function (s) {
        document.getElementById(s).value = "";
    });
    document.getElementById('answer_id').value = "";
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

        if ('answer_id' in myJson) {
            url += myJson['answer_id'];
            delete myJson['answer_id'];
        }

        $.ajax({
            url: url,
            method: 'PUT',
            data: JSON.stringify(myJson),
            success: function() {
                clear_form();
                get_answers(question_id);
            }
        });
    });
});
