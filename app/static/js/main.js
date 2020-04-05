async function fetchAsync (url, room_id) {
    /* Updates the ingredients for more or less portions. */
    // Create URL that will give us new ingredients
    let url_calendar_room = url + `${room_id}/`;
    // Fetch the response and extract text
    let response = await fetch(url_calendar_room);
    let data = await response.text(); //.json();
    // Fill the appropriate element with response
    document.getElementById("calendar_content").innerHTML = data;
    // Update the displayed number of servings
    //document.getElementById("servings").innerText = servings;
  
  }

  function getComboA(selectObject) {
    var value = selectObject.value;  
    console.log(value);
    fetchAsync("/calendar/", value);
  }

  function updateRoomSelection() {
    var value = document.getElementById("room").value;
    console.log(value);
    fetchAsync("/calendar/", value);
  }