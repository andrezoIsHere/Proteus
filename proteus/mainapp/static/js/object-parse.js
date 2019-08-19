
function openSpan(object) {

  let parent = object.parentNode.parentNode;

  parent.querySelector('span[little]').style.display = 'none';

  parent.querySelector('span[full]').style.display = 'inline-block';

  return false;

}

document.addEventListener('DOMContentLoaded', function () {

  let elems = document.querySelectorAll('.item__workspace__part');

  for(var i = 0; i < elems.length; i++) {

    let parent = elems[i];

    let span = elems[i].querySelector('span');

    if(span.innerText.length >= 700) {

      let hidden = document.createElement("div");

      hidden.className = 'workspace__part__hidden';
      hidden.innerHTML = '<span little>' + span.innerText.substr(0, 700) + '<button onClick="openSpan(this); return false">Показать полностью</button></span><span full>' + span.innerText + '</span>';

      elems[i].insertBefore(hidden, elems[i].querySelector('span'));

      span.remove();

    }

  }

});
