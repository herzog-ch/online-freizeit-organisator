const username_input = $("#username-input");
// const search_icon = $('#search-icon')
const artists_div = $('#usernames-content');
const endpoint = 'user_search';
const delay_by_in_ms = 700;
let scheduled_function = false;
let guests = [];

const new_event_form = $('#new_event_form');
const ul_added_users = $('#added-users-ul');

new_event_form.on('submit', function(e, from_source) {
	
	if (from_source == null) {
		e.preventDefault();

		// delete all existing guest elements from form
		let form_children = new_event_form.children();
		for (let i = 0; i < form_children.length; i++) {
			if ($(form_children[i]).attr('id') == 'num_guests') {
				$(form_children[i]).remove();
			}
			else if ($(form_children[i]).attr('id') !== undefined && $(form_children[i]).attr('id').indexOf('guest-') == 0) {
				$(form_children[i]).remove();
			}
		}

		// add all guests as input type="hidden" to form
		for (let i = 0; i < guests.length; i++) {
			let id = 'guest-' + String(i);
			new_event_form.append('<input type="hidden" id="' + id + '" name="' + id + '" value="' + guests[i] + '">');
		}

		console.log('custom behavior');
		$(this).trigger('submit', true);
	}

	console.log('Default behavior');

});


let add_user = function(username) {
	if (guests.includes(username)) return;
  guests.push(username);
	add_user_html(username);
}

let add_user_html = function(username) {
	let id = 'li-' + username;
	ul_added_users.append('<li id="' + id + '" onclick="remove_user(\'' + username + '\')">' + username + '<i class="far fa-minus-square"></li>');
}

let remove_user = function(username) {
	let index_user = guests.indexOf(username);
	if (index_user > -1) {
		guests.splice(index_user, 1);
		remove_user_html(username);
	}
}

let remove_user_html = function(username) {
	let id = '#li-' + username;
	ul_added_users.find(id).remove();
}


let ajax_call = function (endpoint, request_parameters) {
  console.log(endpoint);
  console.log('ajax_call');
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			// fade out the artists_div, then:
			artists_div.fadeTo('slow', 0).promise().then(() => {
        // replace the HTML contents
        console.log(response);

        if (request_parameters['q'].length < 1) {
          artists_div.html('');
        }
        else {
          artists_div.html(response['html']);
        }
				// fade-in the div with new contents
				artists_div.fadeTo('slow', 1)
				// stop animating search icon
				// search_icon.removeClass('blink')
			})
		})
}

username_input.on('keyup', function () {
  console.log('keyup');
	const request_parameters = {
		q: $(this).val() // value of user_input: the HTML element with ID user-input
	}

  // if ($(this).val().length < 1) return;
	// start animating the search icon with the CSS class
	// search_icon.addClass('blink')

	// if scheduled_function is NOT false, cancel the execution of the function
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}

	// setTimeout returns the ID of the function to be executed
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})