class Menu {

  leaveAccount(object) {
    
    $.ajax({
      url: 'exit',
      xhrFields: {
        withCredentials: true
      },
      success: function(output, status, xhr) {

       let menu = document.querySelector('.header__big__navigation');

       window.location.reload();

      },
      cache: false
    });

  }

}

let menuWork = new Menu;
