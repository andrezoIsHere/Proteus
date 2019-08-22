let search = document.querySelector('.main__header__little>input[name="search"]');

search.addEventListener('keydown', function(e) {

  if(search.value) {

    $.get('filter_feed', {'filter': 'tags'}, function(data) {
      console.log(data);
    });

  }

});
