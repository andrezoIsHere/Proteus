class Reactions {

  updateInfo(token) {

    let infobar = document.querySelector('.workspace__part__info[id="' + token + '"]>.workspace__part__info__get');

    let likes = infobar.querySelector('.info__get__reaction#likes>button>i>span');

    let dislikes = infobar.querySelector('.info__get__reaction#dislikes>button>i>span');

    $.get('get_reaction', {'token': token}, function(data) {

      likes.innerText = JSON.parse(data)['likes'];

      dislikes.innerText = JSON.parse(data)['dislikes'];

      console.log(JSON.parse(data));

    });

  }

  setLike(token) {

    $.ajax({

      type: "GET",
      url: 'set_reaction',
      data: {'token': token, 'type': 'like'},
      dataType: 'text',
      cache: false,
      success: function(data) {

        this.updateInfo(token);

      }.bind(this)

    });

  }

  setDislike(token) {

    $.ajax({

      type: "GET",
      url: 'set_reaction',
      data: {'token': token, 'type': 'dislike'},
      dataType: 'text',
      cache: false,
      success: function(data) {

        this.updateInfo(token);

      }.bind(this)

    });

  }

}

executor = new Reactions()
