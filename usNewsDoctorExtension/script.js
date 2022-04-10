async function scriptAsyncFunction() {
	let buttonExists = true; 
	const triggerLoadMore = () => {
		var buttons = document.querySelectorAll('button');
		let numBtns = 0; 
		let loadMoreButtons = [];
		buttons.forEach(button => { 
			if (button.textContent === "Load More") {
				loadMoreButtons.push(button);
				numBtns += 1; 	
			} 
		}); 

		if (numBtns == 2) {
			loadMoreButtons[0].click();
		} else if (numBtns == 1) {
			buttonExists = false; 
		}


		
		/*
		const numBtns = document.getElementsByClassName("Button__ButtonDeprecated-suns4m-1 LoadMoreWrapper__LoadMore-zwyk5c-1 hUZEpc exwUNV").length;
		const loadMoreBtn = document.getElementsByClassName("Button__ButtonDeprecated-suns4m-1 LoadMoreWrapper__LoadMore-zwyk5c-1 hUZEpc exwUNV")[0];
		if (numBtns === 2) {
			loadMoreBtn.click();
		} else {
			console.log("i cannot click");
			buttonExists = false;
		}
		*/
	}
	triggerLoadMore();
	console.log(buttonExists);


	const AvailableMutationObserver = window.MutationObserver || window.WebKitMutationObserver;
	const observer = new AvailableMutationObserver(mutations => {
		if (mutations.length && buttonExists === true) {
			triggerLoadMore();
			console.log(buttonExists);
			if (buttonExists === false) {
				console.log("i am here");
				const hospitalName = document.querySelector('h1').textContent.replace("Doctors","");
				const allDoctors = document.querySelectorAll('[data-test-id=DetailCardDoctor]');
				let data = [];
				allDoctors.forEach(doc => {
					const docName = doc.querySelector('h2').textContent;
					dict = {"Hospital": hospitalName};
					if (docName) {
						dict["Name"] = docName;
					}
					const specialties = doc.querySelector('[class*=DetailCardDoctor__Wrapper]').querySelectorAll('p');
					if (specialties) {
						dict["Broader Specialty"] = specialties[0].textContent;
						if (specialties.length >= 2) {
							dict["Specific Specialty"] = specialties[1].textContent;
						}

					}

					/*
					for (let i = 0; i < specialities.length; i++) {
						
					}
					specialities.forEach(specialty => {
						speciality.textContent;
					}); */
					const bio = doc.querySelector('p.sm-hide').textContent;
					if (bio) {
						dict["Bio"] = bio;
					}

					const additionalAttributes = doc.querySelector('[class*=DetailCardDoctor__PromoContainerSmall]').querySelectorAll('[class*=DetailCardDoctor__DataPoint]');

					if (additionalAttributes) {
						console.log(docName);
						additionalAttributes.forEach(attribute => {
							const paragraphs = attribute.querySelectorAll('p');
							if (paragraphs) {
								try {
									dict[paragraphs[1].textContent] = paragraphs[0].textContent
								} catch (error) {}
							}
						})
					}

					data.push(dict);





					//.querySelector('[class*=DetailCardDoctor__PromoContainerSmall]').querySelectorAll('[class*=DetailCardDoctor__DataPoint]')[0].querySelectorAll('p')[1].textContent

					//doctors.push({ docName }); //add more properties here
				});

				console.log(data);
				chrome.runtime.sendMessage(null, JSON.stringify(data));




				//const allDoctors = document.querySelectorAll()
				//allDoctors[0].querySelectorAll('[class*=DetailCardDoctor__TitleWrapper]')[0]
				/*
				const allDoctors = document.querySelectorAll('h2');
				let doctors = [];
				allDoctors.forEach(doc => {
					const docName = doc.textContent;
					doctors.push({ docName }); //add more properties here
				});
				doctors = doctors.slice(1, -1);
				const data = { doctors }
				chrome.runtime.sendMessage(null, JSON.stringify(data)); */
				
			}
		} 
	});

	const doctorsContainer = document.querySelector('.DoctorResults__ListWrapper-yx1idw-1.ma');
	observer.observe(doctorsContainer, { subtree: true, childList: true });
}

(async () => {
	await scriptAsyncFunction();
})();