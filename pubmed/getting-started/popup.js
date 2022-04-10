'use strict';

// list of urls to navigate
let urls_list = [
	'https://health.usnews.com/best-hospitals/area/pa/childrens-hospital-of-philadelphia-6231730/doctors',
	'https://health.usnews.com/best-hospitals/area/ma/dana-farber-cancer-institute-6140583/doctors',
	'https://health.usnews.com/best-hospitals/area/ga/childrens-healthcare-of-atlanta-6380021/doctors',
];

// start navigation when #startNavigation button is clicked
startNavigation.onclick = function (element) {
	// query the current tab to find its id
	chrome.tabs.query({ active: true, currentWindow: true }, async function (tabs) {
		goToPage(urls_list[0], 1, tabs[0].id);
		// urls_list.slice(1).forEach((url, i) => {
		// 	const position = i + 1;
		// 	console.log('position==>>', position)
		// 	setTimeout(() => {
		// 		goToPage(url, position, tabs[0].id);
		// 	}, position * 20000);
		// })

		// navigation of all pages is finished
		//alert('Navigation Completed');

	});
};

function goToPage(url, url_index, tab_id) {
	return new Promise(function (resolve, reject) {
		// update current tab with new url
		chrome.tabs.update({ url: url });
		console.log('before on updated==>>', url);
		// resolve();
		// fired when tab is updated
		chrome.tabs.onUpdated.addListener(function openPage(tabID, changeInfo) {
			console.log('on updated==>>')
			// tab has finished loading, validate whether it is the same tab
			if(tab_id == tabID && changeInfo.status === 'complete') {
				// remove tab onUpdate event as it may get duplicated
				chrome.tabs.onUpdated.removeListener(openPage);

				// fired when content script sends a message
				chrome.runtime.onMessage.addListener(function getDOMInfo(message) {
					// remove onMessage event as it may get duplicated
					chrome.runtime.onMessage.removeListener(getDOMInfo);

					// save data from message to a JSON file and download
					let json_data = {
						title: JSON.parse(message).title,
						h1: JSON.parse(message).h1,
						url: url
					};

					let blob = new Blob([JSON.stringify(json_data)], {type: "application/json;charset=utf-8"});
					let objectURL = URL.createObjectURL(blob);
					chrome.downloads.download({ url: objectURL, filename: ('content/' + url_index + '/data.json'), conflictAction: 'overwrite' });
				});


				console.log('before exec scc==>>')
				// // execute content script
				chrome.tabs.executeScript(tabID, { file: 'script.js' }, function() {
					console.log('inside exec scc==>>')
					// resolve Promise after content script has executed
					resolve();
				});
			}
		});
	});
}

// async function to wait for x seconds 
async function waitSeconds(seconds) {
	return new Promise(function (resolve, reject) {
		setTimeout(function () {
			resolve();
		}, seconds * 1000);
	});
}
