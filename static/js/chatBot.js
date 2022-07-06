$(document).ready(function() {
    var outputArea = $("#chat-output");
    $('#myModal').modal('show');
    var increament = 0;
    var query_flag = false;
    var session = document.getElementById('session_id').innerHTML;
    var user_id = document.getElementById('user_id').innerHTML;
    var chat_history_flag = true;
    var reset_button = false;
    var restart = false;
    var restart_count = 0;
    var next_response;
    var input_type=false;

    reset_fun = function() {  
        chat_history_flag = false;
        clickOnModalSection();
    } 
    continue_fun = function() {  
        // document.getElementById("quickReplies").innerHTML = "";
        if (next_response){
            setQuickResponse(next_response);
        }else{
            $("#input-user").show();
        }
        // setQuickResponse(next_response);
    }
    
    clickOnModalSection = function () {
        $("#chatBotMessageSection").show();
        $("#input-user").hide();
        query_flag = false;
        $("#myModal").modal('hide');
        
        setInput("Hello","Hello");
    }

    statusButton = function () {
        var request_chat_history = JSON.stringify({
            "session_id": session, //add the user ID here
            "user_id": user_id
        });
        jQuery.ajax({
        url: 'http://127.0.0.1:8000/api/check_status',
        type: "POST",
        data: request_chat_history,
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        // beforeSend: function (x) {
        //     query_flag = false;
        //     $("#quickReplies").html("");
        // },
        success: function (result) {
            if (result["completion_status"] == 1){
                document.getElementById('status').innerHTML = "Complete"
            }else{
                document.getElementById('status').innerHTML = "Incomplete"
            }
        }
    });
    };

    $("#user-input").keydown(function (e) {
        if (e.keyCode == 13 || e.which == 13) {
            e.preventDefault();
        }
    });
    
    $("#user-input").keyup(function (e) {
        var message = $("#user-input").text().trim();
        
        if(message != '' && message != null && message != 'null') {
            $("#submitInputButton").prop('disabled', false);
        } else {
            $("#submitInputButton").prop('disabled', true);
        }
        
        if ((e.keyCode == 13 || e.which == 13) && $("#user-input").text() != null) {
            bot_api_submitInput();
        }
    });
    
    chat_history_submitInput = function (value) {
        $("#input-user").hide()
        query_flag = false
        var request_chat_history = JSON.stringify({
            "session_id": session, //add the user ID here
            "user_id": user_id
        });
        jQuery.ajax({
            url: 'http://127.0.0.1:8000/api/chat_history',
            type: "POST",
            data: request_chat_history,
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            beforeSend: function (x) {
                // $("#wave").show()
                $(".incoming_msg").scrollTop($(".incoming_msg").prop('scrollHeight'));
                $("#input-user").hide();
                query_flag = false;
                // $("#user-input").html('');
                $("#quickReplies").html("");
            },
            success: function (result) {
                $("#input-user").hide();
                query_flag = false;
                if (result.length == 0){
                    chat_history_flag = false;
                    bot_api_submitInput(value);
                }else{
                    chat_history_flag = true;
                    integrateResponse(result);
                }
            }
        });
    };

    bot_api_submitInput = function (value) {
        if (restart_count == 0){
            restart = true;
        }else{
            restart = false;
        }
        chat_history_flag = false;
        var message = $("#user-input").text().trim();
        if(value){

        }else if(message !== '' || message !== null || message !== 'null' && query_flag==true) {
            value = message.replace(/\\n/g, "\\n")
        }
        //Remove previous padding from bot reply
        $("#input-user").hide()
        query_flag = false
        outputArea.append(`<div class="outgoing_msg"><div class="sent_msg"><p>${message}</p></div></div>`);
        $(".incoming_msg").scrollTop($(".incoming_msg").prop('scrollHeight'));
        
        var request = JSON.stringify({
            "sender": session, //add the user ID here
            "payload": value,
            "message": message,
            "restart": restart,
            "user_id": user_id
        });
        restart_count = restart_count+1;
        jQuery.ajax({
            url: 'http://127.0.0.1:8000/api/bot_api',
            type: "POST",
            data: request,
            dataType: "json",
            contentType: "application/json;charset=utf-8",
            beforeSend: function (x) {
                $("#wave").show()
                $(".incoming_msg").scrollTop($(".incoming_msg").prop('height'));
                $("#input-user").hide();
                query_flag = false;
                $("#user-input").html('');
                $("#quickReplies").html("");
            },
            success: function (result) {
                $("#input-user").hide();
                query_flag = false;
                // $("#wave").hide();
                integrateResponse(result);
            }
        });
    };
    
    setInput = function(text,value) {
        text = text.replace(/\_/g, "\'")
        if (chat_history_flag){
            chat_history_submitInput(value);
        }else{
            $("#user-input").text(text);
            bot_api_submitInput(value);
        }
        $("#input-user").hide();
        query_flag = false;
    }

    var increament_list = [];
    integrateResponse = function (result) {
        var msg = [];
        var button_var = "";
        if(result.length == 0){
            query_flag = true;
        }

        for (var i = 0; i < result.length; i++) {
            if (result[i]["image"]){
                var str = result[i]["image"];
                var str_pos = str.indexOf("Chartsfinal-04");
                if (str_pos > -1) {
                    increament++;
                    increament_list.push(increament);
                    msg.push( '<div id="app" class= "container_chart4"><p class="botResult" ><img id="myImg'+increament+'" width="300" height="200" src="' + result[i].image + '/"></p><div class="clearfix"></div></div></br>');
                } else {
                    if (i == result.length-1 && button_var == "") { 
                        query_flag = true;
                        increament++;
                        increament_list.push(increament);
                        msg.push('<div id="app"><p class="botResult" ><img id="myImg'+increament+'" width="300" height="200" src="' + result[i].image + '/"></p><div class="clearfix"></div></div></br>');
                    }else {
                        increament++;
                        increament_list.push(increament);
                        msg.push('<div id="app"><p class="botResult" ><img id="myImg'+increament+'" width="300" height="200" src="' + result[i].image + '/"></p><div class="clearfix"></div></div></br>');
                    }
                }
            }
            if (result[i]["attachment"]){
                query_flag = true;
                msg.push( '<p class="botResult" ><iframe width="300" height="200" src="' + result[i]["attachment"]["payload"]["src"] + '&enablejsapi=1"  frameborder="0" style="border: solid 4px #37474F" ></iframe></p><div class="clearfix"></div></br>');
            }
            if (result[i]["text"] && i == result.length-1) {
                query_flag = true;
                msg.push('<p class="botResult">' + result[i].text + '</p></br>');
            }else if (result[i]["text"]){
                msg.push('<p class="botResult">' + result[i].text + '</p></br>');
            }
            if (result[i]["text"] == "Calendar") {
                query_flag = true;
                // msg.push('<p class="botResult"><iframe src="https://fullcalendar.io/demos" name="iframe_a" height="300px" width="100%" title="Iframe Example"></iframe></p></br>');
            }
            if (result[i]["text"] == "OK, Thanks.") {
                input_type=true;
                query_flag = true;
            }
            if(result[i]["buttons"]){
                button_var = result[i]["buttons"];
                var buttons = []
                $("#input-user").hide();
                query_flag = false;
                for (var b=0; b < result[i]["buttons"].length; b++){
                    buttons[b]=result[i]["buttons"][b]
                }
            }
            if (result[i]["input_text"] && i == result.length-1) {
                query_flag = true;
                msg.push('<div class="outgoing_msg"><div class="sent_msg"><p>' + result[i]["input_text"] + '</p></div></div>');
            }else if (result[i]["input_text"]){
                msg.push('<div class="outgoing_msg"><div class="sent_msg"><p>' + result[i]["input_text"] + '</p></div></div>');
            }
            if (result[i]["next_response"] != "") {
                next_response = result[i]["next_response"];
            }
            if (result[i]["response_text"] && i == result.length-1) {
                reset_button =  true;
                query_flag = true;
                for (let l = 0; l < result[i].response_text.length; l++) {
                msg.push('<p class="botResult">' + result[i].response_text[l] + '</p></br>');
                // msg.push('<p class="botResult">' + result[i].response_text[1] + '</p></br>');
                }
                $("#quickReplies").html('<button class="replies" id="' + "Restart" + '" onClick="reset_fun()"><p>' + "Restart" + '</p></button>\
                <button class="replies" id="' + "Continue" + '" onClick="continue_fun()"><p>' + "Continue" + '</p></button></br>');
            }else if (result[i]["response_text"]){
                msg.push('<p class="botResult">' + result[i].response_text + '</p></br>');
            }
            
        }
        if(msg) {
            addTextResponse(msg, buttons, increament_list, setQuickResponse, zoomimage)
            $("#wave").hide();
            $(".incoming_msg").scrollTop($(".incoming_msg").prop('scrollHeight'));
        }
    }
        
     
    addTextResponse = function (textReplies, buttons, increament_list, setQuickResponse, zoomimage) {
        return new Promise(function(resolve, reject) {
            var k = 0 ;
            var speed_var=0;
            function chatspeed(){
                // var speed_var=0;
                if (chat_history_flag){
                    $("#wave").hide();
                    outputArea.append(`<div class="received_withd_msg user-message">${textReplies[k]}</div>`);
                    $(".incoming_msg").scrollTop($(".incoming_msg").prop('scrollHeight'));
                    k++;
                    if (k < textReplies.length){
                        chatspeed()
                    }
                    var len = increament_list.length;
                    for (var i = 0; i < len; i++){
                        var img = document.getElementById('myImg'+increament_list[i]);
                        if (img){
                            zoomimage(increament_list[i]);
                        }   
                    }
                    if(buttons && k==textReplies.length){

                        setQuickResponse(buttons);  
                    }else if (k==textReplies.length && reset_button == false){
                        $("#input-user").show();
                    }
                }else{
                    setTimeout(function(){ 
                        $("#wave").hide();
                        outputArea.append(`<div class="received_withd_msg user-message">${textReplies[k]}</div>`);
                        $(".incoming_msg").scrollTop($(".incoming_msg").prop('scrollHeight'));
                        k++;
                        if (k < textReplies.length){
                            speed_var = 5000;
                            chatspeed()
                        }
                        var len = increament_list.length;
                        for (var i = 0; i < len; i++){
                            var img = document.getElementById('myImg'+increament_list[i]);
                            if (img){
                                zoomimage(increament_list[i]);
                            }   
                        }
                        if(buttons && k==textReplies.length)	{
                            setQuickResponse(buttons);  
                        }else if (k==textReplies.length && input_type==false){
                            $("#input-user").show();
                        }
                        console.log(1*speed_var)
                    }, 1*speed_var);
                }
                // $(".incoming_msg").scrollTop($("#chat-output").prop('scrollHeight'));
                $("#wave").show();
                $(".incoming_msg").scrollTop($(".incoming_msg").prop('scrollHeight'));

            }
            chatspeed()
        })
    }
    
    zoomimage = function (inc) {
        var modal1 = document.getElementById('myModal1');
        var img = document.getElementById('myImg'+inc);
        var modalImg = document.getElementById("img01");
        var captionText = document.getElementById("caption");
        img.onclick = function(){
            modal1.style.display = "block";
            modalImg.src = this.src;
            captionText.innerHTML = this.alt;
        }
            
        // When the user clicks on <span> (x), close the modal1
        modal1.onclick = function() {
            img01.className += " out";
            setTimeout(function() {
                modal1.style.display = "none";
                modalImg.src = "";
                captionText.innerHTML = "";
                img01.className = "modal1-content";
            }, 400);
        }
    }

    setQuickResponse = function (quickReplies) {
        $("#input-user").hide();
        chat_history_flag = false;
        query_flag = false;
        var buttons = "";
        var check_list_buttons = "";
        var check_title = [];
        var check_payload = "";
        var buttons_spl = "";
        if (quickReplies.length <= 6){
            for (var i = 0; i < quickReplies.length; i++) {
                if (quickReplies[i].title == "SITUATION" || quickReplies[i].title == "THOUGHTS/BELIEFS" || quickReplies[i].title == "EMOTIONS" || quickReplies[i].title == "BEHAVIOUR" || quickReplies[i].title == "PHYSIOLOGICAL RESPONSE"){
                    title1 = quickReplies[i].title;
                    payload1 = quickReplies[i].payload;
                    title2 = title1.replace(/\'/g, "_")
                    buttons_spl += '<button class="replies_spl replies_spl'+i+'" id="' + quickReplies[i].title + '" onClick="setInput(\'' + title2 + '\',\'' + payload1 + '\');">'+'</button></br>';
                }
                else if (quickReplies[i].payload == "/checklist"){
                    title1 = quickReplies[i].title;
                    payload1 = quickReplies[i].payload;
                    title2 = title1.replace(/\'/g, "_")
                    check_title.push(title2);
                    check_payload = payload1
                    check_list_buttons += '<label for="'+ quickReplies[i].title +'"> <input type="checkbox" name="color" value="'+ quickReplies[i].title +'" id="'+ quickReplies[i].title +'">'+ quickReplies[i].title +'</label></br>';
                }
                else if (quickReplies[i].title == "I'm done for today!"){
                    continue;
                } {
                    title1 = quickReplies[i].title;
                    payload1 = quickReplies[i].payload;
                    title2 = title1.replace(/\'/g, "_")
                    buttons += '<button class="replies" id="' + quickReplies[i].title + '" onClick="setInput(\'' + title2 + '\',\'' + payload1 + '\');"><p>' + quickReplies[i].title + '</p></button></br>';
                }
            }
        }else {
            for (var i = 0; i < quickReplies.length; i=i+2) {
                if (i+1 == quickReplies.length) {
                    title1 = quickReplies[i].title;
                    payload1 = quickReplies[i].payload;
                    title2 = title1.replace(/\'/g, "_")
                    buttons += '<button class="replies" id="' + quickReplies[i].title + '" onClick="setInput(\'' + title2 + '\',\'' + payload1 + '\');"><p>' + quickReplies[i].title + '</p></button></br>';
                }else {
                    title1 = quickReplies[i].title;
                    payload1 = quickReplies[i].payload;
                    title2 = quickReplies[i+1].title;
                    payload2 = quickReplies[i+1].payload;
                    title21 = title1.replace(/\'/g, "_")
                    title31 = title2.replace(/\'/g, "_")
                    buttons += '<button class="replies" id="' + quickReplies[i].title + '" onClick="setInput(\'' + title21 + '\',\'' + payload1 + '\');"><p>' + quickReplies[i].title + '</p></button><button class="replies" id="' + quickReplies[i+1].title + '" onClick="setInput(\'' + title31 + '\',\'' + payload2 + '\');"><p>' + quickReplies[i+1].title + '</p></button></br>';
                }
            }
        }


        if(buttons){
            $("#quickReplies").html(buttons);
            divElement = document.querySelector("#quickReplies");
            elemHeight = divElement.offsetHeight;
            const style = document.createElement('style');
            style.innerHTML = `
                .incoming_msg {
                    height: calc(90vh - `+elemHeight+`px);
                }
            `;
            document.head.appendChild(style);
        }else if(check_list_buttons && check_title && check_payload) {
            $("#quickReplies").html(check_list_buttons+'<button class="replies" id="' + "Select" + '"><p>' + "Select" + '</p></button></br>');
            const btn = document.querySelector('#Select');
            btn.addEventListener('click', (event) => {
                let checkboxes = document.querySelectorAll('input[name="color"]:checked');
                let values = [];
                checkboxes.forEach((checkbox) => {
                    values.push(checkbox.value);
                });
                setInput( values+ ' ' , check_payload );
            }); 

            divElement = document.querySelector("#quickReplies");
            elemHeight = divElement.offsetHeight;
            const style = document.createElement('style');
            style.innerHTML = `
                .incoming_msg {
                    height: calc(90vh - `+elemHeight+`px);
                }
            `;
            document.head.appendChild(style);
        }
        $(".incoming_msg").scrollTop($(".incoming_msg").prop('scrollHeight'));
        $(".container_chart4").append(buttons_spl);
    }
});
