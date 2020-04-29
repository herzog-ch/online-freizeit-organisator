const username_input = $('#username-input');
const found_users = $('#usernames-content');
const new_event_form = $('#new_event_form');
const ul_added_users = $('#added-users-ul');
const endpoint = 'user_search';
const delay_by_in_ms = 50;
let scheduled_function = false;
let guests = [];

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

		$(this).trigger('submit', true); // set "from_source" parameter to true, so it will do the default behaviour and POST the form data
	}

});


let add_user = function(username) {
	if (guests.includes(username)) return;
  guests.push(username);
	add_user_html(username);
	found_users.fadeTo('slow', 0).promise().then(() => {
		found_users.html('');
		found_users.fadeTo('slow', 1)
	});
	username_input.val('');
}

let add_user_html = function(username) {
	let id = 'li-' + username;
	ul_added_users.append('<li id="' + id + '" onclick="remove_user(\'' + username + '\')"><span>' + username + '</span><i class="far fa-minus-square"></li>');
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
	$.getJSON(endpoint, request_parameters)
		.done(response => {
			// fade out, then:
			found_users.fadeTo('slow', 0).promise().then(() => {

        if (request_parameters['q'].length < 1) {
          found_users.html('');
        }
        else {
          found_users.html(response['html']);
        }
				// fade in with new contents
				found_users.fadeTo('slow', 1)
			})
		});
}

username_input.on('keyup', function () {
	const request_parameters = {
		q: $(this).val() // user input
	}
	// if scheduled_function is NOT false, cancel the execution
	if (scheduled_function) {
		clearTimeout(scheduled_function)
	}
	scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})