function openTab(evt, tabName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  document.getElementById(tabName).style.maxWidth = "100%";
  if (tabName == "sell" || tabName == "buy") {
    document.getElementById(tabName).style.borderRight = "1px solid rgb(46, 46, 46)";;
  }
  evt.currentTarget.className += " active";
}