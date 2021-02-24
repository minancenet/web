function push(type, title, content) {
  notifications = document.getElementById("notifications");

  notification = document.createElement("div");
  notification.classList.add("notification");
  notificationChildElement = notifications.appendChild(notification);

  notificationImage = document.createElement("i");
  notificationChildImage = notification.appendChild(notificationImage);
  notificationChildImage.classList.add("fas");
  if (type == "rally") {
    notificationChildImage.classList.add("fa-rocket");
  }
  else if (type == "crash") {
    notificationChildImage.classList.add("fa-skiing");
  }
  else {
    notificationChildImage.classList.add("fa-scroll");
  }

  notificationBody = document.createElement("div");
  notificationChildBody = notification.appendChild(notificationBody);
  notificationChildBody.classList.add("notification-body");

  notificationExit = document.createElement("span");
  notificationExit.classList.add("exit");
  notificationExit.innerHTML = "&times;";
  notificationExit.setAttribute("onclick", "closeNotification(this)")
  notificationExitChildElement = notificationBody.appendChild(notificationExit);
  
  notificationTitle = document.createElement("p");
  notificationTitle.classList.add("notification-title");
  notificationTitle.innerHTML = title;
  notificationTitleChildElement = notificationBody.appendChild(notificationTitle);

  notificationContent = document.createElement("p");
  notificationContent.classList.add("notification-content");
  notificationContent.innerHTML = content;
  notificationContentChildElement = notificationBody.appendChild(notificationContent);

  notificationClear = document.createElement("div");
  notificationClear.classList.add("clear");
  notificationChildClear = notification.appendChild(notificationClear);

  notification.style.animationPlayState = "running";
}

function closeNotification(notification) {
  notification.closest(".notification").remove()
}

// <div class="notifications" id="notifications">
// <div class="notification">
//   <i class="fas fa-rocket"></i>
//   <div class="notification-body">
//   <span class="exit" onclick="closeNotification(this)"></span>
//     <p class="notification-title" id="title">Stock of Stonks</p>
//     <p class="notification-content">Stock of Stonks price has crashed 50%.</p>
//   </div>
//   <div class="clear"></div>
// </div>
// </div>