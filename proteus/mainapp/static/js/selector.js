function select(object) {

	let urls = {

		world: 'https://rus.azattyq.org/api/zrqomeuuo_',
		main: 'https://rus.azattyq.org/api/zororegtor',
		politics: 'https://rus.azattyq.org/api/z_roperuom',
		asia: 'https://rus.azattyq.org/api/zjrooeyuoo',
		kazakhstan: 'https://rus.azattyq.org/api/zgroqe_uoq'

	}	

	url = urls[object.getAttribute('id')];

	$.get('set_global_url', {url: url}, function(data) {

		if(data == 'true') {

			let rows = document.querySelectorAll('.item__workspace__userspace>.workspace__userspace__row');

			for(var elem = 0; elem < rows.length; elem++) {

				blocks = rows[elem].querySelectorAll('.workspace__userspace__block');

				for(var block = 0; block < blocks.length; block++) {

					blocks[block].querySelector('button').setAttribute('selected', 'false');
					blocks[block].querySelector('button').innerText = 'Выбрать';

					object.querySelector('button').setAttribute('selected', 'true');
					object.querySelector('button').innerText = 'Выбрано';

				}

			}

		}

	});

}