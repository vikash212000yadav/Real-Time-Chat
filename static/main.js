$(function () {
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + "/rtc/stream/";
    console.log("Connecting to " + ws_path);
    var socket = new ReconnectingWebSocket(ws_path);

    socket.onopen = function () {
        console.log("Connected to chat socket");
    };
    socket.onclose = function () {
        console.log("Disconnected from chat socket");
    };

    socket.onmessage = function (message) {
        console.log("Got websocket message " + message.data);
        var data = JSON.parse(message.data);
        if (data.error) {
            alert(data.error);
            return;
        }
        if (data.join) {
            console.log("Joining room " + data.join);
            var roomdiv = $(
                "<div class='room' id='room-" + data.join + "'>" +
                "<h2>" + data.title + "</h2>" +
                "<div class='messages'></div>" +
                "<input><button>Send</button>" +
                "</div>"
            );
            $("#rtc").append(roomdiv);
            roomdiv.find("button").on("click", function () {
                socket.send(JSON.stringify({
                    "command": "send",
                    "room": data.join,
                    "message": roomdiv.find("input").val()
                }));
                roomdiv.find("input").val("");
            });
        } else if (data.leave) {
            console.log("Leaving room " + data.leave);
            $("#room-" + data.leave).remove();
        } else if (data.message || data.msg_type != 0) {
            var msgdiv = $("#room-" + data.room + " .messages");
            var ok_msg = "";
            switch (data.msg_type) {
                case 0:
                    ok_msg = "<div class='message'>" +
                        "<span class='username'>" + data.username + "</span>" +
                        "<span class='body'>" + data.message + "</span>" +
                        "</div>";
                    break;
                case 1:
                    ok_msg = "<div class='contextual-message text-warning'>" + data.message + "</div>";
                    break;
                case 2:
                    ok_msg = "<div class='contextual-message text-danger'>" + data.message + "</div>";
                    break;
                case 3:
                    ok_msg = "<div class='contextual-message text-muted'>" + data.message + "</div>";
                    break;
                case 4:
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username + " joined the room!" + "</div>";
                    break;
                case 5:
                    ok_msg = "<div class='contextual-message text-muted'>" + data.username + " left the room!" + "</div>";
                    break;
                default:
                    console.log("Unsupported message type!");
                    return;
            }
            msgdiv.append(ok_msg);
            msgdiv.scrollTop(msgdiv.prop("scrollHeight"));
        } else {
            console.log("Cannot handle message!");
        }
    };

    function inRoom(roomId) {
        return $("#room-" + roomId).length > 0;
    };

    $("li.room-link").click(function () {
        roomId = $(this).attr("data-room-id");
        if (inRoom(roomId)) {
            $(this).removeClass("joined");
            socket.send(JSON.stringify({
                "command": "leave",
                "room": roomId
            }));
        } else {
            $(this).addClass("joined");
            socket.send(JSON.stringify({
                "command": "join",
                "room": roomId
            }));
        }
    });
});