(function(){
  var container = document.getElementById("interactive-blind-poll")
  var pollingOptions = ["Science Fiction", "Fantasy", "Strategie", "Rollenspiel"]

  var pollKeyElement = document.createElement('input')
  pollKeyElement.type = "number"
  pollKeyElement.id = "pollKey"
  pollKeyElement.name = "truhenschluessel-eingabe"

  var labelPollKey = document.createElement("label")
  labelPollKey.htmlFor = "pollKey";
  labelPollKey.appendChild(document.createTextNode("Truhenschluessel : "));

  var pollingElements = pollingOptions.map(function(pollItem) {
    var refPollItem = pollItem.toLowerCase()

    var checkboxCon = document.createElement("div")
    var checkbox = document.createElement("input")
    
    checkbox.type = "checkbox"
    checkbox.id = refPollItem
    checkbox.name = refPollItem
    checkbox.value = pollItem

    var label = document.createElement("label")
    label.htmlFor = refPollItem;
    label.className = "padded"
    label.appendChild(document.createTextNode(pollItem));

    checkboxCon.appendChild(checkbox)
    checkboxCon.appendChild(label)
    return checkboxCon
  })

  container.appendChild(labelPollKey)
  container.appendChild(pollKeyElement)

  pollingElements.forEach(checkbox => {
    container.appendChild(checkbox)
  });
  
})();