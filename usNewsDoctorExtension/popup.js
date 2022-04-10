'use strict';

let adult_urls_list = [];


function pause(milliseconds) {
	var dt = new Date();
	while ((new Date()) - dt <= milliseconds) { /* Do nothing */ }
}

const adult_url = chrome.runtime.getURL('usNews/rankingData/data1.json');

fetch(adult_url).then(function(response) {
	response.json().then(allData => {
		allData.forEach(data => { 
			adult_urls_list.push(data["Link"] + "/doctors")
		})
	  });
	//return(response.json())
   })

console.log("url list", adult_urls_list);


// start navigation when #startNavigation button is clicked
let currentPage = 0;
let currentTab;
const folderName = new Date().toLocaleString().replace(",", "").replaceAll(":", "-").replaceAll("/", "-");
startNavigation.onclick = function (element) {
	// query the current tab to find its id
	chrome.tabs.query({ active: true, currentWindow: true }, async function (tabs) {
		currentTab = tabs[0].id;
		goToPage(adult_urls_list[0], 1, currentTab);

	});
};

function goToPage(url, url_index, tab_id) {
	return new Promise(function (resolve, reject) {
		// update current tab with new url
		chrome.tabs.update({ url: url });
		// resolve();
		// fired when tab is updated
		chrome.tabs.onUpdated.addListener(function openPage(tabID, changeInfo) {
			// tab has finished loading, validate whether it is the same tab
			if(tab_id == tabID && changeInfo.status === 'complete') {
				// remove tab onUpdate event as it may get duplicated
				chrome.tabs.onUpdated.removeListener(openPage);

				// fired when content script sends a message
				chrome.runtime.onMessage.addListener(function getDOMInfo(message) {
					// remove onMessage event as it may get duplicated
					chrome.runtime.onMessage.removeListener(getDOMInfo);

					// save data from message to a JSON file and download

					let blob = new Blob([message], {type: "application/json;charset=utf-8"});
					let objectURL = URL.createObjectURL(blob);
					//chrome.downloads.download({ url: objectURL, filename: `${folderName}/data${currentPage + 1}.json`, conflictAction: 'overwrite' });
					chrome.downloads.download({ url: objectURL, filename: `usNews/adultDoctorData/data${currentPage + 1}.json`, conflictAction: 'overwrite' });
					currentPage += 1;
					if (adult_urls_list[currentPage]) {
						goToPage(adult_urls_list[currentPage], currentPage + 1, currentTab);
						pause(300000);
					} else {
						alert('Navigation Completed');
					}
				});

				// // execute content script
				chrome.tabs.executeScript(tabID, { file: 'script.js' }, function() {
					// resolve Promise after content script has executed
					resolve();
				});
			}
		});
	});
}
