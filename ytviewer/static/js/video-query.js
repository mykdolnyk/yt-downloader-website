const textField = document.getElementById('video_url')
const goButton = document.getElementById('go_button');
const throbber = document.getElementById('throbber');
const resultInfo = document.getElementById('result-info');

const errorMessage = "<p>Something went wrong! Please double-check if the ID/URL you entered is correct.</p>"

// goButton.addEventListener('click', function () {
//     let userInput = textField.value;

//     if (userInput == '') {
//         return
//     }

//     textField.value = '';

//     throbber.style.display = 'block';
//     requestAnimationFrame(() => {
//         throbber.style.opacity = 1;
//     });

//     finalRequestVideoUrl = `${requestVideoUrl}?video_url=${userInput}`;

//     fetch(finalRequestVideoUrl)
//     .then(response => response.json())
//     .then(data => {
//         if (data.success) {
//             finalShowVideoUrl = `${showVideoUrl}?video_url=${data.id}`
//             displayLoadingDone(`<p>Here is your video:</p> <a class="button result_url" href="${finalShowVideoUrl}">${data.title}</a>`);
//         } else {
//             displayLoadingDone(errorMessage);
//         }
//     })  
//     .catch(error => {
//         displayLoadingDone(errorMessage)
//     });;
// });

goButton.addEventListener('click', async function () {
    let userInput = textField.value;

    if (userInput == '') {
        return
    }

    let finalQueueVideoUrl = `${requestVideoUrl}?video_url=${userInput}`;

    // Play the loading animation
    textField.value = '';
    throbber.style.display = 'block';
    requestAnimationFrame(() => {
        throbber.style.opacity = 1;
    });

    // Queue the video
    try {
        response = await fetch(finalQueueVideoUrl)
        data = await response.json()
        console.log(data)
        if (!data.success) {
            displayLoadingDone(errorMessage);
            return;
        }
    }
    catch (error) {
        displayLoadingDone(errorMessage);
        return;
    }

    let videoId = data.video_id
    let finalPollVideoUrl = `${pollVideoUrl}?video_id=${videoId}`;

    // Poll for video status updates
    try {
        for (let attempt = 0; attempt < 120; attempt++) {
            response = await fetch(finalPollVideoUrl)
            data = await response.json()
            if (!data.success) {
                displayLoadingDone(errorMessage);
                break
            }
            if (data.status == 'pending') {
                // Wait for 5s
                await new Promise(resolve => setTimeout(resolve, 2000));
                continue
            }
            if (data.status == 'complete') {
                finalShowVideoUrl = `${showVideoUrl}?video_url=${data.id}`
                displayLoadingDone(`<p>Here is your video:</p> <a class="button result_url" href="${finalShowVideoUrl}">${data.title}</a>`);
                break
            }
        }
    } catch (error) {
        displayLoadingDone(errorMessage)
        return true
    }
    
    // Fallback in case there is still no response once the polling is over
    if (throbber.style.display != 'none') {
        displayLoadingDone(errorMessage)
    }
});


function displayLoadingDone(newResultInfo) {
    throbber.style.opacity = 0;
    throbber.style.display = 'none';

    resultInfo.style.opacity = 1;

    resultInfo.innerHTML = newResultInfo
}