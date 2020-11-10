window.onload = function () {
  // audio module
  (function () {
    var context = new (window.AudioContext || window.webkitAudioContext)();
    var request = new XMLHttpRequest();

    request.open("GET", "/audio/tonight-c-3.wav");
    request.responseType = "arraybuffer";
    request.onload = function () {
      context.decodeAudioData(request.response, onDecoded);
    };

    request.send();

    function onDecoded(audioBuffer) {
      var bufferSource = context.createBufferSource();
      bufferSource.buffer = audioBuffer;
      bufferSource.connect(context.destination);
      bufferSource.start();
    }
  })();

  // database module
  var currentPoll = (function (firebase) {
    // Firebase configuration
    var firebaseConfig = {
      apiKey: "AIzaSyAG7ivSRnQUGb5xTuzztDM9YOzGY1IZKJc",
      authDomain: "blind-game-poll.firebaseapp.com",
      databaseURL: "https://blind-game-poll.firebaseio.com",
      projectId: "blind-game-poll",
      storageBucket: "blind-game-poll.appspot.com",
      messagingSenderId: "72922648857",
      appId: "1:72922648857:web:52ad5ce5e05b68bf4c3588",
    };
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);

    var database = firebase.database();

    return database
      .ref("/polls/0")
      .once("value")
      .then(function (snapshot) {
        return snapshot.val();
      })
      .catch(function () {
        alert(
          "Die Daten fuer die Abstimmung konnten nicht geladen werden, ist deine Internetverbindung ok ?"
        );
      });
  })(window.firebase);

  // poll render module
  (function (poll) {
    poll.then(function (pollData) {
      var container = document.getElementById("interactive-blind-poll");
      var pollingOptions = pollData.items.map(function (pollItem) {
        return pollItem.name;
      });

      var pollKeyElement = document.createElement("input");
      pollKeyElement.type = "text";
      pollKeyElement.id = "pollKey";
      pollKeyElement.name = "truhenschluessel-eingabe";

      var labelPollKey = document.createElement("label");
      labelPollKey.htmlFor = "pollKey";
      labelPollKey.appendChild(document.createTextNode("Truhenschluessel : "));

      var pollingElements = pollingOptions.map(function (pollItem) {
        var refPollItem = pollItem.toLowerCase().replace(" ", "-");

        var checkboxCon = document.createElement("div");
        var checkbox = document.createElement("input");

        checkbox.type = "checkbox";
        checkbox.id = refPollItem;
        checkbox.name = refPollItem;
        checkbox.value = pollItem;

        var label = document.createElement("label");
        label.htmlFor = refPollItem;
        label.className = "padded";
        label.appendChild(document.createTextNode(pollItem));

        checkboxCon.appendChild(checkbox);
        checkboxCon.appendChild(label);
        return checkboxCon;
      });

      container.appendChild(labelPollKey);
      container.appendChild(pollKeyElement);

      pollingElements.forEach((checkbox) => {
        container.appendChild(checkbox);
      });

      var button = document.createElement("button");
      button.appendChild(document.createTextNode("Absenden"));

      container.appendChild(button);

      firebase
        .database()
        .ref("/polls/0")
        .on("value", function (snapshot) {
          var pollData = snapshot.val();
          button.onclick = function () {
            var selectedVotes = 0;

            var checkboxes = pollingElements.map(function (checkboxCon) {
              checkbox = checkboxCon.querySelector("input[type=checkbox]");
              if (checkbox.checked) {
                selectedVotes = selectedVotes + 1;
              }
              return [checkbox, checkbox.checked];
            });

            if (selectedVotes != 2) {
              alert(
                "Du hast zwei Stimmen ! Du hast aber " +
                  selectedVotes +
                  " checkboxen aktiviert."
              );

              return;
            } else {
              var truhenschluessel = pollKeyElement.value;
              if (truhenschluessel.length != 16) {
                alert(
                  "Dein Truhenschluessel muss exakt 16 Zeichen haben, aktuell hast du " +
                    truhenschluessel.length +
                    " Zeichen."
                );
              } else {
                var validKey = false;
                var keyVotePermission = true;

                pollData.keys.forEach(function (key) {
                  if (truhenschluessel === key.value) {
                    validKey = true;
                    // check if the key was already used
                    pollData.items.forEach(function (item) {
                      if (typeof item.votes === "object") {
                        Object.keys(item.votes).forEach(function (
                          voteInstanceKey
                        ) {
                          if (
                            item.votes[voteInstanceKey] === truhenschluessel
                          ) {
                            keyVotePermission = false;
                          }
                        });
                      }
                    });
                  }
                });

                if (!validKey || !keyVotePermission) {
                  alert(
                    "Dein Truhenschluessel ist ungueltig oder wurde schon benutzt !"
                  );
                } else {
                  var votes = [];
                  checkboxes.forEach(function (checkbox) {
                    if (checkbox[1] === true) {
                      votes.push(checkbox[0].value);
                    }
                  });

                  var update = {};
                  votes.forEach(function (vote) {
                    var dbVoteIndex = -1;

                    pollData.items.some(function (dbVoteItem) {
                      dbVoteIndex += 1;
                      if (dbVoteItem.name === vote) {
                        return true;
                      }
                    });

                    var updateVoteKey = firebase
                      .database()
                      .ref()
                      .child("polls/0/items/" + dbVoteIndex + "/votes")
                      .push().key;

                    update[
                      "polls/0/items/" + dbVoteIndex + "/votes/" + updateVoteKey
                    ] = truhenschluessel;
                  });
                  if (Object.keys(update).length > 0) {
                    firebase
                      .database()
                      .ref()
                      .update(update, function (error) {
                        if (!error) {
                          alert("Deine Abstimmung war erfolgreich !");
                        } else {
                          alert(
                            "Deine Abstimmung war nicht erfolgreich, bitte versuche es spaeter nochmal !"
                          );
                        }
                      });
                  } else {
                    alert(
                      "Es gab einen Fehler bei der Uebertragung deiner Abstimmung, bitte versuche es spaeter nochmal ! "
                    );
                  }
                }
              }
            }
          };
        });
    });
  })(currentPoll);
};
