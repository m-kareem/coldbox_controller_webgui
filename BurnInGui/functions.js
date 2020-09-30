function openTab(evt, tabName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function loadMonitoringPanels() {

  var listOfEmbedsLarge = configData["listOfEmbedsLarge"];
  var listOfEmbedsSmall = configData["listOfEmbedsSmall"];

  renderEmbeds(configData["listOfEmbedsTemperatures"]);
  renderEmbeds(configData["listOfEmbedsHumidity"]);
  renderEmbeds(configData["listOfEmbedsLarge"], "618px", "300px");
}

function renderEmbeds(listOfEmbeds, width = "140px", height = "70px"){
  var div = document.createElement("div");
  div.class = "row";
  document.getElementById("ControlPanel").appendChild(div);

  for(link of listOfEmbeds){
    var ifrm = document.createElement("iframe");
    ifrm.setAttribute("src", link);
    ifrm.style.width = width;
    ifrm.style.height = height;
    ifrm.style.margin = "10px";
    div.appendChild(ifrm);
  }
}

function setupGUI(){
  configData = JSON.parse(config);

  loadMonitoringPanels();

  setupModules();
  setupCustomTests();

}

function setupModules(){
  var nModules = 4;
  var coldBoxType = "EC";

  var table = document.getElementById("moduleTable");

  for(i = 0; i < nModules; i++){
    var newRow = document.createElement("tr");
    table.appendChild(newRow);

    // module active
    var checkBoxEntry = document.createElement("td");
    newRow.appendChild(checkBoxEntry);

    var checkBoxDiv = document.createElement("div");
    checkBoxDiv.class = "checkbox";
    checkBoxEntry.appendChild(checkBoxDiv);

    var checkBoxLabel = document.createElement("label");
    checkBoxDiv.appendChild(checkBoxLabel);

    var checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = i;
    checkbox.id = "module_" + i;
    checkbox.value = "module_" + i;
    checkbox.checked = true;

    checkBoxLabel.appendChild(checkbox);
    checkBoxLabel.innerHTML = checkBoxLabel.innerHTML + "Chuck " + (i+1);


    // module type
    var moduleTypeEntry = document.createElement("td");
    newRow.appendChild(moduleTypeEntry);

    var moduleTypeSelect = document.createElement("select");
    moduleTypeSelect.class = "form-control";

    for(option of ["LS", "SS", "EC"]){
      var optionDOM = document.createElement("option");
      optionDOM.text = option;
      optionDOM.value = option;

      if(option == coldBoxType){
        optionDOM.selected = true;
      }

      moduleTypeSelect.add(optionDOM);
    }

    moduleTypeEntry.append(moduleTypeSelect);

    // module description
    var moduleDescEntry = document.createElement("td");
    newRow.appendChild(moduleDescEntry);

    var moduleDescDiv = document.createElement("div");
    moduleDescDiv.class = "form-group";
    moduleDescEntry.appendChild(moduleDescDiv);

    var moduleDesc = document.createElement("input");
    moduleDesc.type = "text";
    moduleDesc.class = "form-control";
    moduleDesc.id = "moduleDesc_" + i;
    moduleDesc.placeholder = "20UXYZ#####";

    moduleDescDiv.appendChild(moduleDesc);
  }
}

function setupCustomTests(){
  // setup adding tests
  var list = document.getElementById("testList");
  var add = document.getElementById("addButton");
  add.addEventListener('click', function(){
      var newElement = document.createElement('div');
      newElement.class = "row"
      list.appendChild(newElement);

      var selectInput = document.createElement("select");
      selectInput.class = "form-control";

      var listOfTests = {"strobe": "Strobe Delay", "3pg": "Three Point Gain", "trim": "Trim Range", "response": "Response Curve", "noiseOcc": "Noise Occupancy"};
      for(option in listOfTests){
        if (listOfTests.hasOwnProperty(option)) {
          var optionDOM = document.createElement("option");
          optionDOM.text = listOfTests[option];
          optionDOM.value = option;
          selectInput.add(optionDOM);
        }
      }

      newElement.appendChild(selectInput);

      var newButton = document.createElement("button");
      newButton.class = "close";
      newButton.type = "button";
      newButton.setAttribute("aria-label", "Close");
      newButton.innerHTML = "<span aria-hidden='true'>&times;</span>";
      newElement.appendChild(newButton);
      newButton.addEventListener('click', function () {
          this.parentNode.parentNode.removeChild(this.parentNode);
      });
  });
}

function toggleCustomTests(){
  document.getElementById("customTestsArea").classList.toggle("hidden");
}

function printToLog(string){
  var logDiv = document.getElementById("logBox");
  var toPrint = "\n<p>" + string + "</p>";
  logDiv.innerHTML = logDiv.innerHTML + toPrint;
}

var coldBoxRunning = false;

function startColdbox(){
  if(coldBoxRunning == true){
    console.log("Cannot start coldbox, if already running!");
    return;
  }
  coldBoxRunning = true;
  document.getElementById("startButton").setAttribute("disabled", "disabled");
  document.getElementById("stopButton").removeAttribute("disabled");
  printToLog("Starting Coldbox");
  setTimeout(() => { console.log("World!"); stopColdbox();}, 2000);
}

function stopColdbox(){
  if(coldBoxRunning == false){
    console.log("Cannot stop coldbox, if not running!");
    return;
  }
  printToLog("Stopping Coldbox");
  document.getElementById("stopButton").setAttribute("disabled", "disabled");
  document.getElementById("startButton").removeAttribute("disabled");
  coldBoxRunning = false;
}
