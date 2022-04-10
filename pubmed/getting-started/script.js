
//const delayMe = ms => {
//	return new Promise(resolve => setTimeout(resolve, ms))
//}

async function delayMe(seconds) {
	return new Promise(function(resolve, reject) {
		setTimeout(function() {
			resolve();
		}, seconds*1000);
	});
}

async function scriptAsyncFunction() {
	console.log('got here==>>>');

	// 1. trigger loadMore button
	// 2. add mutation observer on list of doctors
	// 3. when new doctors are added to the list, trigger loadmore btn again
	// 4. reapeat for 3 or desired no of times
	// 5. send data at that point in time 

	const hey = new Promise((resolve) => {
		const loadMoreBtn = document.getElementsByClassName("Button__ButtonDeprecated-suns4m-1 LoadMoreWrapper__LoadMore-zwyk5c-1 gNlWQL kmWga")[0];
		loadMoreBtn.click();
		console.log('btn clickedd==>>')
		setTimeout(resolve, 5000);
	});
	// await hey;
	// await hey;
	await Promise.all(Array.from(Array(3).keys()).map(async () => {
		try {
			// await hey;
			const loadMoreBtn = document.getElementsByClassName("Button__ButtonDeprecated-suns4m-1 LoadMoreWrapper__LoadMore-zwyk5c-1 gNlWQL kmWga")[0];
			console.log('loadmmm==>>', loadMoreBtn.textContent);
			/// loadMoreBtn.scrollIntoView();
			// await delayMe(3);
			// await new Promise((resolve) => setTimeout(resolve, 3000));
			console.log('after firstn delay==>>');
			loadMoreBtn.click();
			// await delayMe(3);
			await new Promise((resolve) => setTimeout(resolve, 5000));
			console.log('after second delay==>>');
		} catch (e) {
			console.log('errrr tt==>>', e);
			// break;
		}
	}));

	console.log('all docs==>>', document.querySelectorAll('h2.kQuiLM')?.length);

	// let page_title = document.title,
	// 	page_h1_tag = '';


	// if(document.querySelector("h1") !== null)
	// 	page_h1_tag = document.querySelector("h1").textContent;

	// // prepare JSON data with page title & first h1 tag
	// let data = JSON.stringify({ title: page_title, h1: page_h1_tag });

	// // // send message back to popup script
	// chrome.runtime.sendMessage(null, data);
}

(async() => {
	console.log('got here async==>>>');
	await scriptAsyncFunction();
})();
